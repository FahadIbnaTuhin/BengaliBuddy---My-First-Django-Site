from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Room, Topic, Message
from .forms import RoomForm

# rooms = [
#     {"id": 1, "name": "Let's learn Python!"}, 
#     {"id": 2, "name": "Learn Javascript"}, 
#     {"id": 3, "name": "Use Facebook properly"}
# ]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist. Please Register")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Its add a new session in the database and inside of our browser and the user is officially logged in
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password is not right.")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # form.save(): Normally, when you call form.save() in Django, it will save the form data to the associated model and the database. The save() method is automatically generated for model forms.
            # commit=False: By passing commit=False as an argument to save(), you are telling Django not to immediately save the object to the database. This means the object is created in memory but not persisted to the database at this point.
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_register.html', {'form': form})


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
    roommessages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {"room": room, "roommessages": roommessages, 'participants': participants}
    return render(request, "base/room.html", context)


@login_required(login_url='login') 
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


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=int(pk))
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

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

    if request.user != room.host:
        return HttpResponse("You are not allowed here!")
    
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, "base/delete.html", {"obj": room})


def delete_msg(request, pk):
    message = Message.objects.get(id=int(pk))

    if request.user != message.user:
        return HttpResponse("You are not allowed here!")
    
    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request, "base/delete.html", {"obj": message})
