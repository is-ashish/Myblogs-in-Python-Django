# Register your models here.
from django.contrib import admin
from .models import *


class KeywordAdmin(admin.ModelAdmin):
    list_display = ("name", "last_scraped")
    search_fields = ('name',)


admin.site.register(Keyword, KeywordAdmin)


class UserKeywordAdmin(admin.ModelAdmin):
    list_display = ("user", "keyword")
    search_fields = ('user__username', "keyword__name")


admin.site.register(UserKeyword, UserKeywordAdmin)
admin.site.register(Code)
admin.site.register(UserCode)
admin.site.register(Opportunity)


class KeywordOpportunityAdmin(admin.ModelAdmin):
    list_display = ("keyword", "opportunity")
    search_fields = ("opportunity__title", "opportunity__url", "keyword__name")


admin.site.register(KeywordOpportunity, KeywordOpportunityAdmin)

