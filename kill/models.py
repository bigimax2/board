from django.db import models



class AllianceKillsID(models.Model):
	id_kills = models.IntegerField(default=None, unique=True, blank=True, null=True)

	class Meta:
		verbose_name = 'Килл альянса'
		verbose_name_plural = 'Килы альянса'

	def __str__(self):
		return self.id_kills


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

	def __str__(self):
		return self.count_corp


class KillGroup(models.Model):
	id_group = models.IntegerField(blank=True, null=True)
	name = models.CharField(max_length=255, null=True, blank=True)
	ship_kills = models.IntegerField(blank=True, null=True, default=0)
	ship_loss = models.IntegerField(blank=True, null=True, default=0)
	pvp = models.BooleanField(default=True, verbose_name='шип игрока')
	def __str__(self):
		return self.id_group
