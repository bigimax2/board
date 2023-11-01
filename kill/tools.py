import datetime
import json
import math
import os
import tarfile
from datetime import date

import requests

from board import settings
from kill import views
from kill.models import KillGroup, AllianceStatic, ActiveCorp, CharacterActive, Kills, KillFromCCP
import time


def corp_alli(id_alliance):
	ur = ("https://esi.evetech.net/latest/alliances/{}/corporations/?datasource=tranquility".format(id_alliance))
	resultat = requests.get(ur)
	resultat.raise_for_status()
	data = resultat.json()
	count_corp = len(data)

	return count_corp

# не трогай!!! работает
def alli_state(request, id_alliance):
	ur = ("https://zkillboard.com/api/stats/allianceID/{}/".format(id_alliance))
	resultat = requests.get(ur)
	resultat.raise_for_status()
	data = resultat.json()
	cont_corp = corp_alli(id_alliance)
	active_pvp = data.get('activepvp')
	act_corp = active_pvp['corporations']['count']
	act_chars = active_pvp['characters']['count']
	ship_loss = data['shipsLost']
	ship_kills = data['shipsDestroyed']
	point_loss = data['pointsLost']
	point_kills = data['pointsDestroyed']
	isk_loss = data['iskLost']
	isk_destroyed = data['iskDestroyed']
	id_alli = data['id']
	date_founded = data['info']['date_founded']
	state_db = AllianceStatic.objects.all().filter(alli_id=id_alliance)

	if len(state_db) != 0:
		for i in state_db:
			i.count_corp = cont_corp
			i.count_active_corp = act_corp
			i.count_active_chars = act_chars
			i.ships_lost = ship_loss
			i.ships_destroyer = ship_kills
			i.point_lost = point_loss
			i.point_destroyer = point_kills
			i.isk_lost = isk_loss
			i.isk_destroyer = isk_destroyed
			i.date_founded_alli = date_founded
			i.save()
	else:
		AllianceStatic.objects.create(count_active_corp=act_corp, ships_destroyer=ship_kills, ships_lost=ship_loss,
	                                        point_lost=point_loss, point_destroyer=point_kills, isk_destroyer=isk_destroyed,
	                                        isk_lost=isk_loss, count_active_chars=act_chars, count_corp=cont_corp, alli_id=id_alli,
		                              date_founded_alli=date_founded)
	return data


def alli_kills_state(request, id_alliance):
	all_kills = AllianceStatic.objects.all().filter(alli_id=id_alliance)
	f = AllianceStatic.objects.get(alli_id=id_alliance)
	for a in all_kills:
		date_found = a.date_founded_alli
		fond_yar = date_found[:4]
		fond_mont = date_found[5:7]
	current_date = date.today()
	now_mont = current_date.month
	now_year = current_date.year

	len_data =''
	len_page = 0

	while len_data != 0:
		len_page +=1

		ur = ('https://zkillboard.com/api/allianceID/{}/year/{}/month/{}/page/{}/'.format(id_alliance, now_year, now_mont, len_page))
		time.sleep(1)
		resultat = requests.get(ur)
		resultat.raise_for_status()
		data = resultat.json()
		len_data = len(data)
		for a in data:
			kill_in_dict = a
			kill_id = a['killmail_id']
			z = a['zkb']
			location_id = z['locationID']
			hash_kill = z['hash']
			fittedValue = z['fittedValue']
			droppedValue = z['droppedValue']
			destroyedValue = z['destroyedValue']
			totalValue = z['totalValue']
			points = z['points']
			npc = z['npc']
			solo = z['solo']
			awox = z['awox']

			default_for_update = {'killmailID': kill_id, 'locationID': location_id, 'hash_kill': hash_kill, 'fittedValue': fittedValue,
			                       'droppedValue': droppedValue, 'destroyedValue': destroyedValue, 'totalValue': totalValue,
			                       'points': points, 'npc': npc, 'solo': solo, 'awox': awox , 'id_alli_id': f.id}
			Kills.objects.update_or_create(id_alli_id=id_alliance, defaults=default_for_update)
	return all_kills


def kill_groups(state, id_alli):
	s = state.get('groups')
	f = AllianceStatic.objects.get(alli_id=id_alli)
	for a in s :
			group_id = a
			if 'shipsDestroyed' in s[a]:
				killship = s[a]['shipsDestroyed']
			else:
				killship = 0
			if 'shipsLost' in s[a]:
				lossship = s[a]['shipsLost']
			else:
				lossship = 0

			ur = ('https://esi.evetech.net/latest/universe/groups/{}/?datasource=tranquility&language=en'.format(a))
			time.sleep(0.25)
			resultat = requests.get(ur)
			resultat.raise_for_status()
			data = resultat.json()
			name = data['name']

			default_for_update = {"id_group":group_id, "ship_kills":killship, "ship_loss":lossship, "name":name, "id_alli_id":f.id}

			KillGroup.objects.update_or_create(id_group=a, defaults=default_for_update)
	return s


