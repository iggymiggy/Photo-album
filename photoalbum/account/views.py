from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from account.admin import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
import json

def login(request):
  if request.is_ajax() and not request.user.is_authenticated(): # prevent unnecessary requests
    form = LoginForm(data=request.POST or None)
    if request.POST:
      if form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
          auth_login(request, user)
          return HttpResponse(json.dumps({'success': True}), content_type="application/json")
      else:
        errors = form.errors
        return HttpResponse(str(errors))
    return render(request, "includes/login.html", {"login_form": form})
  return redirect('/')

def logout(request):
  auth_logout(request)
  return redirect('/')

def register(request):
  if request.is_ajax() and not request.user.is_authenticated():
    form = RegistrationForm(request.POST or None)
    if request.POST:
      if form.is_valid():
        user = form.save()
        user = authenticate(username=request.POST['email'],
                          password=request.POST['password1'])
        auth_login(request, user)
        return HttpResponse(json.dumps({'success': True}), content_type="application/json")
      else:
        errors = form.errors
        return HttpResponse(str(errors))
    return render(request, "includes/register.html", {"registration_form": form})
  return redirect('/')

def settings(request):
  # In the future add some user settings?
  pass
