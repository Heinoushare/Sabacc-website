from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm, ChatForm
from .models import Chat
from games.models import Game

from django.contrib.auth.decorators import login_required

# Create your views here.
def home_view(request, *args, **kwargs):

  linkBegin = "https://sabacc-website.heinoushare.repl.co/game/"
  slash = "/"
  linkEnd = "/null"

  gameLinks = []
  for item in Game.objects.all():
    itemId = str(item.id)
    gameLink = linkBegin + itemId + slash + itemId + linkEnd
    gameLinks.append(gameLink)

  games = Game.objects.all()
  requester = str(request.user)

  context = {
    'games': games,
    'requester': requester, 
    "gameLinks": gameLinks
  }

  return render(request, "home.html", context)

def register_view(request):
  form = CreateUserForm

  form = form(request.POST or None)
  if form.is_valid():
    form.save()
    user = form.cleaned_data.get('username')
    messages.success(request, 'Account was created for ', user)
    return redirect('login')
    


  context = {
    'form': form
  }
  return render(request, "register.html", context)

def login_view(request):


  if request.method == 'POST':

    
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect('home')

    else:
      messages.info(request, 'Username or Password is incorrect.')
      return render(request, "login.html", {})
  context = {
    #'form': form
  }
  return render(request, "login.html", context)


def logout_view(request):
  logout(request)
  return redirect('login')
  
  

@login_required(login_url='login')
def chat_view(request):
  

  form = ChatForm
  oldMessages = []
  newMessages = []
  newMessage = Chat.objects.get(id=1)
  requester = str(request.user)
  
  newMessageIndex = 0
  for item in Chat.objects.all():
    oldMessages.append(item)

    newMessageIndex = len(oldMessages)

  form = form(request.POST or None)
  if form.is_valid():
    form.save()

    

    for item in Chat.objects.all():
      newMessages.append(item)

  
    newMessage = newMessages[newMessageIndex]
  newMessage.author_of_message = requester
  newMessage.save()
  chatResults = Chat.objects.all()


  return render(request, "chat.html", {'chatResults': chatResults, 'form': form})