def Active_Pvp(date, id_alli):
	get_corp = date.get('topAllTime')
	idalli = AllianceStatic.objects.get(alli_id=id_alli)
	i_d = idalli.id
	for a in get_corp[1:2]:
		corp_list = a['data']
		for i in corp_list:
			corpid = i['corporationID']
			corpkill = i['kills']
			ur = ('https://esi.evetech.net/latest/corporations/{}/?datasource=tranquility'.format(corpid))
			time.sleep(0.25)
			resultat = requests.get(ur)
			resultat.raise_for_status()
			data = resultat.json()
			name = data['name']
			default_for_update = {"corp_id":corpid, "corp_name": name, "corp_kills":corpkill, "id_alli_id": i_d}
			ActiveCorp.objects.update_or_create(corp_id=corpid, defaults=default_for_update)

	for b in get_corp[0:1]:
		char_list = b['data']
		for c in char_list:
			char_id = c['characterID']
			char_kill = c['kills']
			ir = ('https://esi.evetech.net/latest/characters/{}/?datasource=tranquility'.format(char_id))
			time.sleep(0.25)
			resultat = requests.get(ir)
			resultat.raise_for_status()
			data = resultat.json()
			name = data['name']
			default_for_update = {"char_id": char_id, "char_kills": char_kill, "id_alli_id": i_d, "char_name": name}
			CharacterActive.objects.update_or_create(char_id=char_id, defaults=default_for_update)
	return get_corp

def DownloadFile(id_alli = settings.ID_ALLIANCE):
	current_date = datetime.datetime.now()
	now_mont = current_date.month
	now_year = current_date.year
	now_day = current_date.day
	n_day = 0
	fondaunt_date = (datetime.datetime(2023, 7, 16))

	while fondaunt_date <= current_date:

		fun_year = fondaunt_date.year
		mont_slice = fondaunt_date
		fun_month = str(mont_slice)[5:7]
		fun_day = str(mont_slice)[8:10]

		url = "https://data.everef.net/killmails/{}/killmails-{}-{}-{}.tar.bz2".format(fun_year, fun_year,
	                                                                            fun_month, fun_day)
		r = requests.get(url)
		fondaunt_date += (datetime.timedelta(days=1))
		with open('D:/kills/killmails-{}-{}-{}.tar.bz2'.format(fun_year, fun_month, fun_day), 'wb') as f:

				f.write(r.content)
				pat = 'D:/unpack_archive_kill/kills-{}-{}-{}'.format(fun_year, fun_month, fun_day)
				tar = tarfile.open('D:/kills/killmails-{}-{}-{}.tar.bz2'.format(fun_year, fun_month, fun_day))
				tar.extractall(pat)
				tar.close()



def GetRelate():
	ur = "https://zkillboard.com/api/related/30000110/202310230800/"
	resultat = requests.get(ur)
	resultat.raise_for_status()
	data = resultat.json()

	return data

def CikleKillAlliance():
	allia_id = settings.ID_ALLIANCE
	direc = 'D:/unpack_archive_kill/'
	idalli = ''
	i = ''
	for root, dirs, files in os.walk(direc):
		for names in files:
			if names.endswith(('.json', '.json')):
				with open(root + "/" + names) as f:
					data = json.load(f)
					attac = data['attackers']
					vict = data['victim']
					if 'alliance_id' in vict.keys():
						idalli = str(vict['alliance_id'])
					else:
						idalli = None

					for alli in attac:
						if 'alliance_id' in alli.keys():
							i = str(alli['alliance_id'])

						else:
							i = None
						if i == allia_id or idalli == allia_id:

							if 'character_id' in vict.keys():
								vic_char_id = vict['character_id']
							else:
								vic_char_id = None
							vic_char_corp = vict['corporation_id']
							if 'alliance_id' in vict.keys():
								vic_char_alli = vict['alliance_id']
							else:
								vic_char_alli = None
							vic_char_ship = vict['ship_type_id']
							idkill = data['killmail_id']
							datekill = data['killmail_time']
							systemid = data['solar_system_id']
							hashkill = data['killmail_hash']

							for t in attac:
								tr = t['final_blow']
								if tr == False:
									continue
								else:
									if 'character_id' in t.keys():
										att_char_id = t['character_id']
									else:
										att_char_id = None
									if 'corporation_id' in t.keys():
										att_char_corp = t['corporation_id']
									else:
										att_char_corp = None
									if 'alliance_id' in t.keys():
										att_char_alli = t['alliance_id']
									else:
										att_char_alli = None
									att_char_ship = t['ship_type_id']
							default_for_update = {'idkill': idkill, 'date_kill': datekill, 'json_file': data, 'solar_system': systemid
							                      , 'hash_kill': hashkill, 'attack_final_personage_id': att_char_id,
							                       'attack_final_personage_corp': att_char_corp, 'attack_final_personage_all': att_char_alli,
							                      'attack_final_personage_ship': att_char_ship, 'victim_personage_id': vic_char_id,
							                      'victim_personage_corp': vic_char_corp, 'victim_personage_all': vic_char_alli,
							                      'victim_personage_ship': vic_char_ship}
							KillFromCCP.objects.update_or_create(idkill=idkill, defaults=default_for_update)

						else:
							continue

	return direc

