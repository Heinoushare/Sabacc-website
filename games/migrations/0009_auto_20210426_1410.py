# Generated by Django 3.1.5 on 2021-04-26 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0008_auto_20210426_1355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='pin',
        ),
        migrations.RemoveField(
            model_name='game',
            name='player2_bet',
        ),
    ]
