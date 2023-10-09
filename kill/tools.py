import requests


def corp_alli(request, id_alliance):
	ur = ("https://esi.evetech.net/latest/alliances/{}/corporations/?datasource=tranquility".format(id_alliance))
	resultat = requests.get(ur)
	etag = resultat.headers.get('etag')
	resultat.raise_for_status()
	data = resultat.json()
	return data


def alli_state(request, id_alliance):
	ur = ("https://zkillboard.com/api/stats/allianceID/{}/".format(id_alliance))
	resultat = requests.get(ur)
	resultat.raise_for_status()
	data = resultat.json()
	return data