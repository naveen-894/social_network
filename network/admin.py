from django.contrib import admin
from .models import User,FriendRequest
# Register your models here.

admin.site.register(FriendRequest)
admin.site.register(User)