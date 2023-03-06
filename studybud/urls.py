from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls'))#kazva da vliza i da proverqva i za savpadashi imena v Base papkata faila urls i zadyljitelno mu trqbva importa includes i path
]
