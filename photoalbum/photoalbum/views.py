from django.shortcuts import render
from django.core.context_processors import csrf
from account.admin import RegistrationForm
from account.models import Account
from album.models import Album, Page, Picture
from django.contrib.auth import authenticate
import random

def index(request):
    #print("home index")
    albums = []
    thumbnails =[]
    user = request.user
    #print("user: ", user)
    if user.is_authenticated():
        albums = user.album_set.all()
        thumbnails = []
        for a in albums:
            picture = ''
            if a.firstpage != 0:
                pages = Page.objects.filter(album=a).order_by('?')
                for page in pages:
                    pictures = Picture.objects.filter(page=page).order_by('?')
                    length = len(pictures)
                    if length >0:
                        random_idx = random.randint(0, length-1)
                        picture = pictures[random_idx]
                        break
            else:
                page = Page(album=a, name="",number="1",layout="")
                picture = Picture(page=page, number=0,url="",caption="",price=0)
            thumbnails.append(picture)    
    registration_form = RegistrationForm()
    album_and_thumbs = zip(albums, thumbnails)
    return render(request, 'home/index.html', {'registration_form': registration_form, 'album_and_thumbs':album_and_thumbs})
