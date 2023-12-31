# Generated by Django 3.2.15 on 2023-11-22 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kill', '0004_get_attac_faction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='get_attac',
            name='alliance_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='get_attac',
            name='character_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='get_attac',
            name='corporation_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='get_attac',
            name='ship_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='get_attac',
            name='weapon_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
