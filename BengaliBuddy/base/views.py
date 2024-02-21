from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#     {"id": 1, "name": "Let's learn Python!"}, 
#     {"id": 2, "name": "Learn Javascript"}, 
#     {"id": 3, "name": "Use Facebook properly"}
# ]


def loginPage(request):
    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=name)
        except:
            messages.error(request, "User doesn't exist. Please Register")
        

    context = {}
    return render(request, 'base/login_register.html', context)


# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # topic__name__icontains means: it will first go to topic -> name and then 'contains' if the user search by only
    # py, then he will get the topic that will match. i before contains means whether or not you want the seach option
    # case insentive or not
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    
    # count works faster then python length in django
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, "base/home.html", context)


def room(request, pk):
    # room = None
    # for i in rooms:
    #     if i["id"] == int(pk):
    #         room = i
    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, "base/room.html", context)


def createRoom(request):
    form = RoomForm
    if request.method == "POST":
        # using the below code, you can see everything you will get in the terminal when the user submit the form
        # print(request.POST)
        # We can get any specific data from the form by this:
        # print(request.POST.get("name"))

        # Passing in all the post data into the form, so the form knows which value is to extract from those
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form": form}
    return render(request, "base/room_form.html", context)


def updateRoom(request, pk):
    room = Room.objects.get(id=int(pk))
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        # 2nd argument tells that change the only the instance=room
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form": form}
    return render(request, "base/room_form.html", context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=int(pk))
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, "base/delete.html", {"obj": room})
