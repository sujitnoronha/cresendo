from django import forms
from clientpage.models import *

class OrganizerForm(forms.ModelForm):
    class Meta:
        model = Locations
        fields = ['name','phonenumber','image', 'latitude', 'longitude', 'address','description']
    