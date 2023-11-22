import datetime
import json

import os
import tarfile

from retry import retry

import requests

from board import settings
from kill import  parserkillmail
from kill.models import (KillGroup, AllianceStatic, ActiveCorp, CharacterActive, Kills, KillFromCCP,
                         Fitting, HighSlot, MidSlot, LowSlot, RigSlot, SubSlot, LowSlotAmmo, HiSlotAmmo, MidSlotAmmo,
                         Get_Item, Get_Attac)
import time
from dateutil.relativedelta import relativedelta


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
	current_date = datetime.datetime.now()


	all_kills = AllianceStatic.objects.all().filter(alli_id=id_alliance)
	f = AllianceStatic.objects.get(alli_id=id_alliance)


	time_date = str(current_date)
	date_found_alli = ''
	fondaunt_date = (datetime.datetime(2023, 7, 16))
	while str(date_found_alli)[:7] <= time_date[:7]:

		date_found_alli = fondaunt_date

		len_page = 1
		len_data = ''
		fondaunt_date += relativedelta(months=1)
		fond_yar = str(date_found_alli)[:4]
		fond_mont = str(date_found_alli)[5:7]
		while len_data != 0:

			ur = ('https://zkillboard.com/api/allianceID/{}/year/{}/month/{}/page/{}/'.format(id_alliance, fond_yar, fond_mont, len_page))
			time.sleep(1)
			resultat = requests.get(ur)
			resultat.raise_for_status()
			data = resultat.json()
			len_data = len(data)
			len_page += 1

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
				Kills.objects.update_or_create(killmailID=kill_id, defaults=default_for_update)

	parserkillmail.ParserKill()
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

	while fondaunt_date < current_date:

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
								vic_char_name = GetName(vic_char_id)
							else:
								vic_char_id = None
							vic_char_corp = vict['corporation_id']
							vic_char_corp_name = GetName(vic_char_corp)
							vic_char_corp_icon = Corporation_Icon(vic_char_corp)
							if 'alliance_id' in vict.keys():
								vic_char_alli = vict['alliance_id']
								vic_char_alli_name = GetName(vic_char_alli)
								vic_char_alli_icon = Alliance_Icon(vic_char_alli)

							else:
								vic_char_alli = None
							vic_char_ship = vict['ship_type_id']
							idkill = data['killmail_id']
							datekill = data['killmail_time']
							systemid = data['solar_system_id']
							system_info = System_Info(systemid)
							systen_name = system_info[0]
							system_ss = system_info[1]
							hashkill = data['killmail_hash']

							for t in attac:
								tr = t['final_blow']
								if tr == False:
									continue
								else:
									if 'character_id' in t.keys():
										att_char_id = t['character_id']
										att_char_name = GetName(att_char_id)
									else:
										att_char_id = None
									if 'corporation_id' in t.keys():
										att_char_corp = t['corporation_id']
										att_char_corp_name = GetName(att_char_corp)
										att_char_corp_icon = Corporation_Icon(att_char_corp)
									else:
										att_char_corp = None
									if 'alliance_id' in t.keys():
										att_char_alli = t['alliance_id']
										att_char_alli_name = GetName(att_char_alli)
										att_char_alli_icon = Alliance_Icon(att_char_alli)
									else:
										att_char_alli = None
									att_char_ship = t['ship_type_id']

							default_for_update = {'idkill': idkill,
							                      'date_kill': datekill,
							                      'json_file': data,
							                      'solar_system': systemid,
							                      'hash_kill': hashkill,
							                      'attack_final_personage_id': att_char_id,
							                      'attack_final_personage_name': att_char_name,
							                      'attack_final_personage_corp': att_char_corp,
							                      'attack_final_personage_corp_name': att_char_corp_name,
							                      'attack_final_personage_corp_icon': att_char_corp_icon,
							                      'attack_final_personage_all': att_char_alli,
							                      'attack_final_personage_all_name': att_char_alli_name,
							                      'attack_final_personage_all_icon': att_char_alli_icon,
							                      'attack_final_personage_ship': att_char_ship,
							                      'victim_personage_id': vic_char_id,
							                      'victim_personage_name': vic_char_name,
							                      'victim_personage_corp': vic_char_corp,
							                      'victim_personage_corp_name': vic_char_corp_name,
							                      'victim_personage_corp_icon': vic_char_corp_icon,
							                      'victim_personage_all': vic_char_alli,
							                      'victim_personage_all_name': vic_char_alli_name,
							                      'victim_personage_all_icon': vic_char_alli_icon,
							                      'victim_personage_ship': vic_char_ship,
							                      'solar_system_name': systen_name,
							                      'solar_system_ss': system_ss,}
							KillFromCCP.objects.update_or_create(idkill=idkill, defaults=default_for_update)

						else:
							continue

	return direc

