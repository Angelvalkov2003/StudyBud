from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'#pravim forma koqto da sydyrja vsichki harakteristiki na edna staq i posle kato q vikame v cikyl se izkarva vsqko edno isakne pri syzdavane na staq