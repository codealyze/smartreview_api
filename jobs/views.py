# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import imports
from django.views.decorators.csrf import csrf_exempt
import os
from jobs.tasks import main, get_task_status, cancel, get_all_tasks
import json

# Create your views here.
threshold = 15
TASK_ID = None
@csrf_exempt
def job_submit(request):
    """
    Execute the main task
    """
    global TASK_ID, threshold
    if get_all_tasks().values()[0]:
            return JsonResponse({"status": "Forbidden, Job in progress."})
        
    try:
        print request.body.decode('utf-8')
        data = json.loads(request.body.decode('utf-8'))
        
        threshold=int(data['threshold_value'])
        isBrowsed = str(data['isBrowsed']).lower()
        print (threshold)
    except:
        #threshold = int(request.POST['threshold_value'])
        threshold = 10
        isBrowsed = "false"
    task = main.delay(threshold=threshold, isBrowsed=isBrowsed)
    TASK_ID = task.id
    
    return JsonResponse({"status": "Job Submitted"})

def get_threshold(request):
    
    return JsonResponse({"threshold":threshold})
def job_status(request):
    """
    Returns current job status
    """
    global TASK_ID
    
    if TASK_ID == None:
        return JsonResponse({"status": "No Jobs running"})
    
    return JsonResponse(get_task_status(TASK_ID))

def job_cancel(request):
    """
    Cancels the job
    """
    global TASK_ID
    cancel(TASK_ID)
    
    return JsonResponse({"status":"Task cancelled"})

def get_all_jobs(request):
    return JsonResponse(get_all_tasks(), safe=False)