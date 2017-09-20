import json
import threading
import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from blog.utlis import scrape_from_advance_search_keyword, scrape_from_advance_search_code
from .models import UserKeyword, UserCode, Code, Keyword, KeywordOpportunity, CodeOpportunity
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from django.http import Http404


def redirect_to_home():
    return redirect(reverse('blog:home'))


def redirect_to_login():
    return redirect(reverse('blog:login'))


def login(request):
    user = request.user
    if user is not None:
        redirect_to_home()
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        print email, password
        user = authenticate(username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponse(json.dumps({"message": "Successfully LoggedIn", "success": True}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({"message": "Enter valid credentials"}),
                                content_type="application/json")
    else:
        return render(request, 'login.html', {})


def signup(request):
    user = request.user
    if user is not None:
        redirect_to_home()
    if request.method == "POST":
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        user = get_user(email)
        if user is not None:
            return HttpResponse(json.dumps({"message": "User already exists for this email ID", "success": False}),
                                content_type="application/json")
        if password1 == password2:
            user = User.objects.create_user(username=email, email=email)
            user.set_password(password1)
            user.save()
            auth_login(request, user)
            return HttpResponse(json.dumps({"message": "Successfully Registered and Logged In", "success": True}),
                                content_type="application/json")

        return HttpResponse(json.dumps({"message": "Passwords don't match", "success": False}),
                            content_type="application/json")
    else:
        return render(request, 'signup.html', {})


def logout(request):
    user = request.user
    if user is not None:
        auth_logout(request)
    return redirect_to_login()


def get_user(email):
    try:
        return User.objects.get(username=email.lower())
    except User.DoesNotExist:
        return None


def add_keyword(request):
    if request.method == 'POST':
        word = request.POST.get('str', None)
        user = request.user
        if not user.is_authenticated():
            return HttpResponse("Not Authenticated")

        if word is None:
            return HttpResponse(json.dumps({"message": "Invalid Keyword"}),
                                content_type="application/json")
        word = word.strip()
        if word == "":
            return HttpResponse(json.dumps({"message": "Invalid Keyword"}),
                                content_type="application/json")
        keyword_query = Keyword.objects.get_or_create(name=word)
        keyword = keyword_query[0]
        keyword_created = keyword_query[1]
        try:
            UserKeyword.objects.get(keyword=keyword, user=user)
            return HttpResponse(json.dumps({"message": "Keyword already present"}),
                                content_type="application/json")
        except UserKeyword.DoesNotExist:
            UserKeyword.objects.create(keyword=keyword, user=user)
            # if keyword.last_scraped is None or keyword.last_scraped > timezone.time() - datetime.timedelta(days=1):
            if keyword_created or keyword.last_scraped is None or keyword.last_scraped <= timezone.now() - datetime.timedelta(days=1):
                t = threading.Thread(target=scrape_from_advance_search_keyword, args=(keyword,))
                t.start()
            return HttpResponse(json.dumps({"message": "Keyword added", "keyword": word}),
                                content_type="application/json")
    else:
        raise Http404("Not Found")


def add_code(request):
    if request.method == 'POST':
        code = request.POST.get('code_id', None)
        user = request.user
        if not user.is_authenticated():
            return HttpResponse("Not Authenticated")
        if code is None:
            return HttpResponse(json.dumps({"message": "Invalid code"}),
                                content_type="application/json")
        try:
            code = Code.objects.get(code_id=code)
        except Code.DoesNotExist:
            return HttpResponse(json.dumps({"message": "Invalid code"}),
                                content_type="application/json")
        try:
            UserCode.objects.get(code=code, user=user)
            return HttpResponse(json.dumps({"message": "code already present"}),
                                content_type="application/json")
        except UserCode.DoesNotExist:
            UserCode.objects.create(code=code, user=user)
            if code.last_scraped is None or code.last_scraped <= timezone.now() - datetime.timedelta(days=1):
                t = threading.Thread(target=scrape_from_advance_search_code, args=(code,))
                t.start()
            return HttpResponse(json.dumps({"message": "code added", "code": code.code}),
                                content_type="application/json")
    else:
        raise Http404("Not Found")


def profile(request):
    user = request.user
    if not user.is_authenticated():
        return redirect_to_login()
    keyword_ids = UserKeyword.objects.filter(user=user).values('keyword__id')
    keyword_opportunities = KeywordOpportunity.objects.filter(keyword__id__in=keyword_ids)

    context = {'keyword_opportunities': keyword_opportunities}
    return render(request, 'profile.html', context)


def code_opportunities(request):
    user = request.user
    if not user.is_authenticated():
        return redirect_to_login()
    code_ids = UserCode.objects.filter(user=user).values('code__id')
    code_opportunities = CodeOpportunity.objects.filter(code__id__in=code_ids)

    context = {'code_opportunities': code_opportunities}
    return render(request, 'code_opportunities.html', context)

def home(request):
    user = request.user
    if not user.is_authenticated():
        return redirect_to_login()
    else:
        all_codes = Code.objects.all()
        user_keywords = UserKeyword.objects.filter(user=user)
        user_codes = UserCode.objects.all()
        context = {'codes': all_codes, 'user_keywords': user_keywords, 'user_codes': user_codes}
        return render(request, 'home.html', context)

