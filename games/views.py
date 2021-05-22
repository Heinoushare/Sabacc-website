from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import GameForm, LeadBettingForm, FollowBettingForm, LeadCardForm, FollowCardForm, LeadShiftForm, FollowShiftForm
from .models import Game
import random


# Create your views here.


@login_required(login_url='login')
def make_game_view(request):

    oldGames = []
    newGames = []
    newGame = Game.objects.get(id=1)
    requester = str(request.user)

    newGameIndex = 0
    for item in Game.objects.all():
        oldGames.append(item)

        newGameIndex = len(oldGames)
    form = GameForm
    gameIds = []
    gameLink = "https://Sabacc-website.heinoushare.repl.co/game/"
    slash = "/"
    linkEnd = "/start"

    form = form(request.POST or None)
    if form.is_valid():
        form.save()
        for item in Game.objects.all():
            gameIds.append(item.id)

        for item in Game.objects.all():
            newGames.append(item)

        gameId = gameIds[len(gameIds) - 1]
        gameId = str(gameId)
        gameLink = gameLink + gameId + slash + gameId + linkEnd
        newGame = newGames[newGameIndex]
        newGame.player1 = requester
        newGame.leading_player = requester
        newGame.active_player = requester
        newGame.save()
        return redirect(gameLink)

    print(request.user)

    context = {
        'form': form,
    }
    return render(request, "make_game.html", context)


