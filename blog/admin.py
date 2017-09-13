# Register your models here.
from django.contrib import admin
from .models import *


admin.site.register(Keyword)
admin.site.register(UserKeyword)
admin.site.register(Code)
admin.site.register(UserCode)
admin.site.register(Opportunity)
admin.site.register(KeywordOpportunity)

