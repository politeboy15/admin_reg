from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import *
from .models import *
import services


def login_required_decorator(func):
    return login_required(func, login_url="login_page")


@login_required_decorator
def logout_page(request):
    logout(request)
    return redirect('login_page')


def login_page(request):
    if request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request, password=password, username=username)
        if user is not None:
            login(request, user)
            return redirect("home_page")
    return render(request, 'login.html')


@login_required_decorator
def home_page(request):
    faculties = services.get_faculties()
    kafedras = services.get_kafedras()
    ctx={
        'counts':{
            'faculties': len(faculties),
            'kafedras': len(kafedras),
        }
    }
    return render(request, 'index.html', ctx)



@login_required_decorator
def faculty_create(request):
    model=Faculty()
    form=FacultyForm(request.POST, instance=model)
    if request.POST and form.is_valid():
        if form.is_valid():
            form.save()
            return redirect('faculty_list')
    ctx={
        "form":form,
    }
    return render(request, 'faculty/form.html', ctx)


@login_required_decorator
def faculty_edit(request, pk):
    model=Faculty.objects.get(pk=pk)
    form=FacultyForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('faculty_list')
    ctx={
        "model":model,
        "form":form,
    }
    return render(request, 'faculty/form.html', ctx)


@login_required_decorator
def faculty_list(request):
    faculties = services.get_faculties()
    ctx = {
        "faculties": faculties,
    }
    return render(request, 'faculty/list.html', ctx)