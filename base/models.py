from django.db import models
from django.contrib.auth.models import User

#  Sled vsqka nova migraciq tq trqbva da se savena i v powershell pishem : python manage.py makemigrations
#  Sled tova trqbva da se izpylni: python manage.py migrate

class Topic(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    


class Room(models.Model): #tuk si pravim tablicite s migration i v shell pishem python manage.py makemigrations da se syzdadat v papkata migrations
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)#Ako se iztrie Topic go zadava na null i pozvolqva sekciqta topic da e null
    name = models.CharField(max_length=200)#zapazva imenata na horata
    description = models.TextField(null=True, blank=True)#zapazva opisaniqta na horata i moje da e prazno
    participants = models.ManyToManyField(User, related_name='participants',blank=True)#pravi many to many s user participants
    updated = models.DateTimeField(auto_now=True)#zapazva koga eupdatenato
    created = models.DateTimeField(auto_now_add=True)#vzima samo pyrviq pyt kato e napravena

    class Meta:
        ordering = ['-updated', '-created']#sortira stranichkite po izdanie kato posledno kachenite sa nay-otgore
    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)#kogato iztriem user se triqt i vsichkite mu deca
    room = models.ForeignKey(Room, on_delete=models.CASCADE)# pri iztrivane da se trie cqloto
    body = models.TextField() 
    updated = models.DateTimeField(auto_now=True)#zapazva koga eupdatenato
    created = models.DateTimeField(auto_now_add=True)#vzima samo pyrviq pyt kato e napravena

    class Meta:
        ordering = ['-updated', '-created']#sortira stranichkite po izdanie kato posledno kachenite sa nay-otgore
        
    def __str__(self):
        return self.body[0:50] #vzimame pyrvite 50 bukvi na texta