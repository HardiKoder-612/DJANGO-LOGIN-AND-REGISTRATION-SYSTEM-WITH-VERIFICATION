from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# class Image(models.Model):
#     id=models.AutoField
#     username=models.CharField(max_length=11,default='')
#     image=models.ImageField(null=True,blank=True,upload_to='media/',default='')
#
#     def __str__(self):
#         return self.username
#     pass

class Task(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True) #many to one relationship. If hte user get deleted, item will also deleted
    title=models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    complete= models.BooleanField(default=False)
    created= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering=['complete']   #any complete items should be at the bottoms of the list.