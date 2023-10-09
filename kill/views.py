import requests
from django.conf import settings
from django.shortcuts import render
from . import tools


def index(request, id_alli=settings.ID_ALLIANCE):

	corp_in_alliance = tools.corp_alli(request, id_alli)
	count_corp = len(corp_in_alliance)
	state = tools.alli_state(request, id_alli)

	return render(request, 'index.html', {'count_corp': count_corp})

