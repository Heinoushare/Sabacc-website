# Generated by Django 3.1.5 on 2021-04-26 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0010_auto_20210426_1422'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='player1_bet',
            new_name='follow_player_bet',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='player2_bet',
            new_name='lead_player_bet',
        ),
    ]
