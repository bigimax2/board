import json
import os

from django.conf import settings
from django.shortcuts import render, redirect

from . import tools
from .models import AllianceStatic, KillGroup, CharacterActive, ActiveCorp, KillFromCCP


def index(request):
	staticalli = AllianceStatic.objects.defer('date_created')

	top_corp = ActiveCorp.objects.all().order_by('-corp_kills')
	top_15_corp = top_corp[:15]

	top_char = CharacterActive.objects.all().order_by('-char_kills')
	top_15_chars = top_char[:15]

	killgr = KillGroup.objects.all().filter(pvp=True)

	a = len(killgr)
	if a % 2 == 0:
		do = int(a / 2 )
	else:
		do = int((a + 1 ) / 2)
	kill1 = killgr[0:do]
	kill2 = killgr[do:a]

	killlist = KillFromCCP.objects.all().order_by('date_kill')
	return render(request, 'index.html', {'staticalli': staticalli, 'killgr': killgr,'kill1': kill1,'kill2': kill2,
	                                       'top_15_corp': top_15_corp, 'top_15_chars': top_15_chars, 'killlist': killlist})


def parser_kill_id(request, id_alli=settings.ID_ALLIANCE):
	#tools.alli_kills_state(request, id_alli)
	#st = tools.alli_state(request, id_alli)
	#tools.kill_groups(st,id_alli)
	#tools.Active_Pvp(st,id_alli)
	#tools.DownloadFile()
	#tools.GetRelate()
	tools.CikleKillAlliance()
	return redirect('index')
