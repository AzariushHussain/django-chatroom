from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RoomForm
from .models import Room, Message
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

@login_required
def room_view(request, room_id=None):
    try:
        if request.method == 'POST':
            if room_id:
                try:
                    room = Room.objects.get(id=room_id)
                    print(f"room: {room}")
                    room.delete()
                    messages.success(request, 'Room deleted successfully.')
                    return redirect('room')
                except Room.DoesNotExist:
                    messages.error(request, 'Room not found.')
                    return redirect('room')
        elif request.method == 'GET':
            rooms = Room.objects.all()
            print(f"rooms: {rooms}")
            return render(request, 'room/room.html', {'rooms': rooms})
    except Exception as e:
        messages.error(request, 'An unexpected error occurred while processing your request.')
        print(f"Exception in room_view: {e}")
        return redirect('room')


@login_required
def create_room(request):
    try:
        if request.method == 'POST':
            form = RoomForm(request.POST)
            if form.is_valid():
                room = form.save(commit=False)
                room.admin = request.user
                room.save()
                messages.success(request, 'Room created successfully.')
                return redirect('room')
            else:
                messages.error(request, 'Form submission failed. Please try again.')
        else:
            form = RoomForm()
        return render(request, 'room/create_room.html', {'form': form})
    except IntegrityError as e:
        messages.error(request, 'Database error occurred while creating the room. Please try again later.')
        print(f"IntegrityError in create_room: {e}")
        return render(request, 'room/create_room.html', {'form': form})
    except Exception as e:
        messages.error(request, 'An unexpected error occurred while creating the room.')
        print(f"Exception in create_room: {e}")
        return render(request, 'room/create_room.html', {'form': form})


@login_required
def messages_view(request, room_id):
    try:
        if request.method == 'GET':
            try:
                room = Room.objects.get(id=room_id)
                messages = Message.objects.filter(room_id=room.id)
                return render(request, 'room/message_window.html', {'room': room, 'messages': messages})
            except Room.DoesNotExist:
                messages.error(request, 'Room not found.')
                return redirect('room')
    except Exception as e:
        messages.error(request, 'An unexpected error occurred while retrieving the messages.')
        print(f"Exception in messages_view: {e}")
        return redirect('room')
