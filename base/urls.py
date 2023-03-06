from django.urls import path
from . import views
#Mqsto kydeto da sedqt opredelenite url ne v glavniq file da e po-razchetimo
urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name = "home"), #ako imeto na adreesa nqma dopylniq da prati kym Filea views metoda home i se kazva home
    path('room/<str:pk>', views.room, name = "room" ),#str:pk e za da se otvarq vinagi linka s nesho sled room koeto da e chislo i da kokretizira za koq tochno staq se otvarq
    path('create-room', views.createRoom, name = "create-room"),
    path('update-room/<str:pk>', views.updateRoom, name = "update-room"), #Pravi url za update i sled nego idto na opredelenata staq
    path('delete-room/<str:pk>', views.deleteRoom, name = "delete-room"),
    path('delete-message/<str:pk>', views.deleteMessage, name = "delete-message"),
    path('profile/<str:pk>', views.userProfile, name = "user-profile" ),
]

