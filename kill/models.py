from django.db import models

class AllianceStatic(models.Model):
	count_corp = models.IntegerField(blank=True, null=True)
	count_active_corp = models.IntegerField(blank=True, null=True)
	ships_destroyer = models.IntegerField(blank=True, null=True)
	ships_lost = models.IntegerField(blank=True, null=True)
	point_lost = models.IntegerField(blank=True, null=True)
	point_destroyer = models.IntegerField(blank=True, null=True)
	isk_lost = models.CharField(max_length=255, blank=True, null=True)
	isk_destroyer = models.CharField(max_length=255, blank=True, null=True)
	count_active_chars = models.IntegerField(blank=True, null=True)
	date_created = models.DateTimeField(auto_now_add=True,  null=True, )
	alli_id = models.IntegerField(blank=True, null=True)
	date_founded_alli = models.CharField(max_length=255, blank=True, null=True)



	def __str__(self):
		return str(self.alli_id)


class KillGroup(models.Model):
	id_group = models.IntegerField(blank=True, null=True)
	name = models.CharField(max_length=255, null=True, blank=True)
	ship_kills = models.IntegerField(blank=True, null=True, default=0)
	ship_loss = models.IntegerField(blank=True, null=True, default=0)
	pvp = models.BooleanField(default=True, verbose_name='шип игрока')
	id_alli = models.ForeignKey(AllianceStatic, null=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.id_group


class ActiveCorp(models.Model):
	corp_id = models.CharField(max_length=15, null=True, blank=True)
	corp_name = models.CharField(max_length=255, null=True, blank=True)
	corp_kills = models.IntegerField(null=True, blank=True)
	id_alli = models.ForeignKey(AllianceStatic, null=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.corp_id


class CharacterActive(models.Model):
	char_id = models.CharField(max_length=15, blank=True, null=True)
	char_name = models.CharField(max_length=255, blank=True, null=True)
	char_kills = models.IntegerField(null=True, blank=True)
	id_alli = models.ForeignKey(AllianceStatic, null=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.char_id


class Kills(models.Model):
	killmailID = models.CharField(max_length=255, blank=True, null=True)
	locationID = models.CharField(max_length=20, blank=True, null=True)
	hash_kill = models.CharField(max_length=255, blank=True, null=True)
	fittedValue = models.CharField(max_length=255, blank=True, null=True)
	droppedValue = models.CharField(max_length=255, blank=True, null=True)
	destroyedValue = models.CharField(max_length=255, blank=True, null=True)
	totalValue = models.CharField(max_length=255, blank=True, null=True)
	points = models.CharField(max_length=255, blank=True, null=True)
	npc = models.BooleanField(default=False)
	solo = models.BooleanField(default=False)
	awox = models.BooleanField(default=False)
	id_alli = models.ForeignKey(AllianceStatic, null=True, on_delete=models.CASCADE)
	json_kill = models.JSONField(blank=True, null=True)
	attack_final_personage_name = models.CharField(max_length=255, blank=True, null=True)
	attack_final_personage_corp_name = models.CharField(max_length=255, blank=True, null=True)
	attack_final_personage_corp_icon = models.URLField(null=True, verbose_name='', blank=True)
	attack_final_personage_all_name = models.CharField(max_length=255, blank=True, null=True)
	attack_final_personage_all_icon = models.URLField(null=True, verbose_name='', blank=True)
	attack_final_personage_ship_id = models.URLField(null=True, verbose_name='', blank=True)
	victim_personage_name = models.CharField(max_length=255, blank=True, null=True)
	victim_personage_portrait = models.URLField(blank=True)
	victim_personage_corp_name = models.CharField(max_length=255, blank=True, null=True)
	victim_personage_corp_icon = models.URLField(null=True, verbose_name='', blank=True)
	victim_personage_all_name = models.CharField(max_length=255, blank=True, null=True)
	victim_personage_all_icon = models.URLField(null=True, verbose_name='', blank=True)
	victim_personage_ship_name = models.CharField(max_length=255, blank=True, null=True)
	victim_personage_ship_type = models.CharField(max_length=255, blank=True, null=True)

	victim_personage_ship_group_id = models.CharField(max_length=255, blank=True, null=True)
	victim_personage_ship_id = models.CharField(max_length=255, blank=True, null=True)
	solar_system_name = models.CharField(max_length=255, blank=True, null=True)
	solar_system_ss = models.CharField(max_length=5, blank=True, null=True)
	region_name = models.CharField(max_length=255, blank=True, null=True)
	date_kill = models.CharField(max_length=255, blank=True, null=True)
	loss = models.BooleanField(default=False)

	def __str__(self):
		return str(self.killmailID)


class KillFromCCP(models.Model):
	idkill = models.CharField(max_length=255, blank=True, null=True)
	date_kill = models.CharField(max_length=255, blank=True, null=True)
	json_file = models.JSONField(blank=True, null=True)
	solar_system = models.CharField(max_length=255, blank=True, null=True)
	solar_system_name = models.CharField(max_length=255, blank=True, null=True)
	solar_system_ss = models.CharField(max_length=5, blank=True, null=True)
	hash_kill = models.CharField(max_length=255, blank=True, null=True)
	attack_final = models.CharField(max_length=255, blank=True, null=True)
	attack_final_personage_id = models.CharField(max_length=255, blank=True, null=True)
	attack_final_personage_name = models.CharField(max_length=255, blank=True, null=True)
	attack_final_personage_corp = models.CharField(max_length=255, blank=True, null=True)
	attack_final_personage_corp_name = models.CharField(max_length=255, blank=True, null=True)
	attack_final_personage_corp_icon = models.URLField(null=True, verbose_name='', blank=True)
	attack_final_personage_all = models.CharField(max_length=255, blank=True, null=True)
	attack_final_personage_all_name = models.CharField(max_length=255, blank=True, null=True)
	attack_final_personage_all_icon = models.URLField(null=True, verbose_name='', blank=True)
	attack_final_personage_ship = models.CharField(max_length=255, blank=True, null=True)
	victim_personage_id = models.CharField(max_length=255, blank=True, null=True)
	victim_personage_name = models.CharField(max_length=255, blank=True, null=True)
	victim_personage_corp = models.CharField(max_length=255, blank=True, null=True)
	victim_personage_corp_name = models.CharField(max_length=255, blank=True, null=True)
	victim_personage_corp_icon = models.URLField(null=True, verbose_name='', blank=True)
	victim_personage_all = models.CharField(max_length=255, blank=True, null=True)
	victim_personage_all_name = models.CharField(max_length=255, blank=True, null=True)
	victim_personage_all_icon = models.URLField(null=True, verbose_name='', blank=True)
	victim_personage_ship = models.CharField(max_length=255, blank=True, null=True)



	def  __str__(self):
		return self.idkill


class Fitting(models.Model):
	count_hi_slot = models.CharField(max_length=2, blank=True)
	count_mid_slot = models.CharField(max_length=2, blank=True)
	count_low_slot = models.CharField(max_length=2, blank=True)
	count_rig_slot = models.CharField(max_length=2, blank=True)
	count_sub_slot = models.CharField(max_length=2, blank=True)
	count_hi_slot_real = models.CharField(max_length=2, blank=True)
	count_mid_slot_real = models.CharField(max_length=2, blank=True)
	count_low_slot_real = models.CharField(max_length=2, blank=True)
	count_rig_slot_real = models.CharField(max_length=2, blank=True)
	count_sub_slot_real = models.CharField(max_length=2, blank=True)
	kill = models.ForeignKey(Kills, null=True, on_delete=models.CASCADE)

class HighSlot(models.Model):
	HiSlot0 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	HiSlot1 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	HiSlot2 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	HiSlot3 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	HiSlot4 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	HiSlot5 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	HiSlot6 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	HiSlot7 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	fit_h = models.ForeignKey(Fitting,null=True, on_delete=models.CASCADE)


class MidSlot(models.Model):
	MedSlot0 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	MedSlot1 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	MedSlot2 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	MedSlot3 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	MedSlot4 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	MedSlot5 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	MedSlot6 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	MedSlot7 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	fit_m = models.ForeignKey(Fitting,null=True, on_delete=models.CASCADE)



class LowSlot(models.Model):
	loSlot0 = models.CharField(max_length=20,null=True, verbose_name='', blank=True)
	loSlot1 = models.CharField(max_length=20,null=True, verbose_name='', blank=True)
	loSlot2 = models.CharField(max_length=20,null=True, verbose_name='', blank=True)
	loSlot3 = models.CharField(max_length=20,null=True, verbose_name='', blank=True)
	loSlot4 = models.CharField(max_length=20,null=True, verbose_name='', blank=True)
	loSlot5 = models.CharField(max_length=20,null=True, verbose_name='', blank=True)
	loSlot6 = models.CharField(max_length=20,null=True, verbose_name='', blank=True)
	loSlot7 = models.CharField(max_length=20,null=True, verbose_name='', blank=True)
	fit_l = models.ForeignKey(Fitting,null=True, on_delete=models.CASCADE)


	def __str__(self):
		return str(self.id)


class RigSlot(models.Model):
	RigSlot1 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	RigSlot2 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	RigSlot3 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	fit_r = models.ForeignKey(Fitting,null=True, on_delete=models.CASCADE)


class SubSlot(models.Model):
	SubSystem1 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	SubSystem2 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	SubSystem3 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	SubSystem4 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	SubSystem5 = models.CharField(max_length=255,null=True, verbose_name='', blank=True)
	fit_s = models.ForeignKey(Fitting, null=True, on_delete=models.CASCADE)

class LowSlotAmmo(models.Model):
	loSlot0_ammo = models.CharField(max_length=20, null=True, verbose_name='', blank=True)
	loSlot1_ammo = models.CharField(max_length=20, null=True, verbose_name='', blank=True)
	loSlot2_ammo = models.CharField(max_length=20, null=True, verbose_name='', blank=True)
	loSlot3_ammo = models.CharField(max_length=20, null=True, verbose_name='', blank=True)
	loSlot4_ammo = models.CharField(max_length=20, null=True, verbose_name='', blank=True)
	loSlot5_ammo = models.CharField(max_length=20, null=True, verbose_name='', blank=True)
	loSlot6_ammo = models.CharField(max_length=20, null=True, verbose_name='', blank=True)
	loSlot7_ammo = models.CharField(max_length=20, null=True, verbose_name='', blank=True)
	low_slot = models.ForeignKey(Fitting, null=True, on_delete=models.CASCADE)

class MidSlotAmmo(models.Model):
	MedSlot0_ammo = models.CharField(max_length=255, null=True, verbose_name='', blank=True)
	MedSlot1_ammo = models.CharField(max_length=255, null=True, verbose_name='', blank=True)
	MedSlot2_ammo = models.CharField(max_length=255, null=True, verbose_name='', blank=True)
	MedSlot3_ammo = models.CharField(max_length=255, null=True, verbose_name='', blank=True)
	MedSlot4_ammo = models.CharField(max_length=255, null=True, verbose_name='', blank=True)
	MedSlot5_ammo = models.CharField(max_length=255, null=True, verbose_name='', blank=True)
	MedSlot6_ammo = models.CharField(max_length=255, null=True, verbose_name='', blank=True)
	MedSlot7_ammo = models.CharField(max_length=255, null=True, verbose_name='', blank=True)
	mid_slot = models.ForeignKey(Fitting, null=True, on_delete=models.CASCADE)


class HiSlotAmmo(models.Model):
	HiSlot0_ammo = models.CharField(max_length=255, null=True, verbose_name='', blank=True)
	HiSlot1_ammo = models.CharField(max_length=255, null=True, verbose_name='', blank=True)
	HiSlot2_ammo = models.CharField(max_length=255, null=True, verbose_name='', blank=True)
	HiSlot3_ammo = models.CharField(max_length=255, null=True, verbose_name='', blank=True)
	HiSlot4_ammo = models.CharField(max_length=255, null=True, verbose_name='', blank=True)
	HiSlot5_ammo = models.CharField(max_length=255, null=True, verbose_name='', blank=True)
	HiSlot6_ammo = models.CharField(max_length=255, null=True, verbose_name='', blank=True)
	HiSlot7_ammo = models.CharField(max_length=255, null=True, verbose_name='', blank=True)
	hi_slot = models.ForeignKey(Fitting, null=True, on_delete=models.CASCADE)

class Get_Attac(models.Model):
	alliance_id = models.CharField(max_length=255, blank=True, null=True)
	alliance_name = models.CharField(max_length=255,blank=True, null=True)
	character_id = models.CharField(max_length=255, blank=True, null=True)
	character_name = models.CharField(max_length=255, blank=True, null=True)
	faction_id = models.CharField(max_length=255, blank=True, null=True)
	corporation_id = models.CharField(max_length=255, blank=True, null=True)
	corporation_name = models.CharField(max_length=255, blank=True, null=True)
	damage_done = models.CharField(max_length=255, blank=True, null=True)
	final_blow = models.BooleanField(default=False)
	security_status = models.CharField(max_length=255, blank=True, null=True)
	ship_type_id = models.CharField(max_length=255, blank=True, null=True)
	ship_name = models.CharField(max_length=255, blank=True, null=True)
	weapon_type_id = models.CharField(max_length=255, blank=True, null=True)
	weapon_name = models.CharField(max_length=255, blank=True, null=True)
	killmail = models.ForeignKey(Kills, null=True, on_delete=models.CASCADE)

class Get_Item(models.Model):
	item_id = models.CharField(max_length=255, blank=True, null=True)
	item_cont = models.CharField(max_length=255, blank=True, null=True)
	item_name = models.CharField(max_length=255, blank=True, null=True)
	hi_slot = models.BooleanField(default=False)
	mi_slot = models.BooleanField(default=False)
	lo_slot = models.BooleanField(default=False)
	rig_slot = models.BooleanField(default=False)
	sub_slot = models.BooleanField(default=False)
	cargo_slot = models.BooleanField(default=False)
	drone_slot = models.BooleanField(default=False)
	item_destroy = models.BooleanField(default=False)
	item_droped = models.BooleanField(default=False)
	killmail = models.ForeignKey(Kills, null=True, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.item_id)
