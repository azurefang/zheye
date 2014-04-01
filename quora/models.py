from django.db import models
from django.contrib.auth.models import User


class AccountModel(models.Model):

    aUser = models.OneToOneField(
        User, primary_key=True, related_name='account')
    aDomain = models.CharField(max_length=30)
    aIntroduction = models.CharField(max_length=30, blank=True)
    aHeadImage = models.ImageField(
        upload_to='img/head/', default='img/head/666b0abfc_l.jpg')

    def __unicode__(self):
        return self.aUser.username


class TopicModel(models.Model):

    tName = models.CharField(max_length=20)
    #tDescription = models.CharField(max_length=100, blank=True, null=True)
    tFollower = models.ManyToManyField(
        AccountModel, related_name='followed_topic', null=True, blank=True)
    tHeadImage = models.ImageField(
        upload_to='img/topic/', default='img/topic/e82bab09c_m.jpg')

    def __unicode__(self):
        return self.tName


class QuestionModel(models.Model):

    qId = models.IntegerField()
    qTitle = models.CharField(max_length=30)
    qTime = models.DateTimeField()
    qContent = models.TextField()
    qOwner = models.ForeignKey(AccountModel, related_name='questioner')
    qFollower = models.ManyToManyField(
        AccountModel, related_name='followed_questions', null=True, blank=True)
    qTopic = models.ManyToManyField(
        TopicModel, related_name='related_questions')

    def __unicode__(self):
        return self.qTitle


class AnswerModel(models.Model):

    aTime = models.DateTimeField()
    aOwner = models.ForeignKey(AccountModel)
    aQuestion = models.ForeignKey(QuestionModel, related_name='answers')
    aContent = models.TextField()
    aLiker = models.ManyToManyField(
        AccountModel, related_name='liked_answer', null=True)
    aHater = models.ManyToManyField(
        AccountModel, related_name='hated_answer)', null=True)
    aCollector = models.ManyToManyField(
        AccountModel, related_name='collected_answer', null=True)

    def __unicode__(self):
        return self.aOwner.aUser.username


class CommentModel(models.Model):

    cTime = models.DateTimeField()
    cContent = models.TextField()
    cOwner = models.ForeignKey(AccountModel, related_name='commenter')
    cAnswer = models.ForeignKey(AnswerModel, related_name='comments')
    cLiker = models.ManyToManyField(AccountModel, related_name='liked_comment', blank=True,
                                    null=True)
    cCommentFather = models.ForeignKey(
        'self', blank=True, null=True, default=None, related_name='father')
