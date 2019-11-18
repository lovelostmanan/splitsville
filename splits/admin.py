from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(person)
admin.site.register(account)
admin.site.register(make_group)
admin.site.register(friend)
admin.site.register(f_list)