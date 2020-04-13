from django.contrib import admin
from .models import Post, Tag, MessageChat, Profile, Friend

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(MessageChat)
admin.site.register(Profile)
admin.site.register(Friend)