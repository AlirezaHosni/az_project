
from django.contrib import admin
from .models import Notifiaction, Email_Verification, Reservation, Advisor_Document , Invitation, Advisor, User, Request, Rate, Advisor_History

# Register your models here.
admin.site.register(User)
admin.site.register(Advisor)
admin.site.register(Request)
admin.site.register(Rate)
admin.site.register(Advisor_History)
admin.site.register(Notifiaction)
admin.site.register(Reservation)
admin.site.register(Advisor_Document)
admin.site.register(Invitation)
admin.site.register(Email_Verification)
