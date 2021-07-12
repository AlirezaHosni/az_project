from django.contrib import admin
from .models import Chat,Message,Chat_User
# Register your models here.


class ChatAdmin(admin.ModelAdmin):
    list_display = ['id','title']


admin.site.register(Chat,ChatAdmin)
admin.site.register(Chat_User)
admin.site.register(Message)