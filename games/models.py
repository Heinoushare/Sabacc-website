from django.db import models

# Create your models here.

class Game(models.Model):
  pin = models.IntegerField(blank=True, null=True)
  player1 = models.TextField()
  player2 = models.TextField()
  player1_credits = models.IntegerField(default=995)
  lead_player_bet = models.IntegerField(blank=True, null=True)
  follow_player_bet = models.IntegerField(blank=True, null=True)
  player2_credits = models.IntegerField(default=995)
  hand_pot = models.IntegerField(default=0)
  sabacc_pot = models.IntegerField(default=10)
  leading_player = models.TextField()
  active_player = models.TextField()
  phase = models.TextField(default="Betting")
  follow_bet_counter = models.BooleanField(default=False)
  game_started = models.BooleanField(default=False)
  deck = models.TextField(default="1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,11,11,11,11,12,12,12,12,13,13,13,13,14,14,14,14,15,15,15,15,0,0,-2,-2,-8,-8,-11,-11,-13,-13,-14,-14,-15,-15,-17,-17")

  player1_hand = models.TextField(default="")
  player2_hand = models.TextField(default="")


  player1_hand_sum = models.IntegerField(default=0)

  

  player2_hand_sum = models.IntegerField(default=0)

  lead_player_card_action = models.TextField(blank = True, null=True)

  follow_player_card_action = models.TextField(blank = True, null=True)

  lead_player_shift_action = models.TextField(blank = True, null = True)

  follow_player_shift_action = models.TextField(blank = True, null = True)