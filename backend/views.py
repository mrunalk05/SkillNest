from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login,logout
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers,status
from .models import skill,domain,User
import requests
from django_globals import globals


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
        print("user")
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            
            if user is not None:
                login(request, user)
                return redirect('afterLogin')
            
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})


@login_required
def handelLogout(request):
    logout(request)
    return redirect('/login')


def profile(request):
    return render(request,'profile.html')

def afterLogin(request):
    # p=User.objects.all()
    # print(p)
    # for i in p:
    #     print(i.id)

    # skil=domain.objects.filter()

    # print(skil)
    # for i in skill:
    #     print(i)
    array=[]
    dom=requests.get("http://127.0.0.1:8000/domainview")
    print(dom.json())
    if globals.user.is_manager:
        
        p=requests.get('http://127.0.0.1:8000/skillview')
        q=p.json()
        for b in q:
            
            for i in b:
                
                if i=="userName":
                    g=User.objects.get(id=b[i])
                    b[i]=g.username
                if i=="domain_id":
                    g=domain.objects.get(domain_id=b[i])
                    b[i]=g.domain+" "+g.skillName
            # print(b)
         
        for b in q:
            x = b["domain_id"].split()
            # print(x)
            context={
                 "uid":b["uid"],
                 "userName":b["userName"],
                 "domain_id":x[0],
                 "skillLevel":b["skillLevel"],
                 "years":b["years"],
                 "projectdes":x[1],
            }
            array.append(context)
         
       
            
           
        print(dom)
        
        return render(request,'afterLogin.html',{'dom':dom,"s":array})

    if globals.user.is_employee:
        s=skill.objects.filter(userName=globals.user.id)
        for i in s:
            context={
                "uid":i.uid,
                "years":i.years,
                "skillName":i.domain_id.skillName,
                "domainName":i.domain_id.domain,
                "skillLevel":i.skillLevel
            }
            array.append(context)
            
        



    return render(request,'afterLogin.html',{'dom':dom,"s":array})

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


def skillUpdate(request):
    if request.method=="POST":
        
        u_id=request.POST["_id"]
        sL=request.POST["skillLevel"]
        y=request.POST["years"]
        pd=request.POST["projectdes"]

    
        context={
                "years":y,
                "skillLevel":sL,
                "projectdes":pd
        }
        requests.patch('http://127.0.0.1:8000/skillview/'+u_id,context)
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

def updateSkill(request):
    if request.method == 'POST':
        q=skill.objects.filter(uid=request.POST["id"])
        data = list(q.values())
        # print (data)
    return render(request,'updateSkill.html',{'da':data})