from django.contrib import admin
from django.contrib.auth.models import User
from .models import Question, Answer, Image,Profile,Anon
from forum.models import Post, Comment 
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    list_display=['body', 'active']

admin.site.register(Profile)
admin.site.register(Question, QuestionAdmin)
admin.site.register([Answer,Image])
# Register your models here.

admin.site.register(Anon)
