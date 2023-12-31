# Generated by Django 4.1.7 on 2023-06-02 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('futbik', '0006_alter_players_surname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hit',
            name='lineup',
        ),
        migrations.RemoveField(
            model_name='matches',
            name='teams',
        ),
        migrations.AddField(
            model_name='hit',
            name='club',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='futbik.clubs'),
        ),
        migrations.AddField(
            model_name='hit',
            name='match',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='hit', to='futbik.matches'),
        ),
        migrations.AddField(
            model_name='hit',
            name='player',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='futbik.players'),
        ),
        migrations.AddField(
            model_name='matches',
            name='team1',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='team1', to='futbik.clubs', verbose_name='Команда 1'),
        ),
        migrations.AddField(
            model_name='matches',
            name='team1_score',
            field=models.IntegerField(default=0, verbose_name='Счет первой команды'),
        ),
        migrations.AddField(
            model_name='matches',
            name='team2',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='team2', to='futbik.clubs', verbose_name='Команда 2'),
        ),
        migrations.AddField(
            model_name='matches',
            name='team2_score',
            field=models.IntegerField(default=0, verbose_name='Счет первой команды'),
        ),
        migrations.DeleteModel(
            name='Score',
        ),
    ]
