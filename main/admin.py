from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Publication, Comment, Mark


admin.site.register(User, UserAdmin)
admin.site.register(Publication)
admin.site.register(Comment)
admin.site.register(Mark)