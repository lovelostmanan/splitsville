from django.shortcuts import render
from django.views import View,generic
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import account, person, friend, f_list
from django.template import loader

# Create your views here.
from django.http import HttpResponse

from django.views.generic import TemplateView

class postlongin(View):
    temp = 'splits/mp2.html'

    def get(self,request):
        user = request.user
        if user.is_active:
            all_people = person.objects.all()
            p = person.objects.get(user=user)
            flist = f_list.objects.get(person=p)
            flist = flist.frnd.all()

            context = {"user":user,"bal":account,"frnds":flist,"all":all_people}
            return render(request,self.temp,context)
        else:
            return HttpResponse("login failed")

    def post(self,request):
        user = request.user
        if user.is_active:
            all_people = person.objects.all()
            p = person.objects.get(user=user)
            pf = friend.objects.get(frnd=p)
            flist = f_list.objects.get(person=p)

            frnd_uname = request.POST.get("frndsel")
            frnd_user = User.objects.get(username=frnd_uname)
            frnd_person = person.objects.get(user=frnd_user)
            frnd_friend = friend.objects.get(frnd=frnd_person)
            frnt_flist = f_list.objects.get(person=frnd_person)

            frnt_flist.frnd.add(pf)
            frnt_flist.save()
            flist.frnd.add(frnd_friend)
            flist.save()

            flist_ppl = flist.frnd.all()

            context = {"user":user,"bal":account,"frnds":flist_ppl,"all":all_people}
            return render(request,self.temp,context)
        else:
            return HttpResponse("login failed")


class login(View):
    template_name = 'splits/mainpage.html'

    def get(self,request):
        user = request.user
        if user.is_authenticated:
            return HttpResponseRedirect('/splits/postlogin')
        return render(request, 'splits/mainpage.html')

    def post(self,request):
        uname= request.POST.get('uname','')
        password = request.POST.get('psw','')
        user = authenticate(username=uname, password=password)
        if user is not None:
            if user.is_active:
                dj_login(request, user) #the user is now logged in
                return HttpResponseRedirect('/splits/postlogin')
        else:
            return HttpResponse("login failed")

class logout(View):

    def get(self,request):
        user = request.user
        dj_logout(request)

        return HttpResponseRedirect("/splits")

   

class signup(View):
    template_name = 'splits/mainpage.html'

    def get(self,request):
        return render(request,'splits/signup.html')

    def post(self,request):
        uname= request.POST.get('uname','')

        try:
            User.objects.get(username=uname)
            return HttpResponse("username exists")
        except:
            fname= request.POST.get('fname','')
            lname= request.POST.get('lname','')
            email= request.POST.get('email','')
            password = request.POST.get('psw','')
            rpassword = request.POST.get('pswr','')

            if password != rpassword:
                return HttpResponse("Go back and use same password")

            password=make_password(password, salt=None, hasher='default')

            user = User(username=uname,password=password,first_name=fname,last_name=lname,email=email)
            user.save()

            manas = person(user=user)
            manas.save()
            acc = account(holder=manas)
            acc.save()
            frnd = friend(frnd=manas)
            frnd.save()
            f = f_list(person=manas)
            f.save()
            return HttpResponseRedirect('/splits')
