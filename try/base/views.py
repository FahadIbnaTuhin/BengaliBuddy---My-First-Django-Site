from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room
from .forms import RoomForm

# rooms = [
#     {"id": 1, "name": "Learn Python with me"}, 
#     {"id": 2, "name": "Know about js"}, 
#     {"id": 3, "name": "React Education"}, 
# ]

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_count = rooms.count()
    topics = Room.objects.all()
    context = {"rooms": rooms, 'topics': topics, 'room_count': room_count}
    return render(request, "base/home.html", context)

def room(request, pk):
    # room = None
    # for i in rooms:
    #     if i["id"] == int(pk):
    #         room = i
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, "base/room.html", context)


def roomForm(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def updateForm(request, pk):
    room = Room.objects.get(id=int(pk))
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=int(pk))
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})