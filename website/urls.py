from django.conf.urls import url,include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    
    path("admin/", admin.site.urls),
    #url(r'^splits/', include('splits.urls')),
    path('splits/',include("splits.urls")),
    path('',include("splits.urls")),
]
