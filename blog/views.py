import json
from django.shortcuts import render ,redirect
from django.contrib.auth import login as auth_login ,authenticate
from django.contrib.auth.forms import UserCreationForm,User
from .models import UserKeyword,UserCode,Code
from django.shortcuts import HttpResponse
from django.http import Http404


def login(request):
    cv = {}
    return render(request,'registration/login.html',cv)


def logout(request):
    cp ={}
    return render(request,'registration/logged_out.html',cp)


def signup(request):
    if request.method == 'POST':
        context={}
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request,user)
            #login(request , user,)
            return redirect('login')
    else:
        form = UserCreationForm()
        context = {'form': form}
    return render(request,'blog/signup.html',context)


def home(request):
    allcode=Code.objects.all()
    context={'allcode':allcode,}
    return render(request,'blog/home.html',context)


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












