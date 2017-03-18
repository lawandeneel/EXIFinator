from pymongo import MongoClient

#AWS Access Credentials
AWS_ACCESS_KEY = "AKIAIITYFFKIZOPWNZLQ" 
AWS_SECRET_KEY = "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" 

#List of S3 Buckets to grab from
s3_bucket_names = [
                    "waldo-recruiting",
                  ]

#Queue names to define for mrq
download_queue = "download"
write_queue = "write"

#db store for exif data
exif_store = MongoClient().waldo.exif_data
