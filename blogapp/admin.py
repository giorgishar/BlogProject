from django.contrib import admin
from .models import Comment, Feedback, Post

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Feedback)
