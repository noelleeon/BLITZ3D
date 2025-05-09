from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth import get_user_model
from .manager import CustomUserManager

###############################################
# Function name: Members                      #
# Description: creates table that contains usr#
# account information.                        #
# Return value: formed table                  #
###############################################
#https://stackoverflow.com/questions/75121950/how-to-use-authenticate-method-with-abstractuser-model-django
#https://www.geeksforgeeks.org/how-to-use-user-model-in-django/#
#https://www.geeksforgeeks.org/django-models/
class Member(AbstractBaseUser, PermissionsMixin):
    userid = models.AutoField(db_column='userID', primary_key=True, null=False)
    username = models.CharField(max_length=255, unique=True, null=True)
    password = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True)
    favteam = models.CharField(max_length=50, null=True)
    USERNAME_FIELD = 'username'
    objects = CustomUserManager()
    class Meta:
        managed = True
        db_table = 'memberz'

###############################################
# Function name: Members                      #
# Description: creates table that contains all#
# articles created and by whom                #
# Return value: formed table                  #
###############################################
#https://www.geeksforgeeks.org/foreign-keys-on_delete-option-in-django-models/#
class Articles(models.Model):
    userid = models.ForeignKey(Member, on_delete=models.CASCADE)
    author = models.TextField()
    arttitle = models.TextField()
    content = models.TextField(default="content")
    class Meta:
        managed = True
        db_table = 'articlez'

#this stuff was being used for live chat. not implemented right now
#https://www.photondesigner.com/articles/instant-messenger?ref=rdjango-instant-messenger
class Author(models.Model):
    name = models.CharField(max_length=500)

class Message(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
