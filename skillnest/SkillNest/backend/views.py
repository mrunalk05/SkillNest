from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, EditUserProfileForm
from django.contrib.auth import  login,logout, authenticate
from django.contrib import messages
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers,status
from .models import skill,domain,User
import requests

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def index(request):
    return render(request, 'index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    # print(form)
    if request.method == 'POST':
        # print("user")
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in Sucessfully!!')
                return HttpResponseRedirect('profile')
                # return redirect('afterLogin')
            
            else:
                msg= 'Invalid Credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})


@login_required
def handelLogout(request):
    logout(request)
    return redirect('/login')


def profile(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            fm= EditUserProfileForm(request.POST, instance=request.user)
            if fm.is_valid():
                messages.success(request, "Profile Updated!!")
                fm.save()
        else:
            fm= EditUserProfileForm(instance=request.user)
        return render(request, 'profile.html', {'name':request.user, 'form':fm})
    else:
        return redirect('index')
def afterLogin(request):
    p=User.objects.all()
    print(p)
    for i in p:
        print(i.id)
    skil=domain.objects.all()
    print(skil)
    # for i in skill:
    #     print(i)
       
    dom=requests.get("http://127.0.0.1:8000/domainview")
    # print(dom)
    return render(request,'afterLogin.html',{'dom':dom,"domain":skil})


class skillSerializer(serializers.ModelSerializer):
    class Meta:
        model=skill
        fields=['uid','userName','domain_id','skillLevel','years']

class skillview(APIView):
    

    def get(self,request,pk=None):
        id=pk
        if id is not None:
            queryset=skill.objects.get(uid=id)
            serializer_class=skillSerializer(queryset)
            # print(queryset.topic)
            return Response({"data":serializer_class.data})
        queryset=skill.objects.all()
        serializer_class=skillSerializer(queryset,many=True)
        return Response(serializer_class.data)

    def post(self,request):
        serializer_class=skillSerializer(data=request.data)
        if serializer_class.is_valid():
            print("yes")
            serializer_class.save()
            return redirect('../skill')
        return Response(serializer_class.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        id=pk
        queryset=skill.objects.get(uid=id)
        serializer_class=skillSerializer(queryset, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response({'msg':serializer_class.data})
        return Response(serializer_class.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        id =pk
        queryset=skill.objects.get(uid=id)
        serializer_class=skillSerializer(queryset, data=request.data,partial=True)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response({'msg':'Partial Data Updated','data':serializer_class.data})
        return Response(serializer_class.errors)

    def delete (self,request,pk):
        id=pk
        member = skill.objects.get(uid=pk)
        member.delete()
        return Response({'msg':'Deleted'})



def skillPost(request):
    if request.method=="POST":
        uN=request.POST["userName"]
        dN=request.POST["domainName"]
        sN=request.POST["skillName"]
        sL=request.POST["skillLevel"]
        y=request.POST["years"]
        pd=request.POST["projectdes"]
        print(uN)
        print(dN)
        print(sN)
        print(sL)
        # print(y)
        q=domain.objects.filter(domain=dN, skillName=sN)
        d_id="" 
        u_id=""
        for i in q:
            d_id=i.domain_id

        print(d_id)
        p=User.objects.get(username=uN)
        u_id=p.id
       
        context={
            "userName":u_id,
            "domain_id":d_id,
            "years":y,
            "skillLevel":sL,
            "projectdes":pd
        }
        
        print("hello")
        print(context)
        requests.post('http://127.0.0.1:8000/skillview',context)
    return redirect("afterLogin")


def skillUpdate(request,pk):
    #  if request.method == 'POST':
    #     skilllevel = request.POST.get('skillLevel'),
    #     project= request.POST.get('project'),
    #     skillex= request.POST.get('skillex')

    #     emp= Employ(
    #     id=id,
    #     skilllevel= skilllevel,
    #     project= project,
    #     skillex= skillex
    #     )
    #     emp.save()
  if request=="POST":
    uN=request.POST["userName"]
    dN=request.POST["domainName"]
    sN=request.POST["skillName"]
    sL=request.POST["skillLevel"]
    y=request.POST["years"]
    pd=request.POST["projectdes"]
    print(uN)
    print(dN)
    q=domain.objects.filter(domain=dN, skillName=sN)
    q_id=""
    u_id=""
    for i in q:
            d_id=i.domain_id

    p=User.objects.get(username=uN)
    u_id=p.id
    context={
            "years":y,
            "skillLevel":sL,
            "projectdes":pd
    }
    requests.patch('http://127.0.0.1:8000/skillview'+u_id,context)
  return redirect("afterLogin")

class domainSerializer(serializers.ModelSerializer):
    class Meta:
        model=domain
        fields='__all__'

class domainview(APIView):
    

    def get(self,request,pk=None):
        id=pk
        if id is not None:
            queryset=domain.objects.get(domain_id=id)
            serializer_class=domainSerializer(queryset)
            # print(queryset.topic)
            return Response({"data":serializer_class.data})
        queryset=domain.objects.all()
        serializer_class=domainSerializer(queryset,many=True)
        return Response(serializer_class.data)

    def post(self,request):
        serializer_class=domainSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return redirect('../afterLogin')
        return Response(serializer_class.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        id=pk
        queryset=domain.objects.get(domain_id=id)
        serializer_class=domainSerializer(queryset, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response({'msg':serializer_class.data})
        return Response(serializer_class.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        id =pk
        queryset=domain.objects.get(domain_id=id)
        serializer_class=domainSerializer(queryset, data=request.data,partial=True)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response({'msg':'Partial Data Updated','data':serializer_class.data})
        return Response(serializer_class.errors)

    def delete (self,request,pk):
        id=pk
        member = domain.objects.get(domain_id=pk)
        member.delete()
        return Response({'msg':'Deleted'})


def delete (request,pk):
        id=pk
        member =skill.objects.get(uid=pk)
        member.delete()
        return redirect("/afterLogin")



def edit(request):
    emp= skill.objects.all()

    context={
        'emp': emp,
    }
    return redirect(request, "index.html", context)

def update(request,id):
    if request.method == 'POST':
        skilllevel = request.POST.get('skillLevel'),
        skillex= request.POST.get('years')

        emp= skill(
        id=id,
        skilllevel= skilllevel,
        skillex= skillex
        )
        emp.save()
        return redirect('home')
        
    return redirect(request, "index.html")