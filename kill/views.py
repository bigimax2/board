from django.conf import settings
from django.shortcuts import render, redirect

from . import tools
from .models import AllianceStatic, KillGroup


def index(request):
	staticalli = AllianceStatic.objects.all()
	killgr = KillGroup.objects.all()

	return render(request, 'index.html', {'staticalli': staticalli, 'killgr': killgr})


def parser_kill_id(request, id_alli=settings.ID_ALLIANCE):
	tools.alli_kills_state(request, id_alli)
	st = tools.alli_state(request, id_alli)
	tools.kill_groups(st)
	return redirect('index')
