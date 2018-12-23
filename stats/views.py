# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from django.shortcuts import render
from dummy_stats import data, return_formatted_data
# Create your views here.
from system_stats import all_stats

def get_image_stats(request):
    """
    Image level stats
    """
    try:
        image_name = request.GET['image_name']
        
        response = data(image_name)
        return JsonResponse({'response': response})
    except KeyError:
        print ("From db")
        response = return_formatted_data(image_name)
        return JsonResponse({'response': response})
    except Exception, err:
        
        return JsonResponse({'response': str(err)}, safe=False)
    
def get_all(request):
    
    return JsonResponse(all_stats())