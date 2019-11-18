from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns= [
    path("", views.login.as_view(), name='index' ),
    path('signup', views.signup.as_view(), name='signup'),
    path("postlogin",views.postlongin.as_view(),name="post"),
    path("logout",views.logout.as_view(),name="logout"),
   
]

