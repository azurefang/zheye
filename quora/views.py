import re
from datetime import datetime

from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render_to_response

from .models import *

import pinyin

from .forms import *
from django.shortcuts import render, redirect
from django.core.context_processors import csrf

def index(request):
    #if request.user
    pass

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_user = form.save()
            new_user.first_name = cd['first_name']
            new_user.last_name = cd['last_name']
            new_user.email = cd['username']
            new_user.save()
            aDomain = pinyin.get('-'.join(cd['first_name'] + cd['last_name']))
            regex = '^' + aDomain + '(-\d+)?'
            same_name = AccountModel.objects.filter(
                aDomain__regex=regex).order_by('-aUser__id')
            if not same_name:
                p = AccountModel(aUser=new_user, aDomain=aDomain)
            else:
                the_last = same_name[0].aDomain
                regex1 = re.compile('^' + aDomain + '$')
                regex2 = re.compile('^' + aDomain + '-(\d+)')
                match1 = re.match(regex1, the_last)
                match2 = re.match(regex2, the_last)
                if match1:
                    p = AccountModel(aUser=new_user, aDomain=aDomain + '-1')
                else:
                    match2.group(1)
                    p = AccountModel(
                        aUser=new_user, aDomain=aDomain + '-' + str(int(match2.group(1)) + 1))
            p.save()
            username = cd['username']
            password = cd['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/ask_question")
    else:
        if request.user:
            return redirect("/")
        form = UserCreationForm()
        ctx = {'form': form}
        ctx.update(csrf(request))
        return render(request, "register.html", ctx)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect("/")
        else:
            return redirect("/admin")
    else:
        if request.user:
            return redirect("/")
        form = LoginForm()
        ctx = {'form': form}
        ctx.update(csrf(request))
        return render(request, "login.html", ctx)


def display_topic(request, tId):

    topic = TopicModel.objects.get(id=tId)
    if not topic:
        raise Http404
#    return render_to_response('display_topic.html', {'user': request.user, 'topic': topic})
    return render(request, 'display_topic.html', {'topic': topic})


def display_account(request, aDomain):
    account = AccountModel.objects.get(aDomain=aDomain)
    if not account:
        raise Http404
    return render(request, "display_account.html", {'account': account})


def display_question(request, qId):
    question = QuestionModel.objects.get(qId=qId)
    try:
        asked = len(question.answers.all().filter(aOwner=request.user))
    except KeyError:
        asked = 0
    if not question:
        raise Http404
    if request.method == 'POST':
        form = request.POST
        aTime = datetime.now()
        aOwner = request.user
        aContent = form.get('answer')
        aQuestion = QuestionModel.objects.get(qId=qId)
        new_answer = AnswerModel(aTime=aTime, aOwner=aOwner.account, aContent=aContent, aQuestion=aQuestion)
        new_answer.save()
        return render(request, 'display_question.html', {'question': question, 'asked': asked})
    else:
        ctx = {'question': question, 'asked': asked}
        ctx.update(csrf(request))
        return render(request, "display_question.html", ctx)


def followed_topics(request):
    account = request.user.account
    return render(request, "followed_topics.html", {'account': account})


def show_topics(request):
    pass



def ask_question(request):
    if request.method == 'POST':
        form = request.POST
        qTitle = form.get('title')
        qContent = form.get('content')
        qTime = datetime.now()
        qOwner = request.user
        new_question = QuestionModel(qId = 0, qTitle=qTitle, qContent=qContent, qTime=qTime, qOwner=qOwner.account)
        new_question.save()
        new_question.qId += new_question.id + 19550224
        topics = form.get('hidden-topics').split(',')
        for i in topics:
            try:
                TopicModel.objects.get(tName=i)
            except TopicModel.DoesNotExist:
                TopicModel(tName=i).save()
            new_question.qTopic.add(TopicModel.objects.get(tName=i))
        new_question.qFollower.add(request.user.account)
        new_question.save()
        return redirect('/question/{}'.format(new_question.qId))
    else:
        c = {}
#        c.update(csrf(request))
        return render(request, "ask_question.html", c)