def Personage_Get_Icon(data_in):
	icon = 'https://images.evetech.net/characters/{}/portrait?tenant=tranquility&size=64'.format(data_in)
	return icon


def Corporation_Icon(data_in):
	ur = "https://images.evetech.net/corporations/{}/logo?tenant=tranquility&size=64".format(data_in)
	return ur


def Alliance_Icon(data_in):
	ur = "https://images.evetech.net/Alliance/{}_64.png".format(data_in)
	return ur


@retry(tries=3, delay=1,)
def Get_GroupID_Type(type):
	ul = 'https://esi.evetech.net/latest/universe/types/{}/?datasource=tranquility&language=en'.format(type)
	res = requests.get(ul)
	res.raise_for_status()
	type_out = res.json()
	ur = 'https://esi.evetech.net/latest/universe/groups/{}/?datasource=tranquility&language=en'.format(type_out['group_id'])
	r = requests.get(ur)
	r.raise_for_status()
	type_name = r.json()
	return type_name['name'], type_out['group_id']

@retry(tries=3, delay=1,)
def System_Info(data_in):
	ur = 'https://esi.evetech.net/latest/universe/systems/{}/?datasource=tranquility&language=en'.format(data_in)
	resultat = requests.get(ur)
	resultat.raise_for_status()
	data = resultat.json()
	name = data['name']
	sec = data['security_status']
	ss = round(sec,1)
	constallation_id = data['constellation_id']
	ur_constel= 'https://esi.evetech.net/latest/universe/constellations/{}/?datasource=tranquility&language=en'.format(constallation_id)
	res =requests.get(ur_constel)
	res.raise_for_status()
	data_region = res.json()
	id_reg = data_region['region_id']
	ur_region = 'https://esi.evetech.net/latest/universe/regions/{}/?datasource=tranquility&language=en'.format(id_reg)
	resul = requests.get(ur_region)
	resul.raise_for_status()
	dat = resul.json()
	reg_name = dat['name']
	return name, ss, reg_name

@retry(tries=3, delay=1,)
def Request_To_CCP(id_kill, hash_kill):
	ur = 'https://esi.evetech.net/latest/killmails/{}/{}/?datasource=tranquility'.format(id_kill,
	                                                                                     hash_kill)
	resultat = requests.get(ur)
	resultat.raise_for_status()
	data = resultat.json()
	return data

@retry(tries=3, delay=1,)
def GetName(id_type):
	l = [id_type]
	ur = requests.post('https://esi.evetech.net/latest/universe/names/?datasource=tranquility',data=json.dumps(l))
	resultat = ur.json()

	a = resultat[0]['name']

	return a

