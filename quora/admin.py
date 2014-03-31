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


class TopicModelAdmin(admin.ModelAdmin):
    list_display = ('tName',)
    list_select_related = ('tName',)


class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ('qTitle', 'qTime', 'qOwner', )


class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('cOwner',)


class AnswerModelAdmin(admin.ModelAdmin):
    list_display = ('aOwner', )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(QuestionModel, QuestionModelAdmin)
admin.site.register(TopicModel, TopicModelAdmin)
admin.site.register(CommentModel, CommentModelAdmin)
admin.site.register(AnswerModel, AnswerModelAdmin)

