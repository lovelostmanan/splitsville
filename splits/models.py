from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User

class person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + '-' + self.user.last_name

class account(models.Model):
    holder = models.OneToOneField(person, on_delete=models.CASCADE)
    totalbalance = models.DecimalField(max_digits=5,decimal_places=3,default=Decimal('0.000'))
    youowe = models.DecimalField(max_digits=5,decimal_places=3,default=Decimal('0.000'))
    youareowed = models.DecimalField(max_digits=5,decimal_places=3,default=Decimal('0.000'))

    def __str__(self):
        return self.holder.user.first_name + '-' + self.holder.user.last_name

    
class make_group(models.Model):
    gname = models.CharField(max_length=64)
    glist = models.ManyToManyField(person)

    def __str__(self):
        return self.gname 

class friend(models.Model):
    frnd = models.OneToOneField(person,on_delete=models.CASCADE)

    def __str__(self):
        return self.frnd.user.username

class f_list(models.Model):
    person = models.OneToOneField(person,on_delete=models.CASCADE)
    frnd = models.ManyToManyField(friend)
