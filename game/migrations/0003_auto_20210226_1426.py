# Generated by Django 3.1.4 on 2021-02-26 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20210226_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tile',
            name='pos_left',
            field=models.CharField(blank=True, default='', max_length=5),
        ),
        migrations.AlterField(
            model_name='tile',
            name='pos_top',
            field=models.CharField(blank=True, default='', max_length=5),
        ),
    ]
