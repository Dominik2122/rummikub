# Generated by Django 3.1.4 on 2021-03-17 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20210317_1915'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='last',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.tile'),
        ),
    ]
