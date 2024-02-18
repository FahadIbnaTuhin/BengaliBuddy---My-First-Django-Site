from django.db import models

# Create your models here.
# python3 manage.py migrate to activate out prebuilt database that django already created for us.
class Room(models.Model):
    # Models by default have an id generated for them. Id value starts from 1

    # host = 
    # topic = 
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # blank=True means the form that the users needs to be submit, it can be null, the user can do that later
    # all the users that are currently active in the room
    # participants = 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # if we save multiple time, auto_now_add will be change at the very first time whereas auto_now will be change
    # every single time the user will save 

    def __str__(self):
        return str(self.name)
    