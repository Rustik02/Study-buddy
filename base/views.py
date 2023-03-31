from django.contrib.auth import authenticate, login, logout
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from base.forms import *
from base.models import Room, Topic, Message, User


def home(request):
    search = request.GET.get('search') \
        if request.GET.get('search') is not None \
        else ''
    rooms = Room.objects.filter(
        Q(topic__name__contains=search) |
        Q(name__contains=search) |
        Q(description__contains=search)
    )
    if bool(request.GET.get('more')):
        topics = Topic.objects.annotate(Count('room'))
    else:
        topics = Topic.objects.annotate(Count('room'))[:1]
    messages = Message.objects.all().order_by('-created')[:3]
    context = {
        'rooms': rooms,
        'topics': topics,
        'all': len(Topic.objects.all()),
        'messages': messages
    }
    return render(request, 'base/index.html', context)


def room_detail(request, pk):
    room = Room.objects.get(id=pk)
    messages = Message.objects.filter(room_id=room.pk)
    participants = room.participants.all()
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            mes = form.save(commit=False)
            mes.room = room
            mes.user = request.user
            room.participants.add(request.user)
            mes.save()
        return redirect('room', room.pk)
    context = {'room': room,
               'messages': messages,
               'participants': participants,
               "form": form
               }
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def room_create(request):
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/create_room.html', context)


@login_required(login_url='login')
def room_update(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    context = {'form': form}
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'base/edit-room.html', context)


@login_required(login_url='login')
def room_delete(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room.name})


@login_required(login_url='login')
def message_delete(request, pk):
    message = Message.objects.get(id=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('room', message.room.pk)

    return render(request, 'base/delete.html', {'obj': message.body})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context = {'form': UserForm, 'error': 'Incorrect'}
            return render(request, 'base/login.html', context)
    else:
        context = {'form': UserForm}
        return render(request, 'base/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


def registration_user(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('home')
    return render(request, 'base/registration.html', {'form': form})


def create_topic(request):
    form = TopicForm
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form
    }
    return render(request, 'base/create_topic.html', context)


def user_profile(request, pk):
    user = User.objects.get(pk=pk)
    rooms = Room.objects.filter(host=user)
    messages = Message.objects.all().order_by('-created')[:3]
    context = {
        'messages': messages,
        'user': user,
        'rooms': rooms
    }
    return render(request, 'base/profile.html', context)


def user_edit(request, pk):
    user = request.user
    form = UpdateUserForm(instance=user)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user.pk)
    context = {
        'user': user,
        'form': form
    }
    return render(request, 'base/edit-user.html', context)
