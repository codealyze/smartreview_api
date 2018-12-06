from celery.decorators import task
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from smartreview_api.celery import app
import time
from celery.task.control import revoke
from smartreviewdata_app import OD
from celery import current_task
from smartreviewdata_app.SIGNATURE import match_query
from smartreviewdata_app.DB_mysql import DB
from smartreviewdata_app.utils import publish_message, make_blob_public
import subprocess
import fnmatch
import numpy as np
import os


logger = get_task_logger(__name__)

@task(name="Fraud Detection")
def main(threshold=15, isBrowsed='false'):
    
    if isBrowsed == 'true':
        current_task.update_state(state='PROGRESS',
                meta={'stage': 'Pulling Files'})
        #subprocess.call("rm ~/.gsutil/credstore", shell=True)
        subprocess.call("gsutil cp -c gs://ximistorage/testimages/* data/testimages/", shell=True)
        
    current_task.update_state(state='PROGRESS',
                meta={'stage': 'Object Detection'})
    publish_message('progress', 'Stage', 'Object Detection')
    # Run Object Detection and create image parts
    logger.info("\nObject Detection Running and Exporting into imageparts...")
    OD.predict_boxes("data/testimages")
    
    
    #Push xmls to cloud storage
    #print ("\nPushing XMLs to cloud storage ...")
    #subprocess.call("gsutil mv testxmls/* gs://smartreviewdata/testxmls/", shell=True)
    
    # Calculate Rows data using OCR
    current_task.update_state(state='PROGRESS',
                meta={'stage': 'Extracting Info'})
    publish_message('progress', 'Stage', 'Extracting Info')
    logger.info("\nRows being calculated for the imageparts...")
    
    #Init database here so that connection is never broken
    database = DB("root", "root", "srlogs")
    sno = database.query('SELECT max(sno) from {}'.format(database.table))[0][0]
    
    from smartreviewdata_app import OCR
    ROWS = OCR.calculate_data(sno, 'data/imageparts', train_flag='False', source='images')
    
    
    current_task.update_state(state='PROGRESS',
                meta={'stage': 'Matching records'})
    publish_message('progress', 'Stage', 'Matching Records')
    logger.info("\nMatching with BIGQUERY records and pushing...")

    match_query(ROWS, database, threshold)

    #Commiting database
    logger.info("\n Database commiting...")
    database.cnx.commit()
    
    current_task.update_state(state='PROGRESS',
                meta={'stage': 'Wrapping up'})
    publish_message('progress', 'Stage', 'Wrapping up')
    #Push imageparts to cloud storage 
    logger.info("\nPushing imageparts to global_imageparts ...")
    subprocess.call("cp -r data/imageparts/* data/global_imageparts/", shell=True)
    subprocess.call("rm -r data/imageparts/*", shell=True)
    subprocess.call("gsutil cp -r data/predictions/fraud gs://ximistorage/predictions/", shell=True)
    subprocess.call("gsutil acl ch -u AllUsers:R gs://ximistorage/predictions/fraud/*", shell=True)
    
    publish_message('progress', 'Stage', 'Finished')
    #Clear testimages
    #subprocess.call("rm -r testimages", shell=True)
    return "Job Complete!"

def get_task_status(task_id):
 
    # If you have a task_id, this is how you query that task 
    task = AsyncResult(task_id)
 
    status = task.status
    progress = 0
 
    if status == u'SUCCESS':
        progress = 100
    elif status == u'FAILURE':
        progress = 0
    elif status == 'PROGRESS':
        progress = task.info["stage"]
 
    return {'status': status, 'stage': progress}

def cancel(task_id):
     revoke(task_id, terminate=True)
     
     app.control.purge()
    
def get_all_tasks():
    i = app.control.inspect()
    return i.active()