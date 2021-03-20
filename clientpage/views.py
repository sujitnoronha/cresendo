from django.shortcuts import render
from rest_framework.decorators import api_view
from profanity_check import predict, predict_prob
from clientpage.models import *
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response 
from clientpage.serializers import DriveSerializer
from clientpage.forms import * 
from django.contrib import messages
from PIL import Image
from textblob import TextBlob

        

from geopy.distance import geodesic

# Create your views here.
def home(request):
    drive = Locations.objects.filter(locationtype="tourist").order_by('FOMO')
    rest = Locations.objects.filter(locationtype="resteraunt").order_by('FOMO')    
    context = {
        'apikey' : 'AIzaSyCYUeS2YnGYNzt9kZRc1p-4tt4IyEacsjY',
        'drives': drive,
        'rest': rest,
    }
    return render(request,'clientpage/home.html',context)


def test(request):
    return render(request, 'clientpage/new.html')


#detail view for drive donation
def drivedonation(request, id):
    drive = Locations.objects.get(id=id)
    comments = CommentsField.objects.filter(location = drive).order_by('-id')
    context = {
        "drive" : drive,
        "comments": comments,
    }

    if request.method == "POST":
        comment = request.POST['comment']
        rating = request.POST['rating']
        pred = predict_prob([comment])
        print('hateval',pred)
        if pred[0] > 0.5:
            messages.info(request, 'Hate-speech detected! Please keep the comments clean')
            return render(request,'clientpage/profile.html',context)

        form = CommentForm(request.POST)

        print(form.is_valid())
        if form.is_valid():
            com = form.save(commit=False)
            com.location = drive
            com.save()
            blob = TextBlob(comment)
            polar = blob.sentences[0].sentiment.polarity
            print("sentiment",polar)
            if polar < 0:
                drive.FOMO = drive.FOMO - (10 - (polar + rating))
                print("fomoscore",drive.FOMO)
                drive.save() 
            messages.info(request, 'Posted successfully')
            return render(request,'clientpage/profile.html',context)

    return render(request,'clientpage/profile.html',context)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def locations(request,*args,**kwargs):
    print(request.data)
    lat = request.data['latitude']
    long = request.data['longitude']
    print(lat,long)
    origin = (lat,long)
    distance = {}
    for m in Locations.objects.all():
        dest = (m.latitude, m.longitude)
        print(dest)
        distance[m.name] = round(geodesic(origin, dest).kilometers, 2)
    s_d = sorted(distance.items(), key=lambda x: x[1]) 
    context = []
    for i in range(len(s_d)):
        li = {}
        drivedata = Locations.objects.get(name=s_d[i][0])
        url = drivedata.get_absolute_url()  
        serializer = DriveSerializer(drivedata, many=False)
        li.update({"driveinfo": serializer.data, "distance": s_d[i][1],'url': url,"imageurl": drivedata.image.url})
        context.append(li)

    return Response({"message":"success", "data": context})



def enquiryview(request):
    context = {
    }
        
    return render(request,'clientpage/liveenquiry.html',context)

def appointmentview(request,id):
    drive = DonationDrives.objects.get(id=id)
    
    form = appointForm()
    context = {
        "drive" : drive,
        "form" : form,
    }
    if request.method == "POST":
        print(request.POST)
        form = appointForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            appoint = form.save(commit=False)
            appoint.drive = drive
            appoint.save()
            messages.success(request,'Appointment success!')
            return render(request,'clientpage/profile.html',context)

    return render(request,'clientpage/appointment.html',context)

