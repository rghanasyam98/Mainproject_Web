from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# Register your models here.
from myapp.models import Myuser, Loan, Chit, News, Auction

admin.site.register(Myuser, UserAdmin)
admin.site.register(Loan)
admin.site.register(Chit)
admin.site.register(News)
admin.site.register(Auction)



