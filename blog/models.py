from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Keyword(BaseModel):
    name = models.CharField(max_length=80, unique=True)
    last_scraped = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class UserKeyword(BaseModel):
    keyword = models.ForeignKey(Keyword)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.keyword.name

    class Meta:
        unique_together = (("user", "keyword"),)


class Code(BaseModel):
    code = models.CharField(max_length=255)
    code_id = models.CharField(max_length=80, null=True, blank=True, unique=True)
    last_scraped = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code


class UserCode(BaseModel):
    user = models.ForeignKey(User)
    code = models.ForeignKey(Code)

    def __str__(self):
        return self.user.username + " " + self.code


class Opportunity(BaseModel):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    posted_on = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = (('url', 'title'), )
        verbose_name_plural = 'Opportunities'


class KeywordOpportunity(BaseModel):
    keyword = models.ForeignKey(Keyword)
    opportunity = models.ForeignKey(Opportunity)

    def __str__(self):
        return self.keyword.name + " " + self.opportunity.title

    class Meta:
        verbose_name_plural = 'Keyword Opportunities'


class CodeOpportunity(BaseModel):
    code = models.ForeignKey(Code)
    opportunity = models.ForeignKey(Opportunity)

    def __str__(self):
        return self.code.code + " " + self.opportunity.title

    class Meta:
        verbose_name_plural = 'Code Opportunities'


class UserRequest(BaseModel):
    user = models.ForeignKey(User)
    codes = models.ManyToManyField(Code)
    keywords = models.ManyToManyField(Keyword)
    last_scraped = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'User Requests'


class UserRequestOpportunity(BaseModel):
    user_request = models.ForeignKey(UserRequest, related_name='user_request_opportunities')
    opportunity = models.ForeignKey(Opportunity)

    def __str__(self):
        return self.user_request.id + " " + self.opportunity.title

    class Meta:
        verbose_name_plural = 'User Request Opportunities'