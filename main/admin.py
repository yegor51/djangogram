from django.contrib import admin
from .models import User, Publication, Comment, Mark


admin.site.register(User)
admin.site.register(Publication)
admin.site.register(Comment)
admin.site.register(Mark)