
from django.contrib import admin
from .models import Advisor, User, Request, Rate, Advisor_History

# Register your models here.
admin.site.register(User)
admin.site.register(Advisor)
admin.site.register(Request)
admin.site.register(Rate)
admin.site.register(Advisor_History)
