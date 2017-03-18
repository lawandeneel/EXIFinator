import os
from settings import *
from exifread import process_file
from boto.s3.connection import S3Connection
from boto.s3.bucket import Bucket
from mrq.job import queue_job
from mrq.task import Task
from mrq.context import setup_context, connections, retry_current_job, log

def initialize_jobs(bucket_name):
    setup_context()
    jobs_count = 0
    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
    bucket = Bucket(connection=conn, name=bucket_name)
    for key in bucket.list(): 
        queue_job("tasks.Download", {
                        "bucket_name": bucket_name,
                        "key_name": key.key 
                    }, queue=download_queue)
        jobs_count += 1
    return jobs_count

class Download(Task):
    def run(self, params):

        key_name = params["key_name"]
        _, extension = os.path.splitext(key_name)
        if (extension == ".jpg"):
            conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
            bucket = conn.get_bucket(params["bucket_name"])
            key = bucket.get_key(key_name)
            key.get_contents_to_filename(key_name)
            log.info("Succesfully downloaded file from s3 bucket %s", key_name) 
            queue_job("tasks.Write", {
                            "key_name": key_name 
                        }, queue=write_queue)
        else:
            #TODO handle compressed and other file types
            log.warn("Currently unable to handle file extension type for file %s", key_name) 
            os.remove(key_name)

class Write(Task):
    def run(self, params):
        key_name = params["key_name"]
        log.info("Opening file to extract exif for %s", key_name)

        #Use exifread libary to extract exif data from image file 
        f = open(key_name)
        exif_data = process_file(f, details=False)
        log.info("Extracted exif data")

        #Delete the file
        f.close()
        os.remove(key_name)
        
        #Only extract data needed from libary call to store in database 
        tags = {} 
        for field_name in exif_data:
            field = exif_data[field_name]
            tags[field_name] = {
                'printable': str(field), 
                'tag': field.tag, 
                'field_type': field.field_type, 
                'field_length': field.field_length, 
                'values': str(field.values)}
        
        #Store dictionary of tags into mongodb instance
        log.info("Inserting tags into db") 
        exif_store.insert_one(tags) 
        log.info("Successfully inserted tags into db") 
