# Generated by Django 4.1.7 on 2023-05-29 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('futbik', '0004_lineup_is_first_eleven'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineup',
            name='position',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='players',
            name='height',
            field=models.IntegerField(default=-1, null=None, verbose_name='Рост'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='players',
            name='shirtNo',
            field=models.IntegerField(default=-1, null=None, verbose_name='Номер футболки'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='players',
            name='weight',
            field=models.IntegerField(default=-1, null=None, verbose_name='Вес'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='players',
            name='age',
            field=models.IntegerField(null=None, verbose_name='Возраст'),
        ),
    ]
