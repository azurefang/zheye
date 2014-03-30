from django.shortcuts import render
from django.http import HttpResponse
from quora.models import *

import simplejson


def ajax_topic_json(request):
    all_topics = [i.tName for i in TopicModel.objects.all()]
    result = {}
    '''
    result['topic'] = all_topics
    result = simplejson.dumps(result)
    '''
    result = simplejson.dumps(all_topics)
    return HttpResponse(result, mimetype="application/json")

