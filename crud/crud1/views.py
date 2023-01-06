from django.shortcuts import render, redirect
from .models import Employ
# Create your views here.

def index(request):
    emp= Employ.objects.all()

    context={
        'emp': emp,
    }

    return render(request, "index.html", context)

def add(request):
    if(request.method == "POST"):
        skilllevel= request.POST.get('skilllevel')
        skillex= request.POST.get('skillex')
        project= request.POST.get('project')

        empr= Employ(
        skilllevel= skilllevel,
        skillex= skillex,
        project= project
        )
        empr.save()
        return redirect('home')

    return render(request, "index.html")

def edit(request):
    emp= Employ.objects.all()

    context={
        'emp': emp,
    }
    return redirect(request, "index.html", context)

def update(request,id):
    if request.method == 'POST':
        skilllevel = request.POST.get('skilllevel'),
        project= request.POST.get('project'),
        skillex= request.POST.get('skillex')

        emp= Employ(
        id=id,
        skilllevel= skilllevel,
        project= project,
        skillex= skillex
        )
        emp.save()
        return redirect('home')
        
    return redirect(request, "index.html")