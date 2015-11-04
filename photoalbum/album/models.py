from django.db import models
from account.models import Account
import uuid

def _createId():
    print(uuid.uuid1().hex)
    return uuid.uuid1().hex

class Album(models.Model):
  owner = models.ForeignKey(Account)
  name = models.CharField(max_length=30)
  description = models.TextField()
  firstpage = models.IntegerField(default=0)  #index of first page
  public_hash = models.CharField(max_length=32, default=_createId, unique=True)
  
class Page(models.Model):
  album = models.ForeignKey(Album)
  name = models.CharField(max_length=30)
  number = models.IntegerField()
  layout = models.CharField(max_length=15)

class Picture(models.Model):
  page = models.ForeignKey(Page)
  number = models.IntegerField()
  url = models.URLField(default="")
  caption = models.TextField(default="")
  price = models.DecimalField(default=0,max_digits=10, decimal_places=2)
  

