from django.contrib import admin
from .models import Publication, Comment, Mark


admin.site.register(Publication)
admin.site.register(Comment)
admin.site.register(Mark)