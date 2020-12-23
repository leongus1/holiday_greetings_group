from django.db import models
import re
from cloudinary.models import CloudinaryField

# Create your models here.

class UserManager(models.Manager):
    def validate(self, postdata):
        email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postdata['f_n']) < 2:
            errors['f_n'] = "First name must be 2 or more characters"
        if len(postdata['l_n']) < 2:
            errors['l_n'] = "Last name must be 2 or more characters"
        if not email_check.match(postdata['email']):
            errors['email'] = "Invalid email address"
        if len(postdata['pw']) < 8:
            errors['pw'] = "Password must be at least 8 characters"
        if postdata['pw'] != postdata['conf_pw']:
            errors['conf_pw'] = "Password does not match confirm password"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
class Template(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Image(models.Model):
    name = models.CharField(max_length=100)
    img = CloudinaryField('img', null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Video(models.Model):
    name = models.CharField(max_length=100)
    vid = CloudinaryField('vid', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Card(models.Model):
    name = models.CharField(max_length=50, blank=True)
    creator = models.ForeignKey(User,related_name='cards', on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    images = models.ManyToManyField(Image, related_name='cards', blank=True)
    video = models.ForeignKey(Video, related_name='cards', blank=True, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, related_name='cards', blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    



    
    