from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

# rooms = [
#     {"id": 1, "name": "Let's learn Python!"}, 
#     {"id": 2, "name": "Learn Javascript"}, 
#     {"id": 3, "name": "Use Facebook properly"}
# ]

# Create your views here.
def home(request):
    rooms = Room.objects.all()
    context = {"rooms": rooms}
    return render(request, "base/home.html", context)

def room(request, pk):
    # room = None
    # for i in rooms:
    #     if i["id"] == int(pk):
    #         room = i
    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, "base/room.html", context)
