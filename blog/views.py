import json
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import login as auth_login ,authenticate
from .models import UserKeyword,UserCode,Code
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from django.http import Http404,HttpResponseRedirect


def login(request):
    cv={}
    if request.method=='POST':
        email= request.POST.get('email',None)
        password1 = request.POST.get('password1',None)
        user = authenticate(username=email, password=password1)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return render(request, 'blog/home.html',cv)
        else:
            return render(request, 'blog/login.html', cv)
    else:
        return render(request, 'blog/login.html', cv)


def logout(request):
    cp ={}
    return render(request,'blog/logged_out.html',cp)


def get_user(email):
    try:
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None



def signup(request):
        cv={}
        if request.method == "POST":
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            user = get_user(email)
            if password1 == password2:
                if user is None:
                    user=User.objects.create_user(username=email)
                    user.set_password('password1')
                    user.save()
                    # user= authenticate(username=user, password=password1)
                    # auth_login(request, user)
                    # login
                    return redirect('blog:login')
            else:
                # messages
                return render(request, 'blog/signup.html',cv)
        else:
            # messages
            return render(request, 'blog/signup.html',cv)



def add_keyword(request):
    if request.method=='POST':
        word=request.POST.get('str',None)
        user = request.user
        if not user.is_authenticated():
            return HttpResponse("Not Authenticated")
        try:
            UserKeyword.objects.get(keyword=word, user=user)
            return HttpResponse(json.dumps({"message": "Keyword already present"}),
                                content_type="application/json")
        except UserKeyword.DoesNotExist:
            UserKeyword.objects.create(keyword=word, user=user)
            return HttpResponse(json.dumps({"message": "Keyword added"}),
                                content_type="application/json")
    else:
        raise Http404("Not Found")

def add_code(request):
    if request.method == 'POST':
        code = request.POST.get('code_id', None)
        user = request.user
        if not user.is_authenticated():
            return HttpResponse("Not Authenticated")
        try:
            code = Code.objects.get(id=code)
        except:
            return HttpResponse(json.dumps({"message": "Invalid code"}),
                                content_type="application/json")
        try:
            UserCode.objects.get(code=code, user=user)
            return HttpResponse(json.dumps({"message": "code already present"}),
                                content_type="application/json")
        except UserCode.DoesNotExist:
            UserCode.objects.create(code=code, user=user)
            return HttpResponse(json.dumps({"message": "code added"}),
                                content_type="application/json")
    else:
        raise Http404("Not Found")



def get_profile(request):
    if request.method=='POST':
        user=request.user
        allkey=UserKeyword.objects.filter(user=user)
        allcode=UserCode.objects.all()
        context={'allkey':allkey,'allcode':allcode}
        return render(request,'blog/profile.html',context)



def home(request):
    user=request.user
    if not user.is_authenticated():
       # print "if executeed"
        print "ejvv"
        cv={}
        return render(request,'blog/login',cv)
    else:
        print  "else executeed"
        allcode = Code.objects.all()
        context = {'allcode': allcode, }
        return render(request, 'blog/home.html', context)

