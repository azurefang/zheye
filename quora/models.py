import hashlib

from django.db import models


class AccountModel(models.Model):

    uName = models.CharField(max_length=20)
    uPasswd = models.CharField(max_length=50)
    uIs_active= models.IntegerField(blank=True)
    uIntroduction = models.CharField(max_length=30)

    def __unicode__(self):
        return self.uName

    def is_authenticated(self):
        return True

    def hashed_passwd(self, passwd=None):
        if not passwd:
            return self.uPasswd
        else:
            return hashlib.md5(passwd).hexdigest()

    def check_passwd(self, passwd):
        if self.hashed_passwd(passwd) == self.uPasswd:
            return True
        return False


class TopicModel(models.Model):

    tName = models.CharField(max_length=20)
    tFollower = models.ManyToManyField(AccountModel, related_name='followed_topic')


class QuestionModel(models.Model):

    qTitle = models.CharField(max_length=30)
    qTime = models.DateTimeField()
    qContent = models.TextField()
    qOwner = models.ForeignKey(AccountModel, related_name='questioner')
    qFollower = models.ManyToManyField(AccountModel, related_name='followed_question')
    qTopic = models.ManyToManyField(TopicModel, related_name='related_question')


class AnswerModel(models.Model):

    aTime = models.DateTimeField()
    aOwner = models.ForeignKey(AccountModel)
    aQuestion = models.ForeignKey(QuestionModel)
    aLiker = models.ManyToManyField(AccountModel, related_name='liked_answer')
    aHater = models.ManyToManyField(AccountModel, related_name='hated_answer)')
    aCollector = models.ManyToManyField(AccountModel, related_name='collected_answer')


class CommentModel(models.Model):

    cTime = models.DateTimeField()
    cOwner = models.ForeignKey(AccountModel, related_name='commenter')
    cAnswer = models.ForeignKey(AnswerModel, related_name='answer')
    cLiker = models.ManyToManyField(AccountModel, related_name='liked_comment')
    cCommentFather = models.ForeignKey('self', blank=True, null=True, default=None, related_name='father')
