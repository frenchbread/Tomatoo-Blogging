from django.contrib import admin
from models import Post, Save


class PostAdmin(admin.ModelAdmin):
    pass
admin.site.register(Post, PostAdmin)


class LikeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Save, LikeAdmin)
