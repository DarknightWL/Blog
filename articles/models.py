from django.db import models

# Create your models here.

class Users(models.Model):
    user_name = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=16)
    create_time = models.DateTimeField(auto_now_add=True)
    change_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name

    class Meta:
        ordering = [ 'user_name']


class Article(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True)
    date_time = models.DateField(auto_now_add=True)
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_time']
