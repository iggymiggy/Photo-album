from django.shortcuts import render, redirect
from django.http import HttpResponse
from album.models import Album, Page, Picture
from django.db.models import Sum
import hashlib

def index(request, album_id):
  if request.user.is_authenticated():
    sid = 'mikkoikonen'
    pid = request.user.id
    key = '201ce80c86417c86da841a0fc047afbc'
    url = '/'.join(request.build_absolute_uri().split('/')[:-2])+'/'
    remote_url = 'http://payments.webcourse.niksula.hut.fi/pay/'
    price = get_price(int(album_id))
    context = {
          'sid': sid,
          'pid': pid,
          'key': key,
          'success_url': url+'success/',
          'cancel_url': url+'cancel/',
          'error_url': url+'error/',
          'amount': price,
          'checksum': calc_checksum(pid, sid, price, key),
          'remote_url': remote_url
        }
    return render(request, 'includes/payment.html', context);
  return redirect('/')

def pay(request): #might be used for payment
  if request.user.is_authenticated():
    if request.POST:
      pass
  return redirect('/')

def success(request):
  if request.GET:
    pid = request.GET['pid']
    ref = request.GET['ref']
    checksum = request.GET['checksum']
  return HttpResponse('Payment success!')

def cancel(request):
  return HttpResponse('Payment cancelled!')

def error(request):
  return HttpResponse('Payment error!')

def calc_checksum(pid, sid, amount, key):
    checksum_str = "pid={!s}&sid={!s}&amount={!s}&token={!s}".format(pid, sid, amount, key).encode('utf-8')
    m = hashlib.md5()
    m.update(checksum_str)
    checksum = m.hexdigest()
    return checksum

def get_price(album_id):
  pages = Page.objects.filter(album=album_id)
  price = 0
  for page in pages:
    pictures = Picture.objects.filter(page=page)
    for picture in pictures: 
        price = price + picture.price
        print("picture.price: ", picture.price)
  print("sum: ", price)
  page_ids = [page.id for page in pages]
  print(page_ids)
  #price = Picture.objects.filter(pk__in=page_ids).aggregate(Sum('price')).get('price__sum', 0.00)
  return price
