from django.db import models
from django.contrib.auth.models import User


class UserKeyword(models.Model):
    keyword=models.CharField(max_length=80)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.keyword

    class Meta:
        unique_together = (("user", "keyword"),)


class Code(models.Model):
    code=models.CharField(max_length=80)

    def __str__(self):
        return self.code



class UserCode(models.Model):
    user=models.ForeignKey(User)
    code=models.ForeignKey(Code)

