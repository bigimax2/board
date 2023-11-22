import requests, json
import pandas as pd
from board import settings
from kill import tools
from kill.models import AllianceStatic, Kills

def ParserKill():
	allia_id = settings.ID_ALLIANCE
	all_id = AllianceStatic.objects.get(alli_id=settings.ID_ALLIANCE)
	allkill = Kills.objects.all().filter(id_alli_id=all_id.id).order_by('-date_kill')
	for kill in allkill:
		tools.Fitting(kill.killmailID)
		data = tools.Request_To_CCP(kill.killmailID, kill.hash_kill)

		attac = data['attackers']
		vict = data['victim']
		items = vict['items']

		tools.Get_Items(items, kill.id)
		x = pd.json_normalize(attac, max_level=2)
		y = pd.json_normalize(vict, max_level=2)


		if 'character_id' in vict.keys():
			vic_char_id = vict['character_id']
			kill.victim_personage_portrait = tools.Personage_Get_Icon(vic_char_id)
			kill.victim_personage_name = tools.GetName(vic_char_id)
		else:
			kill.victim_personage_name = None

		vic_char_corp = vict['corporation_id']
		kill.victim_personage_corp_name = tools.GetName(vic_char_corp)
		kill.victim_personage_corp_icon = tools.Corporation_Icon(vic_char_corp)
		if 'alliance_id' in vict.keys():
			vic_char_alli = vict['alliance_id']
			kill.victim_personage_all_name = tools.GetName(vic_char_alli)
			kill.victim_personage_all_icon = tools.Alliance_Icon(vic_char_alli)
			kill.save()
			if str(vic_char_alli) == allia_id:
				kill.loss = True
		else:
			kill.victim_personage_all_name = None
			kill.victim_personage_all_icon = None
		vic_char_ship = vict['ship_type_id']
		kill.victim_personage_ship_id = vic_char_ship

		group_info = tools.Get_GroupID_Type(vic_char_ship)
		kill.victim_personage_ship_name = tools.GetName(vic_char_ship)
		kill.victim_personage_ship_type = group_info[0]
		kill.victim_personage_ship_group_id = group_info[1]
		kill.json_kill = data

		datekill = data['killmail_time']
		kill.date_kill = datekill
		systemid = data['solar_system_id']
		system_info = tools.System_Info(systemid)
		kill.solar_system_name = system_info[0]
		kill.solar_system_ss = system_info[1]
		kill.region_name = system_info[2]
		kill.save()

		for t in attac:
			tr = t['final_blow']
			if tr == False:
				continue
			else:
				if 'character_id' in t.keys():
					att_char_id = t['character_id']
					kill.attack_final_personage_name = tools.GetName(att_char_id)
				else:
					kill.attack_final_personage_name = None

				if 'corporation_id' in t.keys():
					att_char_corp = t['corporation_id']
					kill.attack_final_personage_corp_name = tools.GetName(att_char_corp)
					kill.attack_final_personage_corp_icon = tools.Corporation_Icon(att_char_corp)
				else:
					kill.attack_final_personage_corp_name = None
					kill.attack_final_personage_corp_icon = None

				if 'alliance_id' in t.keys():
					att_char_alli = t['alliance_id']
					kill.attack_final_personage_all_name = tools.GetName(att_char_alli)
					kill.attack_final_personage_all_icon = tools.Alliance_Icon(att_char_alli)
				else:
					kill.attack_final_personage_all_name = None
					kill.attack_final_personage_all_icon = None

				att_char_ship = t['ship_type_id']
				kill.attack_final_personage_ship_id = att_char_ship

				kill.save()
