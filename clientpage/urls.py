from django.urls import path,include
from clientpage.views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', home, name='home'),
    path('locations/', csrf_exempt(locations), name="locations"),
    path('<int:id>/', drivedonation, name="profile"),
    path('test/', test, name="test"),
    path('videocall/', enquiryview, name="liveenquiry"),
    path('<int:id>/appoint/', appointmentview, name="appointment"),
    
   
]