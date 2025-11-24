from django.db import models
from django.conf import settings

class Shop (models.Model):
    owner = models.OneToOneField( settings.AUTH_USER_MODEL,related_name="shop",null=True,blank=True, on_delete=models.CASCADE,verbose_name="")
    name = models.CharField( max_length=50)
    address = models.CharField( max_length=50)
    phone = models.CharField( max_length=50)
    created_at =models.DateTimeField(auto_now=False, auto_now_add=True)
    def __str__(self):
        return self.name
    