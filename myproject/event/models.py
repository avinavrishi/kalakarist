from django.db import models
from django.contrib.auth.models import AbstractUser

class EventType(models.Model):
    eventTypeName = models.CharField(max_length=50)
    def __str__(self):
        return self.eventTypeName
    
class EventCategory(models.Model):
    eventCategoryName = models.CharField(max_length=50)
    def __str__(self):
        return self.eventCategoryName
    
class EventPrize(models.Model):
    firstPrize = models.IntegerField()
    secondPrize = models.IntegerField()
    thirdPrize = models.IntegerField()
    
    def __str__(self):
        return self.id
    
class EntryFee(models.Model):
    entryTypes = (
        ('earlyBird', 'earlyBird'),
        ('lateBird', 'lateBird'),
    )    
    entryType = models.CharField(max_length=50, choices=entryTypes)
    price = models.IntegerField()
    def __str__(self):
        return self.id

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

# Create your models here.
class Events(models.Model):
    eventID = models.AutoField(primary_key=True)
    eventName = models.CharField(max_length=50)
    eventType = models.ForeignKey(EventType, default="Choose Event Type", on_delete=models.CASCADE)
    eventCategory = models.ForeignKey(EventCategory, default="Choose Category Type", on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, default= "Enter description")
    image = models.ImageField(upload_to='images/', default="")
    venue = models.ForeignKey(Address, default="Choose Venue", on_delete=models.CASCADE)
    entryFee = models.ForeignKey(EntryFee, default="", on_delete=models.CASCADE)
    prize = models.ForeignKey(EventPrize, default="", on_delete=models.CASCADE)
    eventDate = models.DateTimeField(default="")
    createdAt=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Event_name

class Users(AbstractUser):
    genderTypes = (
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')
    )

    phoneNumber = models.CharField(max_length=15)
    dateOfBirth = models.DateField()
    gender = models.CharField(choices=genderTypes, max_length=10)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    profilePicture = models.ImageField(upload_to='participant_profiles/', null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Battle(models.Model):
    battleTypes = (
        ('rap', 'rap'),
        ('dance', 'dance'),
    )

    eventId = models.ForeignKey(Events, on_delete=models.CASCADE)
    battleName = models.CharField(max_length=200)
    battleType = models.CharField(max_length=50, choices=battleTypes)
    battlePoints = models.IntegerField()
    participants = models.ManyToManyField(Users)

    def __str__(self):
        return self.battle_name
