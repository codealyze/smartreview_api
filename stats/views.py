# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from django.shortcuts import render
from dummy_stats import data
# Create your views here.
from system_stats import stats

def get_image_stats(request):
    """
    Image level stats
    """
    try:
        image_name = request.GET['image_name']
        
        return JsonResponse({'response': data[image_name]})
    except Exception, err:
        
        return JsonResponse({'response': str(err)}, safe=False)
    
def get_all(request):
    
    return JsonResponse(stats)