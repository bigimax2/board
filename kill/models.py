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



	def __str__(self):
		return self.count_corp


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