from pymongo import MongoClient

#AWS Access Credentials
AWS_ACCESS_KEY = <AWS_ACCESS_KEY> 
AWS_SECRET_KEY = <AWS_SECRET_KEY> 

#List of S3 Buckets to grab from
s3_bucket_names = [
                    "waldo-recruiting",
                  ]

#Queue names to define for mrq
download_queue = "download"
write_queue = "write"

#db store for exif data
exif_store = MongoClient().waldo.exif_data
