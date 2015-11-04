from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from album.models import Album, Page, Picture
from account.models import Account
import json

#TODO: Remove this
def index(request):
  user = request.user
  user_albums = Album.objects.filter(id=user.id)
  albums = {'albums': user_albums}
  return render(request, "home/index.html", albums)
    
def create_album(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            name = request.POST['album_name_create']
            description = request.POST['album_description_create']
            album = Album(owner=user, name=name, description=description, firstpage=0)
            album.save()
            return redirect('view_album', album_id = album.id)
    else:
        return redirect('/')

def rename_album(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            name = request.POST['newName']
            description = request.POST['newDes']
            album_id = request.POST['album_id']
            a_id = int(''.join(ele for ele in album_id if ele.isdigit()))
            album = Album.objects.get(id=int(a_id))
            album.name = name
            album.description = description
            album.save()
            return redirect('view_album', album_id = album.id)
    else:
        return redirect('/')

def view_album(request, album_id):
  try:
    album = Album.objects.get(id = int(album_id))
    user = request.user
    if user.id == album.owner.id:
      album_pages = album.page_set.all().order_by('number')
      return render(request, "album/album.html", {'album': album, 'pages':album_pages, })
  except Album.DoesNotExist:
    return redirect('/')
    
def remove_album(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            album_id = request.POST['album_id']
            a_id = int(''.join(ele for ele in album_id if ele.isdigit()))
            album = Album.objects.get(id=int(album_id))
            album.delete()
    return redirect('/')


def view_public_album(request, album_key):
    try:
        album = Album.objects.get(public_hash = album_key)
        album_pages = album.page_set.all().order_by('number')
        return render(request, "album/album.html", {'album': album, 'pages':album_pages, 'public':"public" })
    except Album.DoesNotExist:
        return redirect('/')

def create_page(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            layout = request.POST['layout']
            album_id = request.POST['album_id']
            url = request.POST['url']
            page_name = request.POST['page_name']
            try:
                album = Album.objects.get(id = album_id)
            except Album.DoesNotExist:
                album = None
            if album != None:
                 #all pages for the first time
                album_pages = album.page_set.all().order_by('number')
                page = Page(number=(len(album_pages) + 1), name= page_name, layout=layout,album=album)
                page.save()
                layout_num = int(layout[len(layout)-1])
                
                for i in range(layout_num):
                    picture = Picture(page=page,number=i+1,url=url, caption="", price=0)
                    picture.save()
                    if layout_num == 3 and i == 1:
                        break
                #add first page idx to album field
                if album.firstpage == 0:
                    album.firstpage = page.id
                    album.save()
                #all pages after saving to database
                album_pages = album.page_set.all().order_by('number')
                page = {'id': page.id, 'number': page.number, 'name':page.name, 'layout':page.layout, 'album_id':album_id, 'album_pages':album_pages}
                url = "album/"+layout + ".html"
                return render(request, url, page)
    else:
        return redirect('/')
        
def save_page(request):
    if request.method == 'POST':    
        user = request.user
        if user.is_authenticated():
            #parse json string to json data
            json_data = request.POST['data'] 
            jdata = json.loads(json_data)
            imgsrc = {} #for image urls from links
            captions = {}
            pictures_from_page = {} #for picture models in database
            url = "/"
            data ={}
            current_page = 0
            #parse json dictionary to own dictionaries for image sources, captions and page
            for key in jdata:
                if key.find("image") != -1: #image tags
                    idx = ''.join(c for c in key if c.isdigit())
                    imgsrc[idx]=jdata[key]
                if key.find("textBox") != -1: #captions
                    idx = ''.join(c for c in key if c.isdigit())
                    captions[idx]=jdata[key]
                if key == 'page_id' :   #page
                    page_id=jdata[key]
                    page=Page.objects.get(id=int(page_id))
                    current_page = page
                    data['id']= page.id
                if key == 'layout' :    #layout
                    url = "album/" + jdata[key] + ".html"
            pictures = Picture.objects.filter(page=page).order_by('number')
            if 'one_picture' in jdata:
                for key in imgsrc:  
                    picture = Picture.objects.get(number=int(key), page=page)
                    picture.url = imgsrc[key]
                    print("hinta: ", picture.price)
                    if jdata['price'] is not None and jdata['price'] is not 0 :
                        picture.price = float(jdata['price'])
                        print("hinta2: ", picture.price)
                    picture.save()
            else: #caption
                if 'image_number' in json_data and 'caption_text' in json_data:
                    picture = Picture.objects.get(number=int(jdata['image_number']), page=page)
                    picture.caption = jdata['caption_text']
                    picture.save()
            pictures = Picture.objects.filter(page=current_page).order_by('number')
            if page != None:
                album = Album.objects.get(id = page.album.id)
                album_pages = album.page_set.all().order_by('number')
                data = {'id': page.id, 'number': page.number, 'name':page.name, 'layout':page.layout, 'album_id':page.album.id, 'album_pages':album_pages}
                data['pictures'] = pictures
            return render(request, url,data)
    else:
        return redirect('/')
    
def view_page(request):
    user = request.user
    if user.is_authenticated():
        page_id = request.POST['page_id']
        current_page = Page.objects.get(id=page_id)
        pictures = Picture.objects.filter(page=current_page).order_by('number')
        url = "album/" + str(current_page.layout) + ".html"
        page = current_page
        album = Album.objects.get(id=page.album.id)
        album_pages = album.page_set.all().order_by('number')
        data = {'id': page.id, 'number': page.number, 'name':page.name, 'layout':page.layout, 'album_id':page.album, 'album_pages':album_pages}
        data['pictures'] = pictures
        return render(request, url, data)
    else:
        return redirect('/')

def remove_page(request):
    if request.method == 'POST':    
        user = request.user
        if user.is_authenticated():
            page_id = request.POST['pageid']
            p_id = int(''.join(ele for ele in page_id if ele.isdigit()))
            page = Page.objects.get(id=int(p_id))
            remove_number = page.number
            pages = Page.objects.filter(album=page.album).order_by('number')
            for p in pages:
                if p.number > remove_number:
                    p.number = p.number-1 #refresh page numbers coming after page to be removed
                    p.save()
            album = page.album
            page.delete()
            album_pages = Page.objects.filter(album=page.album).order_by('number')
            return redirect('view_album', album_id = album.id)
    else:
        return redirect('/')

def name_page(request):
    if request.method == 'POST':    
        user = request.user
        if user.is_authenticated():
            page_id = request.POST['page_id']
            page_id = int(''.join(ele for ele in page_id if ele.isdigit()))
            newName = request.POST['newName']
            page = Page.objects.get(id=int(page_id))
            page.name = newName
            page.save()
            pictures = Picture.objects.filter(page=page).order_by('number')
            url = "album/" + str(page.layout) + ".html"
            album = Album.objects.get(id=page.album.id)
            album_pages = album.page_set.all().order_by('number')
            data = {'id': page.id, 'number': page.number, 'name':page.name, 'layout':page.layout, 'album_id':page.album, 'album_pages':album_pages}
            #if not added pictures yet
            if not pictures:
                return render(request, url, data)
            data['pictures'] = pictures
            return render(request, url, data)
    else:
        return redirect('/')
        
def moveleft_page(request):
    user = request.user
    if user.is_authenticated():
        page_id = request.POST['page_id']
        page = Page.objects.get(id=page_id)
        if page.number >1 :
            try:
                number = page.number-1
                page_left = Page.objects.get(album=page.album, number=number)
                page_tmp = page
                page_left_tmp = page_left
                
                page_b =Page(album=page_tmp.album,name=page_tmp.name, layout= page_tmp.layout, number = page_left_tmp.number)
                page_a =Page(album=page_tmp.album,name= page_left_tmp.name,layout= page_left_tmp.layout, number = page_tmp.number)
                page_b.save()
                page_a.save()
                pic_p_left = Picture.objects.filter(page=page_left).order_by('number')
                pic_p = Picture.objects.filter(page=page).order_by('number')
                for pic in pic_p_left:
                    pic.page = page_a
                    pic.save()
                for pic in pic_p:
                    pic.page = page_b
                    pic.save()   
                page.delete()
                page_left.delete()
                pictures = Picture.objects.filter(page=page_b).order_by('number')
                url = "album/" + str(page_b.layout) + ".html"
                album = Album.objects.get(id=page_b.album.id)
                album_pages = Page.objects.filter(album =album).order_by('number')
                data = {'id': page_b.id, 'number': page_b.number, 'name':page_b.name, 'layout':page_b.layout, 'album_id':page_b.album, 'album_pages':album_pages}
                data['pictures'] = pictures
                return render(request, url, data)
            except Page.DoesNotExist:
                return render(request, "album/album.html")
        return (request,"album/album.html")
    else:
        return redirect('/')        
        
def moveright_page(request):
    user = request.user
    if user.is_authenticated():
        page_id = request.POST['page_id']
        page = Page.objects.get(id=page_id)
        pages = Page.objects.filter(album=page.album)
        if page.number < len(pages):
            try:
                number = page.number+1
                page_left = Page.objects.get(album=page.album, number=number)
                page_tmp = page
                page_left_tmp = page_left
                
                page_b =Page(album=page_tmp.album,name=page_tmp.name, layout= page_tmp.layout, number = page_left_tmp.number)
                page_a =Page(album=page_tmp.album,name= page_left_tmp.name,layout= page_left_tmp.layout, number = page_tmp.number)
                page_b.save()
                page_a.save()
                pic_p_left = Picture.objects.filter(page=page_left).order_by('number')
                pic_p = Picture.objects.filter(page=page).order_by('number')
                for pic in pic_p_left:
                    pic.page = page_a
                    pic.save()
                for pic in pic_p:
                    pic.page = page_b
                    pic.save()   
                page.delete()
                page_left.delete()
                pictures = Picture.objects.filter(page=page_b).order_by('number')
                url = "album/" + str(page_b.layout) + ".html"
                album = Album.objects.get(id=page_b.album.id)
                album_pages = Page.objects.filter(album =album).order_by('number')
                data = {'id': page_b.id, 'number': page_b.number, 'name':page_b.name, 'layout':page_b.layout, 'album_id':page_b.album, 'album_pages':album_pages}
                data['pictures'] = pictures
                return render(request, url, data)
            except Page.DoesNotExist:
                return render(request, "album/album.html")
        return (request,"album/album.html")
    else:
        return redirect('/')             
        
        
        
        
        
        
        
        
        
        
        
        
        
        
  
