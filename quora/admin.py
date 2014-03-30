from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *


class ProfileInline(admin.StackedInline):
    model = AccountModel
    max_num = 1
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(QuestionModel)
admin.site.register(TopicModel)
admin.site.register(CommentModel)
admin.site.register(AnswerModel)

