# Creating a Discord Bot account

1. Go to [Discord Developer Portal](https://discord.com/developers/applications),
 and login with your Discord account.
2. Click on `New Application` and give your bot a name.
 ![Step 1](img/step1.png)
3. Go to the left sidebar and click on `Bot`.
 ![Step 2](img/step3.png)
4. Click on `Reset Token` and copy the token. This your bot token for `DISCORD_TOKEN` in `config.py`.
 ![Step 3](img/step4.png)
5. Scroll down to `Privileged Gateway Intents`.
6. Enable **Message Content** Intent. This is important!
  ![Step 4](img/step5.png)

# Getting Channel ID

1. Go to your Discord server and right click on the channel where you want to sync the chat.
2. Click on `Copy ID` to copy the channel ID.
  ![Step 5](img/step6.png)
3. Paste the channel ID in `CHANNEL_ID` in `config.py`.
