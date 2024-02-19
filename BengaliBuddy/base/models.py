# Everytime you change or make something inside models, you have to write down this command after writing the code
#           python3 manage.py makemigrations
#           python3 manage.py migrate

from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

# Create your models here.
# python3 manage.py migrate to activate out prebuilt database that django already created for us.
class Room(models.Model):
    # Models by default have an id generated for them. Id value starts from 1
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # blank=True means the form that the users needs to be submit, it can be null, the user can do that later
    # all the users that are currently active in the room
    # participants = 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # if we save multiple time, auto_now_add will be change at the very first time whereas auto_now will be change
    # every single time the user will save 

    class Meta:
        ordering = ['-updated', '-created']
        # for ascending infact from small to big:
        # ordering = ['updated', 'created']

    def __str__(self):
        return str(self.name)
    
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # on_delete=models.CASCADE means if the Room is deleted, all the childrens of that will be deleted
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]
    # For Messages, we want to let the user show only first 50 charaters at the beginning

    
    