# Generated by Django 4.1.7 on 2023-06-08 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('futbik', '0007_remove_hit_lineup_remove_matches_teams_hit_club_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hit',
            name='PG',
            field=models.FloatField(default=0.5, verbose_name='predicted goal'),
        ),
        migrations.AlterField(
            model_name='hit',
            name='match',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='hits', to='futbik.matches'),
        ),
    ]