def game_view(request, game_id, pk, action):
    deckList = []
    drawCards = []
    comma = ","


    game = Game.objects.get(id=pk)
    #print(game)


    if action == "start":
      if game.game_started == False:
        deckList = list(game.deck.split(','))
        drawCardIndex = random.randint(0, len(deckList) - 1)
        drawCards.append(deckList[drawCardIndex])
        deckList.pop(drawCardIndex)
        drawCardIndex = random.randint(0, len(deckList) - 1)
        drawCards.append(deckList[drawCardIndex])
        deckList.pop(drawCardIndex)

        for item in drawCards:
          print(item)
          game.player1_hand_sum = game.player1_hand_sum + int(item)
          if game.player1_hand == "":
            game.player1_hand = game.player1_hand + item

          elif game.player1_hand != "":
            game.player1_hand = game.player1_hand + comma + item
        removeCards = drawCards
        drawCards = []

        
        drawCardIndex = random.randint(0, len(deckList) - 1)
        drawCards.append(deckList[drawCardIndex])
        deckList.pop(drawCardIndex)
        drawCardIndex = random.randint(0, len(deckList) - 1)
        drawCards.append(deckList[drawCardIndex])
        deckList.pop(drawCardIndex)
        print(deckList)
        removeCards = removeCards + drawCards

        for item in drawCards:
          print(item)
          game.player2_hand_sum = game.player2_hand_sum + int(item)
          if game.player2_hand == "":
            game.player2_hand = game.player2_hand + item

          elif game.player2_hand != "":
            game.player2_hand = game.player2_hand + comma + item

        forCounter = 0
        for item in deckList:
          print(item)
          forCounter = forCounter + 1
          #print(deckList.index(item))
          if forCounter == 1:
            game.deck = item

          elif forCounter != 1:
            game.deck = game.deck + comma + item

        game.game_started = True

        game.save()

      linkBegin = "https://Sabacc-website.heinoushare.repl.co/game/"
      linkEnd = "/leadBet"
      slash = "/"
      gameId = str(game_id)
      link = linkBegin + gameId + slash + pk + linkEnd

      return redirect(link)

    player = str(request.user)

    leadBettingForm = LeadBettingForm(request.POST or None, instance=game)
    followBettingForm = FollowBettingForm(request.POST or None, instance=game)
    leadCardForm = LeadCardForm(request.POST or None, instance=game)
    followCardForm = FollowCardForm(request.POST or None, instance=game)
    leadShiftForm = LeadShiftForm(request.POST or None, instance = game)
    followShiftForm = FollowShiftForm(request.POST or None, instance = game)


    if action == "leadCard":
      if leadCardForm.is_valid():
        print("Lead player card actioon")
        print(leadCardForm)

        leadCardForm.save()

        if game.lead_player_card_action.lower() == "draw":
          if game.leading_player == game.player1:
            deckList = []
            drawCards = []

            deckList = list(game.deck.split(','))

            drawCardIndex = random.randint(0, len(deckList) - 1)
            drawCards.append(deckList[drawCardIndex])
            deckList.pop(drawCardIndex)
            
            removeCards = drawCards

            for item in drawCards:
              print(item)
              game.player1_hand_sum = game.player1_hand_sum + int(item)
              if game.player1_hand == "":
                game.player1_hand = game.player1_hand + item

              elif game.player1_hand != "":
                game.player1_hand = game.player1_hand + comma + item

            forCounter = 0
            for item in deckList:
              print(item)
              forCounter = forCounter + 1
              #print(deckList.index(item))
              if forCounter == 1:
                game.deck = item

              elif forCounter != 1:
                game.deck = game.deck + comma + item

          elif game.leading_player == game.player2:

            deckList = []
            drawCards = []

            deckList = list(game.deck.split(','))

            drawCardIndex = random.randint(0, len(deckList) - 1)
            drawCards.append(deckList[drawCardIndex])
            deckList.pop(drawCardIndex)
            
            removeCards = removeCards + drawCards

            for item in drawCards:
              print(item)
              game.player2_hand_sum = game.player2_hand_sum + int(item)
              if game.player2_hand == "":
                game.player2_hand = game.player2_hand + item

              elif game.player2_hand != "":
                game.player2_hand = game.player2_hand + comma + item

            forCounter = 0
            for item in deckList:
              print(item)
              forCounter = forCounter + 1
              #print(deckList.index(item))
              if forCounter == 1:
                game.deck = item

              elif forCounter != 1:
                game.deck = game.deck + comma + item

        elif game.lead_player_card_action.lower().startswith("trade"):
          if game.leading_player == game.player1:
            player1Hand = list(game.player1_hand.split(','))
            tradeCard = game.lead_player_card_action.lower().split("trade: ", 1)[1]
            player1Hand.remove(tradeCard)
            tradeCardValue = int(tradeCard)
            game.player1_hand_sum = game.player1_hand_sum - tradeCardValue

 
            deckList = []
            drawCards = []

            deckList = list(game.deck.split(','))

            drawCardIndex = random.randint(0, len(deckList) - 1)
            drawCards.append(deckList[drawCardIndex])
            deckList.pop(drawCardIndex)
            drawCardIndex = random.randint(0, len(deckList) - 1)
            drawCards.append(deckList[drawCardIndex])
            deckList.pop(drawCardIndex)
            print(deckList)
            removeCards = removeCards + drawCards

            for item in drawCards:
              print(item)
              game.player1_hand_sum = game.player1_hand_sum + int(item)
              if game.player1_hand == "":
                game.player1_hand = game.player1_hand + item

              elif game.player1_hand != "":
                game.player1_hand = game.player1_hand + comma + item

            forCounter = 0
            for item in deckList:
              print(item)
              forCounter = forCounter + 1
              #print(deckList.index(item))
              if forCounter == 1:
                game.deck = item

              elif forCounter != 1:
                game.deck = game.deck + comma + item

          elif game.leading_player == game.player2:
            player2Hand = list(game.player2_hand.split(','))

            tradeCard = game.lead_player_card_action.lower().split("trade: ", 1)[1]
            player2Hand.remove(tradeCard)
            tradeCardValue = int(tradeCard)
            game.player2_hand_sum = game.player2_hand_sum - tradeCardValue

            deckList = []
            drawCards = []

            deckList = list(game.deck.split(','))

            drawCardIndex = random.randint(0, len(deckList) - 1)
            drawCards.append(deckList[drawCardIndex])
            deckList.pop(drawCardIndex)
            drawCardIndex = random.randint(0, len(deckList) - 1)
            drawCards.append(deckList[drawCardIndex])
            deckList.pop(drawCardIndex)
            print(deckList)
            removeCards = removeCards + drawCards

            for item in drawCards:
              print(item)
              game.player2_hand_sum = game.player2_hand_sum + int(item)
              if game.player2_hand == "":
                game.player2_hand = game.player2_hand + item

              elif game.player2_hand != "":
                game.player2_hand = game.player2_hand + comma + item

            forCounter = 0
            for item in deckList:
              print(item)
              forCounter = forCounter + 1
              #print(deckList.index(item))
              if forCounter == 1:
                game.deck = item

              elif forCounter != 1:
                game.deck = game.deck + comma + item

          elif game.lead_player_card_action.lower() == "alderaan":
            print(game.leading_player, " just called Alderaan!")


        #game.lead_player_card_action = None
        if game.active_player == game.player1:
          game.active_player = game.player2

        elif game.active_player == game.player2:
          game.active_player = game.player1
        game.save()

        linkStart = "https://Sabacc-website.heinoushare.repl.co/game/"
        slash = "/"
        linkEnd = "/leadShift"
        link = linkStart + pk + slash + pk + linkEnd

        

        return redirect(link)
        

    elif action == "followCard":
      if followCardForm.is_valid():

        followCardForm.save()
        if game.follow_player_card_action.lower() == "draw":
          if game.leading_player != game.player1:
            deckList = []
            drawCards = []

            deckList = list(game.deck.split(','))

            drawCardIndex = random.randint(0, len(deckList) - 1)
            drawCards.append(deckList[drawCardIndex])
            deckList.pop(drawCardIndex)
            
            removeCards = removeCards + drawCards

            for item in drawCards:
              print(item)
              game.player1_hand_sum = game.player1_hand_sum + int(item)
              if game.player1_hand == "":
                game.player1_hand = game.player1_hand + item

              elif game.player1_hand != "":
                game.player1_hand = game.player1_hand + comma + item

            forCounter = 0
            for item in deckList:
              print(item)
              forCounter = forCounter + 1
              #print(deckList.index(item))
              if forCounter == 1:
                game.deck = item

              elif forCounter != 1:
                game.deck = game.deck + comma + item

          elif game.leading_player != game.player2:

            deckList = []
            drawCards = []

            deckList = list(game.deck.split(','))

            drawCardIndex = random.randint(0, len(deckList) - 1)
            drawCards.append(deckList[drawCardIndex])
            deckList.pop(drawCardIndex)
            drawCardIndex = random.randint(0, len(deckList) - 1)
            drawCards.append(deckList[drawCardIndex])
            deckList.pop(drawCardIndex)
            print(deckList)
            removeCards = removeCards + drawCards

            for item in drawCards:
              print(item)
              game.player2_hand_sum = game.player2_hand_sum + int(item)
              if game.player2_hand == "":
                game.player2_hand = game.player2_hand + item

              elif game.player2_hand != "":
                game.player2_hand = game.player2_hand + comma + item

            forCounter = 0
            for item in deckList:
              print(item)
              forCounter = forCounter + 1
              #print(deckList.index(item))
              if forCounter == 1:
                game.deck = item

              elif forCounter != 1:
                game.deck = game.deck + comma + item

        elif game.follow_player_card_action.lower().startswith("trade"):
          if game.leading_player != game.player1:
            player1Hand = list(game.player1_hand.split(','))
            tradeCard = game.follow_player_card_action.lower().split("trade: ", 1)[1]
            player1Hand.remove(tradeCard)
            tradeCardValue = int(tradeCard)
            game.player1_hand_sum = game.player1_hand_sum - tradeCardValue

 
            deckList = []
            drawCards = []

            deckList = list(game.deck.split(','))

            drawCardIndex = random.randint(0, len(deckList) - 1)
            drawCards.append(deckList[drawCardIndex])
            deckList.pop(drawCardIndex)
            drawCardIndex = random.randint(0, len(deckList) - 1)
            drawCards.append(deckList[drawCardIndex])
            deckList.pop(drawCardIndex)
            print(deckList)
            removeCards = removeCards + drawCards

            for item in drawCards:
              print(item)
              game.player1_hand_sum = game.player1_hand_sum + int(item)
              if game.player1_hand == "":
                game.player1_hand = game.player1_hand + item

              elif game.player1_hand != "":
                game.player1_hand = game.player1_hand + comma + item

            forCounter = 0
            for item in deckList:
              print(item)
              forCounter = forCounter + 1
              #print(deckList.index(item))
              if forCounter == 1:
                game.deck = item

              elif forCounter != 1:
                game.deck = game.deck + comma + item

          elif game.leading_player != game.player2:
            player2Hand = list(game.player2_hand.split(','))

            tradeCard = game.follow_player_card_action.lower().split("trade: ", 1)[1]
            player2Hand.remove(tradeCard)
            tradeCardValue = int(tradeCard)
            game.player2_hand_sum = game.player2_hand_sum - tradeCardValue

            deckList = []
            drawCards = []

            deckList = list(game.deck.split(','))

            drawCardIndex = random.randint(0, len(deckList) - 1)
            drawCards.append(deckList[drawCardIndex])
            deckList.pop(drawCardIndex)
            drawCardIndex = random.randint(0, len(deckList) - 1)
            drawCards.append(deckList[drawCardIndex])
            deckList.pop(drawCardIndex)
            print(deckList)
            removeCards = removeCards + drawCards

            for item in drawCards:
              print(item)
              game.player2_hand_sum = game.player2_hand_sum + int(item)
              if game.player2_hand == "":
                game.player2_hand = game.player2_hand + item

              elif game.player2_hand != "":
                game.player2_hand = game.player2_hand + comma + item

            forCounter = 0
            for item in deckList:
              print(item)
              forCounter = forCounter + 1
              #print(deckList.index(item))
              if forCounter == 1:
                game.deck = item

              elif forCounter != 1:
                game.deck = game.deck + comma + item

          
        game.phase = "Shift"
        game.follow_player_card_action = None
        game.save()
        linkStart = "https://Sabacc-website.heinoushare.repl.co/game/"
        slash = "/"
        linkEnd = "/followShift"
        link = linkStart + pk + slash + pk + linkEnd

        return redirect(link)


    elif action == "leadBet":
      print("Lead player betting")
      if leadBettingForm.is_valid():
        if game.follow_bet_counter == True:
          if game.follow_player_bet == game.lead_player_bet:
            game.hand_pot = game.hand_pot + game.follow_player_bet * 2
            game.lead_player_bet = None
            game.phase = "Card"

        if game.active_player == game.player1:
          game.active_player = game.player2
        elif game.active_player == game.player2:
          game.active_player = game.player1

        game.follow_bet_counter = False
        game.follow_player_bet = None

        game.save()

        leadBettingForm.save()
        linkStart = "https://Sabacc-website.heinoushare.repl.co/game/"
        slash = "/"
        linkEnd = "/leadCard"
        link = linkStart + pk + slash + pk + linkEnd

        return redirect(link)


    elif action == "followBet":
      if followBettingForm.is_valid():
        followBettingForm.save()
        if game.follow_player_bet == game.lead_player_bet:
          print(" calls.")
          game.hand_pot = game.hand_pot + game.lead_player_bet + game.follow_player_bet
          game.player1_credits = game.player1_credits - game.lead_player_bet
          game.player2_credits = game.player2_credits - game.follow_player_bet
          game.lead_player_bet = None
          game.follow_player_bet = None
          game.phase = "Card"
          if game.active_player == game.player1:
            game.active_player = game.player2
          elif game.active_player == game.player2:
            game.active_player = game.player1

          game.save()


        elif game.follow_player_bet == 0:
          print(" folds.")
          if game.leading_player == game.player1:
            game.player1_credits = game.player1_credits + game.hand_pot
            game.hand_pot = 0
          elif game.leading_player == game.player2:
            game.player2_credits = game.player2_credits + game.hand_pot
            game.hand_pot = 0

            game.player1_hand = ""
            game.player2_hand = ""

            deckList = list(game.deck.split(','))
            drawCardIndex = random.randint(0, len(deckList) - 1)
            drawCards.append(deckList[drawCardIndex])
            deckList.pop(drawCardIndex)
            drawCardIndex = random.randint(0, len(deckList) - 1)
            drawCards.append(deckList[drawCardIndex])
            deckList.pop(drawCardIndex)

            for item in drawCards:
              print(item)
              game.player1_hand_sum = game.player1_hand_sum + int(item)
              if game.player1_hand == "":
                game.player1_hand = game.player1_hand + item

              elif game.player1_hand != "":
                game.player1_hand = game.player1_hand + comma + item
            removeCards = drawCards
            drawCards = []

            
            drawCardIndex = random.randint(0, len(deckList) - 1)
            drawCards.append(deckList[drawCardIndex])
            deckList.pop(drawCardIndex)
            drawCardIndex = random.randint(0, len(deckList) - 1)
            drawCards.append(deckList[drawCardIndex])
            deckList.pop(drawCardIndex)
            print(deckList)
            removeCards = removeCards + drawCards

            for item in drawCards:
              print(item)
              game.player2_hand_sum = game.player2_hand_sum + int(item)
              if game.player2_hand == "":
                game.player2_hand = game.player2_hand + item

              elif game.player2_hand != "":
                game.player2_hand = game.player2_hand + comma + item

            forCounter = 0
            for item in deckList:
              print(item)
              forCounter = forCounter + 1
              #print(deckList.index(item))
              if forCounter == 1:
                game.deck = item

              elif forCounter != 1:
                game.deck = game.deck + comma + item

            if game.leading_player == game.player1:
              game.leading_player = game.player2
            elif game.leading_player == game.player2:
              game.leading_player == game.player1

            game.follow_player_bet = None

            game.save()

          elif game.follow_player_bet > game.lead_player_bet:
            print(" raises to ", game.follow_player_bet)
            game.follow_bet_counter = True
            if game.active_player == game.player1:
              game.active_player = game.player2
            elif game.active_player == game.player2:
              game.active_player == game.player1
            #game.lead_player_bet = None

            game.save()
          game.save()
        linkStart = "https://Sabacc-website.heinoushare.repl.co/game/"
        slash = "/"
        linkEnd = "/followCard"
        link = linkStart + pk + slash + pk + linkEnd

        return redirect(link)

    if action == "leadShift":
      print("Shift phase!")


    print(player)
    context = {
        'player': player,
        'game': game,
        'leadBettingForm': leadBettingForm,
        'followBettingForm': followBettingForm,
        'leadCardForm': leadCardForm,
        'followCardForm': followCardForm,
        'leadShiftForm': leadShiftForm,
        'followShiftForm': followShiftForm
    }

    return render(request, "game.html", context)
