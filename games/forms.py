from .models import Game

from django import forms


class GameForm(forms.ModelForm):
  class Meta:
    model = Game
    fields = [
      'player2'
    ]

class LeadBettingForm(forms.ModelForm):
  class Meta:
    model = Game
    fields = [
      'lead_player_bet'
    ]

class FollowBettingForm(forms.ModelForm):
  class Meta:
    model = Game
    fields = [
      'follow_player_bet'
    ]

class LeadCardForm(forms.ModelForm):
  class Meta:
    model = Game
    fields = [
      'lead_player_card_action'
    ]

class FollowCardForm(forms.ModelForm):
  class Meta:
    model = Game
    fields = [
      'follow_player_card_action'
    ]

class LeadShiftForm(forms.ModelForm):
  class Meta:
    model = Game
    fields = [
      'lead_player_shift_action'
    ]

class FollowShiftForm(forms.ModelForm):
  class Meta:
    model = Game
    fields = [
      'follow_player_shift_action'
    ]