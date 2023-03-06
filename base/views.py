from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic, Message #trqbva da dobavim bazite danni koito iskame i topic
from .forms import RoomForm#svyrzva s form.py
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

#Kogato v htmla ima link toy ni izprasha kum url.py v proekta koyto ni izprasha kym views.py 

#python manage.py runserver
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:#ako usera e lognat da ne moje da vliza v login page
        return redirect("home")
    if request.method=='POST':#Ako choveka clickne za vlizane
        username = request.POST.get('username').lower()#vzimame usernamea i go pravi na malki bukvi za da nqma obyrkvane
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)#vzima usernamea i ako nqma takyv v bazata danni hbyrlq greshka
        except:
            messages.error(request, 'User does not exist')#izkacha messege ako ima greshno ime
        user = authenticate(request, username = username, password = password)#proverqva dali ima user s tova ime i parola
        if user is not None:
            login(request, user)#logva usera
            return redirect('home')#prasha ni kym home ako usera e veren
        else:
            messages.error(request, 'Wrong password')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)#maha akaunta i preprasha kym home
    return redirect('home')

def registerPage(request):
    
    form = UserCreationForm()
    if request.method == "POST":#Ako se aktivira post methoda koyto idva ot butona register
        form = UserCreationForm(request.POST)#syzdavame user s parametrite ot post
        if form.is_valid():
            user = form.save(commit=False)#zapazvame cqloto vyv form bez da go izpylnqvame
            user.username = user.username.lower()#pravim imeto s malki bukvi
            user.save()#oficialno zapazva usera
            login(request, user)#vkarva usera v akaunta
            redirect('home')
        else:
            messages.error(request, 'An error accured during registration')
    context = {'form': form}
    return render(request, 'base/login_register.html', context)

def home(request):
    #q = request.GET.get('q') if request.GET.get('q') != None else '' #vzima se ot html i e okonchanie na urlto na stranicata i ako urlto e prazno izkarva vsichki stai
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ''
    


    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |#ako imeto na sekciqta sydyrja chas ot qto
        Q(name__icontains = q) 
    )
        
    topics = Topic.objects.all()#vzima vsichki topics
    room_count = rooms.count()#vzima kolko stai ima nalichni
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))#vzoma vsichki messigi
    context = {'rooms' : rooms, 'topics' : topics, 'room_count' : room_count, 'room_messages': room_messages}#promenliva koqto e rechnik i kazva koi promenlivi iskame da dadem na htmla
    return render(request, 'base/home.html', context) #Svyrzva otvarqneto na home s html fila home i mu dava promenilvata context


def room(request, pk):
    room = Room.objects.get(id=pk)#Zadava vsqka staq da ima za Info kokretnoto nesho na staqta chrez Idto i
    room_messages = room.message_set.all()#dava konkretnite messegi na konkretnata staq v koqto se namirame
    participants= room.participants.all()#vzimame participants ot bazata danni i shoto e many to many moje s .all
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,#vzimame ot requesta koy user se e lognal
            room = room,#vzimame staqta
            body = request.POST.get('body')#vzimame tqloto na message ot html 
        )
        room.participants.add(request.user)#koga nqkoy komentira vliza v participants na staqta
        return redirect('room', pk = room.id)#vkarvame pak v syshata staq s syhoto id za da ne se obyrka nesho ot POST
    context = {'room':room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user= User.objects.get(id=pk)
    rooms = user.room_set.all()#vzimame vsichki stai na syotvetniq profile
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')#zadyljava go za login i ako nqma login go prasha kym login page
def createRoom(request):
    form = RoomForm()#vzima cqlata informaciq ot RoomForm
    topics = Topic.objects.all()#vzima vsichki topics
    if request.method == "POST":#pravi vyzmojno kato vyvedem informaciq v stranichkata da se zapazva v baza danni
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)#ako ima takyv topic go slaga ako nqma pravi nov
        Room.objects.create(
            host=request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
            )
        
        return redirect('home')#izprasha ni v nachalniq prozorec
    context = {'form': form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')#zadyljava go za login i ako nqma login go prasha kym login page
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)#vzima staqta koqto she rabotim s primary key
    form = RoomForm(instance=room)#syzdava formata v koqto she updatevame i q zapylva s informaciq ot room ot gorniq red
    topics = Topic.objects.all()
    if request.user != room.host:#proverqva dali sobstvenika na staqta e syshiq chove koyto e vleznal i ako ne e mu hvyrlq response
        return HttpResponse("You are not allowed here")
    if request.method == "POST":#pravi vyzmojno kato vyvedem informaciq v stranichkata da se zapazva v baza danni
        form = RoomForm(request.POST, instance=room)#kachva zaqvkata v bazata danni otgovarqsha na idto
        if form.is_valid():#Proverqqva dali vsichko e validno 
            form.save()#zapazva promenite
            return redirect('home')#izprasha ni v nachalniq prozorec
        
    context = {'form': form, 'topics':topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')#zadyljava go za login i ako nqma login go prasha kym login page
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:#proverqva dali sobstvenika na staqta e syshiq chove koyto e vleznal i ako ne e mu hvyrlq response
        return HttpResponse("You are not allowed here")
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')#zadyljava go za login i ako nqma login go prasha kym login page
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:#proverqva dali sobstvenika na staqta e syshiq chove koyto e vleznal i ako ne e mu hvyrlq response
        return HttpResponse("You are not allowed here")
    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})