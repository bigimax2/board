import requests

from kill.models import KillGroup, AllianceStatic
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
			i.save()
	else:
		AllianceStatic.objects.create(count_active_corp=act_corp, ships_destroyer=ship_kills, ships_lost=ship_loss,
	                                        point_lost=point_loss, point_destroyer=point_kills, isk_destroyer=isk_destroyed,
	                                        isk_lost=isk_loss, count_active_chars=act_chars, count_corp=cont_corp, alli_id=id_alli)
	return data


def alli_kills_state(request, id_alliance):
	ur = ("https://zkillboard.com/api/kills/allianceID/{}/page/1/".format(id_alliance))
	resultat = requests.get(ur)
	resultat.raise_for_status()
	data = resultat.json()
	return data




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