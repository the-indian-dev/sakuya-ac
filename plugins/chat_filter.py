"""
Enables moderation of words in chat to make it safe for children
"""

from lib.PacketManager.packets import FSNETCMD_TEXTMESSAGE
import re

# To disable moderation completely disable this, set ENABLED = False
# To allow some profanity, set ABOVE_13 = True

ENABLED = True
ABOVE_13 = False

class Plugin:
    def __init__(self):
        self.plugin_manager = None
        if ABOVE_13:
            # Moderate less for teens/adults - only severe language and unsafe links
            moderation_string = r'\b(b[i!]tch|cunt|whore|slut|bastard|nude|naked|porn|penis|vagina|boobs|dick|hate|murder|die|n[i!]gg?(er|a|as|ers)|f[a@]gg?ot?|kike|chink|retard|racist|racism|rape|rapist|molest|https?:\/\/\S+|www\.\S+)\b'
        else:
            # Stricter moderation for children
            moderation_string = r'\b(f[u\*]ck(?:er|ing)?|sh[i!]t(?:ty|head)?|b[i!]tch(?:es|y)?|cunt|ass(?:hole|wipe|hat)?|' \
                                r'whore|slut(?:ty)?|damn(?:it)?|hell|piss(?:ed)?|bastard|nude|naked|' \
                                r'sex(?:ual)?|porn(?:ography)?|penis|vagina|boobs?|tits?|titties|dick|' \
                                r'cock|pussy|boner|' \
                                r'horny|jerk(?:\s*off)?|masturbat(?:e|ion)|cum(?:ming)?|' \
                                r'hate|kill|murder|die|stupid|idiot|dumb(?:ass)?|moron|' \
                                r'n[i!]gg?(?:er|a|as|ers)|f[a@]gg?ot?|kike|chink|spic|wetback|' \
                                r'retard(?:ed)?|racist|racism|nazi|' \
                                r'rape(?:d|s)?|rapist|molest(?:er|ed)?|pedophile|' \
                                r'bl[o0][w0]job|handjob|' \
                                r'wtf|stfu|gtfo|lmfao|' \
                                r'https?:\/\/\S+|www\.\S+)\b'

        self.filter_regex = re.compile(moderation_string, re.IGNORECASE)

    def register(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.plugin_manager.register_hook('on_chat', self.on_chat)

    @staticmethod
    def censor_match_dynamic_length(match_obj):
        """
        This function is called by re.sub for each match.
        It returns a string of '#' characters matching the length of the found word.
        """
        matched_word = match_obj.group(0)  # Get the actual text that was matched
        return '#' * len(matched_word)

    def on_chat(self, data, player, message_to_client, message_to_server):
        decode = FSNETCMD_TEXTMESSAGE(data)
        msg = decode.raw_message

        # Check if the message contains filtered content
        censored_text = self.filter_regex.sub(self.censor_match_dynamic_length, msg)

        if censored_text != msg:
            # Create a new message with censored content
            message = FSNETCMD_TEXTMESSAGE.encode(censored_text, with_size=True)
            message_to_server.append(message)
            return False
        return True
