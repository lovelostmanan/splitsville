from django.shortcuts import render
from django.views import View,generic
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import account, person, friend, f_list, make_group, expense
from django.template import loader
import decimal
from django.conf import settings

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

            all_grps = make_group.objects.all()
            my_grps = []

            c = 0
            activity = None
            for x in all_grps:
                for y in x.glist.all():
                    if y == p:
                        my_grps.append(x)
                        if c == 0:
                            c=1
                            activity = expense.objects.filter(group=x)
                        else:
                            accc = expense.objects.filter(group=x)
                            activity = activity.union(accc)


            my_acc = account.objects.get(holder=p)
            totalbal = my_acc.youareowed - my_acc.youowe
            context = {"user":user,
                        "bal":my_acc,
                        "totbal":totalbal,
                        "frnds":flist,
                        "all":all_people,
                        "my_grps":my_grps,
                        "activity":activity}
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

            if len(request.POST.getlist("friend_make_grp")) > 0:
                mems_users = [User.objects.get(username=x) for x in request.POST.getlist("friend_make_grp")]
                mems = [ person.objects.get(user = x) for x in mems_users]
                new_grp = make_group(gname=request.POST.get("make_grp_name"))
                new_grp.save()
                for x in mems:
                    new_grp.glist.add(x)

                new_grp.save()
            
            if type(request.POST.get("frndsel")) != type(None) :
                if len(request.POST.get("frndsel")) > 0:
                    frnd_uname = request.POST.get("frndsel")
                    frnd_user = User.objects.get(username=frnd_uname)
                    frnd_person = person.objects.get(user=frnd_user)
                    frnd_friend = friend.objects.get(frnd=frnd_person)
                    frnt_flist = f_list.objects.get(person=frnd_person)

                    frnt_flist.frnd.add(pf)
                    frnt_flist.save()
                    flist.frnd.add(frnd_friend)
                    flist.save()

            if type(request.POST.get("expense_name")) != type(None) :    
                ex_name = request.POST.get("expense_name") 
                ex_amt = float(request.POST.get("expense_amt"))
                ex_grp = request.POST.get("expense_group")
                print("\n\n\n\n\n",ex_grp,"\n\n\n\n")
                grp = make_group.objects.filter(gname=ex_grp)[0]
                ex = expense(name=ex_name,group=grp,amt=ex_amt)
                ex.save()

                mem_ex = grp.glist.all()
                mem_count = len(mem_ex)
                dis_amt = float(ex_amt)/ mem_count

                for x in mem_ex:
                    if x != p:
                        acc = account.objects.get(holder=x)
                        print(acc.holder, acc.youowe)
                        acc.youowe = decimal.Decimal(acc.youowe) + decimal.Decimal(dis_amt)
                        acc.save()
                    else:
                        macc = account.objects.get(holder=x)
                        macc.youareowed = decimal.Decimal(macc.youareowed) + decimal.Decimal(ex_amt) - decimal.Decimal(dis_amt)
                        print(macc.holder,macc.youareowed)
                        macc.save()            
            
            flist = flist.frnd.all()
            all_grps = make_group.objects.all()
            my_grps = []
            activity = None
            c = 0
            for x in all_grps:
                for y in x.glist.all():
                    if y == p:
                        my_grps.append(x)
                        if c == 0:
                            c=1
                            activity = expense.objects.filter(group=x)
                        else:
                            accc = expense.objects.filter(group=x)
                            activity = activity.union(accc)


            my_acc = account.objects.get(holder=p)
            totalbal = my_acc.youareowed - my_acc.youowe
            context = {"user":user,
                        "bal":my_acc,
                        "totbal":totalbal,
                        "frnds":flist,
                        "all":all_people,
                        "my_grps":my_grps,
                        "activity":activity}
            return render(request,self.temp,context)
        else:
            return HttpResponse("login failed")


class login(View):
    template_name = 'splits/mainpage.html'

    def get(self,request):
        user = request.user
        if user.is_authenticated:
            return HttpResponseRedirect('/splits/postlogin')
        context = {"sitekey":settings.SITE_KEY}
        return render(request, 'splits/mainpage.html',context)

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