def Fittings(alliance_id = settings.ID_ALLIANCE):
	global m
	stat = AllianceStatic.objects.get(alli_id=alliance_id)
	kill_file = Kills.objects.all().filter(id_alli_id=stat)
	for l in kill_file:
		json_kill = l.json_kill

		victim = json_kill['victim']
		ship_id = victim['ship_type_id']
		type = Get_Types(ship_id)
		dogma = type['dogma_attributes']
		items = victim['items']
		km = l.id
		fitid = ''

		default_low = {}
		default_mid = {}
		default_hi = {}
		default_rig = {}
		default_sub = {}
		default_low_amo = {}
		default_hi_amo = {}
		default_mid_amo = {}

		if len(items) != 0:
			deff = {}
			for s in dogma:
				if s['attribute_id'] == 12:
					deff['count_low_slot'] = int(s['value'])
				if s['attribute_id'] == 13:
					deff['count_mid_slot'] = int(s['value'])
				if s['attribute_id'] == 14:
					deff['count_hi_slot'] = int(s['value'])
				if s['attribute_id'] == 1137:
					deff['count_rig_slot'] = int(s['value'])
				if s['attribute_id'] == 1367:
					deff['count_sub_slot'] = int(s['value'])
				Fitting.objects.update_or_create(kill_id=km, defaults=deff)
				fitid = Fitting.objects.get(kill_id=km)


			for i in items:

					if i['flag'] == 11:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_low_amo['loSlot0_ammo'] = i['item_type_id']
							else:
								default_low['loSlot0'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_low_amo['loSlot0_ammo'] = i['item_type_id']
							else:
								default_low['loSlot0'] = i['item_type_id']
					if i['flag'] == 12:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_low_amo['loSlot1_ammo'] = i['item_type_id']
							else:
								default_low['loSlot1'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_low_amo['loSlot1_ammo'] = i['item_type_id']
							else:
								default_low['loSlot1'] = i['item_type_id']
					if i['flag'] == 13:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_low_amo['loSlot2_ammo'] = i['item_type_id']
							else:
								default_low['loSlot2'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_low_amo['loSlot2_ammo'] = i['item_type_id']
							else:
								default_low['loSlot2'] = i['item_type_id']
					if i['flag'] == 14:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_low_amo['loSlot3_ammo'] = i['item_type_id']
							else:
								default_low['loSlot3'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_low_amo['loSlot3_ammo'] = i['item_type_id']
							else:
								default_low['loSlot3'] = i['item_type_id']
					if i['flag'] == 15:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_low_amo['loSlot4_ammo'] = i['item_type_id']
							else:
								default_low['loSlot4'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_low_amo['loSlot4_ammo'] = i['item_type_id']
							else:
								default_low['loSlot4'] = i['item_type_id']
					if i['flag'] == 16:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_low_amo['loSlot5_ammo'] = i['item_type_id']
							else:
								default_low['loSlot5'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_low_amo['loSlot5_ammo'] = i['item_type_id']
							else:
								default_low['loSlot5'] = i['item_type_id']
					if i['flag'] == 17:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_low_amo['loSlot6_ammo'] = i['item_type_id']
							else:
								default_low['loSlot6'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_low_amo['loSlot6_ammo'] = i['item_type_id']
							else:
								default_low['loSlot6'] = i['item_type_id']
					if i['flag'] == 18:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_low_amo['loSlot7_ammo'] = i['item_type_id']
							else:
								default_low['loSlot7'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_low_amo['loSlot7_ammo'] = i['item_type_id']
							else:
								default_low['loSlot7'] = i['item_type_id']

					if i['flag'] == 19:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_mid_amo['MedSlot0_ammo'] = i['item_type_id']
							else:
								default_mid['MedSlot0'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_mid_amo['MedSlot0_ammo'] = i['item_type_id']
							else:
								default_mid['MedSlot0'] = i['item_type_id']
					if i['flag'] == 20:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_mid_amo['MedSlot1_ammo'] = i['item_type_id']
							else:
								default_mid['MedSlot1'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_mid_amo['MedSlot1_ammo'] = i['item_type_id']
							else:
								default_mid['MedSlot1'] = i['item_type_id']
					if i['flag'] == 21:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_mid_amo['MedSlot2_ammo'] = i['item_type_id']
							else:
								default_mid['MedSlot2'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_mid_amo['MedSlot2_ammo'] = i['item_type_id']
							else:
								default_mid['MedSlot2'] = i['item_type_id']
					if i['flag'] == 22:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_mid_amo['MedSlot3_ammo'] = i['item_type_id']
							else:
								default_mid['MedSlot3'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_mid_amo['MedSlot3_ammo'] = i['item_type_id']
							else:
								default_mid['MedSlot3'] = i['item_type_id']
					if i['flag'] == 23:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_mid_amo['MedSlot4_ammo'] = i['item_type_id']
							else:
								default_mid['MedSlot4'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_mid_amo['MedSlot4_ammo'] = i['item_type_id']
							else:
								default_mid['MedSlot4'] = i['item_type_id']
					if i['flag'] == 24:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_mid_amo['MedSlot5_ammo'] = i['item_type_id']
							else:
								default_mid['MedSlot5'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_mid_amo['MedSlot5_ammo'] = i['item_type_id']
							else:
								default_mid['MedSlot5'] = i['item_type_id']
					if i['flag'] == 25:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_mid_amo['MedSlot6_ammo'] = i['item_type_id']
							else:
								default_mid['MedSlot6'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_mid_amo['MedSlot6_ammo'] = i['item_type_id']
							else:
								default_mid['MedSlot6'] = i['item_type_id']
					if i['flag'] == 26:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_mid_amo['MedSlot7_ammo'] = i['item_type_id']
							else:
								default_mid['MedSlot7'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_mid_amo['MedSlot7_ammo'] = i['item_type_id']
							else:
								default_mid['MedSlot7'] = i['item_type_id']

					if i['flag'] == 27:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_hi_amo['HiSlot0_ammo'] = i['item_type_id']
							else:
								default_hi['HiSlot0'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_hi_amo['HiSlot0_ammo'] = i['item_type_id']
							else:
								default_hi['HiSlot1'] = i['item_type_id']
					if i['flag'] == 28:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_hi_amo['HiSlot1_ammo'] = i['item_type_id']
							else:
								default_hi['HiSlot1'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_hi_amo['HiSlot1_ammo'] = i['item_type_id']
							else:
								default_hi['HiSlot1'] = i['item_type_id']
					if i['flag'] == 29:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_hi_amo['HiSlot2_ammo'] = i['item_type_id']
							else:
								default_hi['HiSlot2'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_hi_amo['HiSlot2_ammo'] = i['item_type_id']
							else:
								default_hi['HiSlot2'] = i['item_type_id']
					if i['flag'] == 30:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_hi_amo['HiSlot3_ammo'] = i['item_type_id']
							else:
								default_hi['HiSlot3'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_hi_amo['HiSlot3_ammo'] = i['item_type_id']
							else:
								default_hi['HiSlot3'] = i['item_type_id']
					if i['flag'] == 31:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_hi_amo['HiSlot4_ammo'] = i['item_type_id']
							else:
								default_hi['HiSlot4'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_hi_amo['HiSlot4_ammo'] = i['item_type_id']
							else:
								default_hi['HiSlot4'] = i['item_type_id']
					if i['flag'] == 32:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_hi_amo['HiSlot5_ammo'] = i['item_type_id']
							else:
								default_hi['HiSlot5'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_hi_amo['HiSlot5_ammo'] = i['item_type_id']
							else:
								default_hi['HiSlot5'] = i['item_type_id']
					if i['flag'] == 33:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_hi_amo['HiSlot6_ammo'] = i['item_type_id']
							else:
								default_hi['HiSlot6'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_hi_amo['HiSlot6_ammo'] = i['item_type_id']
							else:
								default_hi['HiSlot6'] = i['item_type_id']
					if i['flag'] == 34:
						if 'quantity_dropped' in i:
							if i['quantity_dropped'] != 1:
								default_hi_amo['HiSlot7_ammo'] = i['item_type_id']
							else:
								default_hi['HiSlot7'] = i['item_type_id']
						if 'quantity_destroyed' in i:
							if i['quantity_destroyed'] != 1:
								default_hi_amo['HiSlot7_ammo'] = i['item_type_id']
							else:
								default_hi['HiSlot7'] = i['item_type_id']

					if i['flag'] == 92:
						default_rig['RigSlot1'] = i['item_type_id']
					if i['flag'] == 93:
						default_rig['RigSlot2'] = i['item_type_id']
					if i['flag'] == 94:
						default_rig['RigSlot3'] = i['item_type_id']

					if i['flag'] == 125:
						default_sub['SubSystem1'] = i['item_type_id']
					if i['flag'] == 126:
						default_sub['SubSystem2'] = i['item_type_id']
					if i['flag'] == 127:
						default_sub['SubSystem3'] = i['item_type_id']
					if i['flag'] == 128:
						default_sub['SubSystem4'] = i['item_type_id']
					if i['flag'] == 129:
						default_sub['SubSystem5'] = i['item_type_id']
			def_real_slots = {'count_hi_slot_real':len(default_hi), 'count_mid_slot_real':len(default_mid),
			                  'count_low_slot_real':len(default_low), 'count_rig_slot_real':len(default_rig),
			                  'count_sub_slot_real':len(default_sub)}
			if not default_rig:
				RigSlot.objects.create(fit_r_id=fitid.id)
			else:
				RigSlot.objects.update_or_create(fit_r_id=fitid.id, defaults=default_rig)

			if not default_hi:
				HighSlot.objects.create(fit_h_id=fitid.id)
			else:
				HighSlot.objects.update_or_create(fit_h_id=fitid.id, defaults=default_hi)
			if not default_hi_amo:
				HiSlotAmmo.objects.create(hi_slot_id=fitid.id)
			else:
				HiSlotAmmo.objects.update_or_create(hi_slot_id=fitid.id, defaults=default_hi_amo)

			if not default_mid:
				MidSlot.objects.create(fit_m_id=fitid.id)
			else:
				MidSlot.objects.update_or_create(fit_m_id=fitid.id, defaults=default_mid)
			if not default_mid_amo:
				MidSlotAmmo.objects.create(mid_slot_id=fitid.id)
			else:
				MidSlotAmmo.objects.update_or_create(mid_slot_id=fitid.id, defaults=default_mid_amo)

			if not default_low:
				LowSlot.objects.create(fit_l_id=fitid.id)
			else:
				LowSlot.objects.update_or_create(fit_l_id=fitid.id, defaults=default_low)
			if not default_low_amo:
				LowSlotAmmo.objects.create(low_slot_id=fitid.id)
			else:
				LowSlotAmmo.objects.update_or_create(low_slot_id=fitid.id, defaults=default_low_amo)


			if not default_sub:
				SubSlot.objects.create(fit_s_id=fitid.id)
			else:
				SubSlot.objects.update_or_create(fit_s_id=fitid.id, defaults=default_sub)
			Fitting.objects.update_or_create(kill_id=km, defaults=def_real_slots)
		else:
			deff0 = {'count_low_slot': 0, 'count_hi_slot': 0, 'count_mid_slot': 0, 'count_rig_slot': 0,
			         'count_sub_slot': 0, }
			Fitting.objects.update_or_create(kill_id=km, defaults=deff0)

@retry(tries=3, delay=1,)
def Get_Types(data_in):
	ul = 'https://esi.evetech.net/latest/universe/types/{}/?datasource=tranquility&language=en'.format(data_in)
	res = requests.get(ul)
	res.raise_for_status()
	types = res.json()
	return types

'''запускает заполнение модели для потерянного шмота'''
def Get_Items(data_in, kill):
	if len(data_in):
		for it in data_in:

			if it['flag'] == 5:
				if 'quantity_dropped' in it:
					name_item = Get_Items_Name_In_File(it['item_type_id'])
					Get_Item.objects.create(item_id=it['item_type_id'], item_cont=it['quantity_dropped'], cargo_slot=True,
				                        item_droped=True, item_name=name_item, killmail_id=kill)
				elif 'quantity_destroyed' in it:
					name_item = Get_Items_Name_In_File(it['item_type_id'])
					Get_Item.objects.create(item_id=it['item_type_id'], item_cont=it['quantity_destroyed'], cargo_slot=True,
				                        item_destroy=True, item_name=name_item, killmail_id=kill)

			if 11 <= it['flag'] <= 18:
				if 'quantity_dropped' in it:
					name_item = Get_Items_Name_In_File(it['item_type_id'])
					Get_Item.objects.create(item_id=it['item_type_id'], item_cont=it['quantity_dropped'], lo_slot=True,
				                        item_droped=True, item_name=name_item,killmail_id=kill)
				elif 'quantity_destroyed' in it:
					name_item = Get_Items_Name_In_File(it['item_type_id'])
					Get_Item.objects.create(item_id=it['item_type_id'], item_cont=it['quantity_destroyed'], lo_slot=True,
				                        item_destroy=True, item_name=name_item, killmail_id=kill)
			if 19 <= it['flag'] <= 26:
				if 'quantity_dropped' in it:
					name_item = Get_Items_Name_In_File(it['item_type_id'])
					Get_Item.objects.create(item_id=it['item_type_id'], item_cont=it['quantity_dropped'], mi_slot=True,
				                        item_droped=True, item_name=name_item, killmail_id=kill)
				elif 'quantity_destroyed' in it:
					name_item = Get_Items_Name_In_File(it['item_type_id'])
					Get_Item.objects.create(item_id=it['item_type_id'], item_cont=it['quantity_destroyed'], mi_slot=True,
				                        item_destroy=True, item_name=name_item, killmail_id=kill)

			if 27 <= it['flag'] <= 34:
				if 'quantity_dropped' in it:
					name_item = Get_Items_Name_In_File(it['item_type_id'])
					Get_Item.objects.create(item_id=it['item_type_id'], item_cont=it['quantity_dropped'], hi_slot=True,
				                        item_droped=True, item_name=name_item, killmail_id=kill)
				elif 'quantity_destroyed' in it:
					name_item = Get_Items_Name_In_File(it['item_type_id'])
					Get_Item.objects.create(item_id=it['item_type_id'], item_cont=it['quantity_destroyed'], hi_slot=True,
				                        item_destroy=True, item_name=name_item, killmail_id=kill)

			if it['flag'] == 87:
				if 'quantity_dropped' in it:
					name_item = Get_Items_Name_In_File(it['item_type_id'])
					Get_Item.objects.create(item_id=it['item_type_id'], item_cont=it['quantity_dropped'], drone_slot=True,
				                        item_droped=True, item_name=name_item, killmail_id=kill)
				elif 'quantity_destroyed' in it:
					name_item = Get_Items_Name_In_File(it['item_type_id'])
					Get_Item.objects.create(item_id=it['item_type_id'], item_cont=it['quantity_destroyed'], drone_slot=True,
				                        item_destroy=True, item_name=name_item, killmail_id=kill)

			if 92 <= it['flag'] <= 94:
				if 'quantity_dropped' in it:
					name_item = Get_Items_Name_In_File(it['item_type_id'])
					Get_Item.objects.create(item_id=it['item_type_id'], item_cont=it['quantity_dropped'], rig_slot=True,
				                        item_droped=True, item_name=name_item, killmail_id=kill)
				elif 'quantity_destroyed' in it:
					name_item = Get_Items_Name_In_File(it['item_type_id'])
					Get_Item.objects.create(item_id=it['item_type_id'], item_cont=it['quantity_destroyed'], rig_slot=True,
				                        item_destroy=True, item_name=name_item, killmail_id=kill)

			if 125 <= it['flag'] <= 129:
				if 'quantity_dropped' in it:
					name_item = Get_Items_Name_In_File(it['item_type_id'])
					Get_Item.objects.create(item_id=it['item_type_id'], item_cont=it['quantity_dropped'], sub_slot=True,
				                        item_droped=True, item_name=name_item, killmail_id=kill)
				elif 'quantity_destroyed' in it:
					name_item = Get_Items_Name_In_File(it['item_type_id'])
					Get_Item.objects.create(item_id=it['item_type_id'], item_cont=it['quantity_destroyed'], sub_slot=True,
				                        item_destroy=True, item_name=name_item, killmail_id=kill)
	else:
		Get_Item.objects.create(killmail_id=kill)


def Get_Items_Name_In_File(data_in):
	file_name = "D://typeIDs.json"
	with open(file_name, 'r', encoding='utf-8') as f:
		data1 = json.load(f)
		for item in data1:
			if item == str(data_in):
				n = data1[item]
				name = n['name']['en']
				return name

def Attackers(alli_id = settings.ID_ALLIANCE):
	alli = AllianceStatic.objects.get(alli_id=alli_id)
	kills = Kills.objects.all().filter(id_alli_id=alli.id)
	for k in kills:
		js = k.json_kill
		att = js['attackers']

		for it in att:
			if 'alliance_id' in it:
				alli_id = it['alliance_id']
			else:
				alli_id = None
			if 'corporation_id' in it:
				corp_id = it['corporation_id']
			else:
				corp_id = None
			if 'character_id' in it:
				char_id = it['character_id']
			else:
				char_id = None
			if 'faction_id' in it:
				fact_id = it['faction_id']
			else:
				fact_id = None
			if 'weapon_type_id' in it:
				weapon_id = it['weapon_type_id']
			else:
				weapon_id = it['ship_type_id']
			if 'ship_type_id' in it:
				ship_id = it['ship_type_id']
			else:
				ship_id = '670'

			Get_Attac.objects.create(killmail_id=k.id, alliance_id=alli_id, corporation_id=corp_id,
			                         character_id=char_id,damage_done=it['damage_done'],
			                         final_blow=it['final_blow'], security_status=it['security_status'],
			                         ship_type_id=ship_id, weapon_type_id=weapon_id, faction_id=fact_id)
