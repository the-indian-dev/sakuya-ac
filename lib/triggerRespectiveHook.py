from logging import debug

def triggerRespectiveHook(packet_type, packet, player, message_to_client, message_to_server, plugin_manager):
    if packet_type == "FSNETCMD_LOGON":
        keep_message = plugin_manager.triggar_hook('on_login', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_LOGOFF":
        keep_message = plugin_manager.triggar_hook('on_logout', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_ERROR":
        keep_message = plugin_manager.triggar_hook('on_error', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_LOADFIELD":
        keep_message = plugin_manager.triggar_hook('on_load_field', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_ADDOBJECT":
        keep_message = plugin_manager.triggar_hook('on_add_object', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_READBACK":
        keep_message = plugin_manager.triggar_hook('on_readback', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_SMOKECOLOR":
        keep_message = plugin_manager.triggar_hook('on_smoke_color', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_JOINREQUEST":
        keep_message = plugin_manager.triggar_hook('on_join_request', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_JOINAPPROVAL":
        keep_message = plugin_manager.triggar_hook('on_join_approval', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_REJECTJOINREQ":
        keep_message = plugin_manager.triggar_hook('on_reject_join_request', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_AIRPLANESTATE":
        keep_message = plugin_manager.triggar_hook('on_flight_data', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_UNJOIN":
        keep_message = plugin_manager.triggar_hook('on_unjoin', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_REMOVEAIRPLANE":
        keep_message = plugin_manager.triggar_hook('on_remove_airplane', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_REQUESTTESTAIRPLANE":
        keep_message = plugin_manager.triggar_hook('on_request_test_airplane', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_KILLSERVER":
        keep_message = plugin_manager.triggar_hook('on_kill_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_PREPARESIMULATION":
        keep_message = plugin_manager.triggar_hook('on_prepare_simulation', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_TESTPACKET":
        keep_message = plugin_manager.triggar_hook('on_test_packet', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_LOCKON":
        keep_message = plugin_manager.triggar_hook('on_lockon', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_REMOVEGROUND":
        keep_message = plugin_manager.triggar_hook('on_remove_ground', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_MISSILELAUNCH":
        keep_message = plugin_manager.triggar_hook('on_missile_launch', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_GETDAMAGE":
        keep_message = plugin_manager.triggar_hook('on_get_damage', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_WEAPONCONFIG":
        keep_message = plugin_manager.triggar_hook('on_weapon_config', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_AIRCMD":
        keep_message = plugin_manager.triggar_hook('on_air_cmd', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_TEXTMESSAGE":
        keep_message = plugin_manager.triggar_hook('on_chat', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_ENVIRONMENT":
        keep_message = plugin_manager.triggar_hook('on_environment', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_SKYCOLOR":
        keep_message = plugin_manager.triggar_hook('on_sky_color', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_FOGCOLOR":
        keep_message = plugin_manager.triggar_hook('on_fog_color', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_LIST":
        keep_message = plugin_manager.triggar_hook('on_list', packet, player, message_to_client, message_to_server)
    else:
        keep_message = True
        debug(f"Unknown packet type {packet_type}, C2S")

    return keep_message

def triggerRespectiveHookServer(packet_type, packet, player, message_to_client, message_to_server, plugin_manager):
    if packet_type == "FSNETCMD_LOGON":
        keep_message = plugin_manager.triggar_hook('on_login_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_LOGOFF":
        keep_message = plugin_manager.triggar_hook('on_logout_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_ERROR":
        keep_message = plugin_manager.triggar_hook('on_error_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_LOADFIELD":
        keep_message = plugin_manager.triggar_hook('on_load_field_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_ADDOBJECT":
        keep_message = plugin_manager.triggar_hook('on_add_object_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_READBACK":
        keep_message = plugin_manager.triggar_hook('on_readback_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_SMOKECOLOR":
        keep_message = plugin_manager.triggar_hook('on_smoke_color_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_JOINREQUEST":
        keep_message = plugin_manager.triggar_hook('on_join_request_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_JOINAPPROVAL":
        keep_message = plugin_manager.triggar_hook('on_join_approval_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_REJECTJOINREQ":
        keep_message = plugin_manager.triggar_hook('on_reject_join_request_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_AIRPLANESTATE":
        keep_message = plugin_manager.triggar_hook('on_flight_data_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_UNJOIN":
        keep_message = plugin_manager.triggar_hook('on_unjoin_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_REMOVEAIRPLANE":
        keep_message = plugin_manager.triggar_hook('on_remove_airplane_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_REQUESTTESTAIRPLANE":
        keep_message = plugin_manager.triggar_hook('on_request_test_airplane_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_KILLSERVER":
        keep_message = plugin_manager.triggar_hook('on_kill_server_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_PREPARESIMULATION":
        keep_message = plugin_manager.triggar_hook('on_prepare_simulation_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_TESTPACKET":
        keep_message = plugin_manager.triggar_hook('on_test_packet_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_LOCKON":
        keep_message = plugin_manager.triggar_hook('on_lockon_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_REMOVEGROUND":
        keep_message = plugin_manager.triggar_hook('on_remove_ground_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_MISSILELAUNCH":
        keep_message = plugin_manager.triggar_hook('on_missile_launch_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_GETDAMAGE":
        keep_message = plugin_manager.triggar_hook('on_get_damage_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_WEAPONCONFIG":
        keep_message = plugin_manager.triggar_hook('on_weapon_config_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_AIRCMD":
        keep_message = plugin_manager.triggar_hook('on_air_cmd_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_TEXTMESSAGE":
        keep_message = plugin_manager.triggar_hook('on_chat_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_ENVIRONMENT":
        keep_message = plugin_manager.triggar_hook('on_environment_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_SKYCOLOR":
        keep_message = plugin_manager.triggar_hook('on_sky_color_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_FOGCOLOR":
        keep_message = plugin_manager.triggar_hook('on_fog_color_server', packet, player, message_to_client, message_to_server)
    elif packet_type == "FSNETCMD_LIST":
        keep_message = plugin_manager.triggar_hook('on_list_server', packet, player, message_to_client, message_to_server)
    else:
        keep_message = True
        debug(f"Unknown packet type {packet_type}, S2C")

    return keep_message
