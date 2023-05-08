from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from chat.models import Thread
from accounts import models
from chat.models import Thread, ChatMessage


@login_required
def messages_page(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads
    }
    return render(request, 'chat/messages.html', context)


def create_thread(request, pk):
  first_person = request.user
  second_person = models.CustomUser.objects.get(id=pk)

  if Thread.objects.filter(first_person=first_person, second_person=second_person).exists():
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads
    }
    return render(request, 'chat/messages.html', context)
  else:
    sender_thread = Thread(first_person=first_person, second_person=second_person) # if it's a new communication create a new thread
    sender_thread.save()
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads
    }
    return render(request, 'chat/messages.html', context)

  

