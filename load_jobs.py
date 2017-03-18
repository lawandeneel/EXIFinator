from settings import *
from tasks import initialize_jobs

for bucket_name in s3_bucket_names:
    jobs_count = initialize_jobs(bucket_name)
    print "Queued {} jobs from S3 bucket: {}".format(jobs_count, bucket_name)
