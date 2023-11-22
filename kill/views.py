from django.core.paginator import Paginator

from django.conf import settings
from django.shortcuts import render, redirect

from . import tools, parserkillmail
from .models import AllianceStatic, KillGroup, CharacterActive, ActiveCorp, KillFromCCP, Kills, Fitting, HighSlot, \
	MidSlot, LowSlot, RigSlot, SubSlot, HiSlotAmmo, MidSlotAmmo, LowSlotAmmo, Get_Item, Get_Attac


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

	kill_list = Kills.objects.all().filter(npc=False).order_by('date_kill').exclude(victim_personage_ship_type='Capsule').exclude(victim_personage_ship_type='Shuttle')
	killlist_all = Paginator(kill_list,20)
	page_number = request.GET.get('page')
	killlist = killlist_all.get_page(page_number)

	return render(request, 'index.html', {'staticalli': staticalli, 'killgr': killgr,'kill1': kill1,'kill2': kill2,
	                                       'top_15_corp': top_15_corp, 'top_15_chars': top_15_chars, 'killlist': killlist})


def parser_kill_id(request, id_alli=settings.ID_ALLIANCE):
	#tools.alli_kills_state(request, id_alli)
	#st = tools.alli_state(request, id_alli)
	#tools.kill_groups(st,id_alli)
	#tools.Active_Pvp(st,id_alli)
	#tools.DownloadFile()
	#tools.GetRelate()
	#tools.CikleKillAlliance()
	#parserkillmail.ParserKill()
	#tools.Fittings()
	#tools.Get_Count_Slot()
	tools.Attackers()
	return redirect('index')

def ShowKill(request, idkill):
	kill = Kills.objects.all().filter(killmailID=idkill)
	kid = ''
	fid = ''
	for i in kill:
		kid = i.id
	count_slot = Fitting.objects.all().filter(kill_id=kid)
	for s in count_slot:
		fid = s.id
	hi_slot = HighSlot.objects.all().filter(fit_h_id=fid)
	mid_slot = MidSlot.objects.all().filter(fit_m_id=fid)
	low_slot = LowSlot.objects.all().filter(fit_l_id=fid)
	rig_slot = RigSlot.objects.all().filter(fit_r_id=fid)
	sub_slot = SubSlot.objects.all().filter(fit_s_id=fid)
	hi_slot_amo = HiSlotAmmo.objects.all().filter(hi_slot_id=fid)
	med_slot_amo = MidSlotAmmo.objects.all().filter(mid_slot_id=fid)
	low_slot_amo = LowSlotAmmo.objects.all().filter(low_slot_id=fid)
	item = Get_Item.objects.all().filter(killmail_id=kid)
	attack = Get_Attac.objects.all().filter(killmail_id=kid)
	context = {'kill':kill, 'count_slot':count_slot,
		                                    'sub_slot':sub_slot, 'rig_slot':rig_slot, 'low_slot':low_slot,
			                                    'hi_slot':hi_slot, 'mid_slot':mid_slot, 'hi_slot_amo':hi_slot_amo,
	           'med_slot_amo':med_slot_amo, 'low_slot_amo':low_slot_amo, 'item':item, 'attack':attack,}
	return render(request,'kill.html', context)
