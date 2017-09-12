# Register your models here.
from django.contrib import admin
from .models import UserKeyword
from .models import UserCode,Code


admin.site.register(UserKeyword)
admin.site.register(Code)
admin.site.register(UserCode)

