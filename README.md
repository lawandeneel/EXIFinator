# EXIFinator
This is a python tool to extract exif data from images on Amazon S3 buckets, and store it in a mongodb data source. This implementation uses the MRQ python library. MRQ is a distributed task queue that uses redis as a queueing layer, mongodb to store metadata and gevent as a concurrency library. Each image key in the s3 bucket is queued as its own task. There are 2 task queues, one for downloading the image, and one for processing and writing it to a mongodb collection. Once an image is downloaed, it is queued in the process/write. It uses a third party python library called exif-py to extract exif data from the jpg's. Lastly it uses mongodb as it's data source to store the exif data. Additionally, there is an optional node.js based api server to serve the exif data from the mongodb store through a REST based api. I decided to use mrq to allow this application to be useful in a more scaled environment. MRQ allows not only delegation of various tasks, but also the individual monitoring of speicific workers and tasks. With the dashboard server, you can see the current queus, as well as all failed tasks and their logs, and requeue them manually for processing. 

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [API](#api)
- [Built With](#built-with)
- [To Do](#to-do)

## Requirements
* Python 2.7
* Redis 3.2
* Mongodb 3.4.2

## Setup

Run `./setup.sh`
* This script pip installs all python packages needed
* Also starts redis and mongo servers if you haven't already
* `mrq-config.py` contains all the configurations for the mrq (number of greentlet threads per worker, queue names, dashboard port etc)

Your AWS Access Key / Secret Key, as well as any additional S3 bucket names should be added to the `settings.py` file.
  
## Usage
### Start MRQ Workers
Run `./start_workers.sh` to start individual mrq-workers. This file can be configured to add/remove worker processes and configure which task queue(s) they are listening to. It will also start the mrq-dashboard server which shows queue/worker status, and pending tasks and their status and can be accessed at http://localhost:5555/.
* The syntax to start a worker is `mrq-worker <queue-name>, <another-queue-name>`
* Right now there are 2 queues, the download queue and the write queue
* There are 2 workers, one that is reading from both the download queue, and one that only takes off the write queue
* The max amount of greenlets to spawn per worker is defined in `mrq-config.py` in the field `GREENLETS = 100`
* Currently there are 100 greenlets per worker (but can be played with to optimize I/O efficiency)

### Start batching jobs
Run `./run.sh` which will batch all files in the s3 buckets specified in `settings.py` to be added as MRQ Tasks. The workers will take care of the rest. The worker, queue, and tasks statuses (including all failed tasks) and logs can all be viewed in the mrq-dashboard. More S3 buckets can be added/removed later in settings file

### Monitor Logs
All logs for workers/servers are under the `logs/` directory

## API
I originally used this for testing, but thought I'd include it in the repo. If you have node.js and npm installed you can go to the `api/` directory and run:
1. `npm install`
2. `node server`
And there start an active api server running that allows you to access the mongo database from your browser at http://localhost:3001.

#### Examples
1. You can use http://localhost:3001/waldo/exif_data to see the collection that all the exif data is stored in
2. You can use mongo queries with the api to query that collection with http://localhost:3001/waldo/exif_data?query={"Image%20Make.printable":"SONY"}

## Built With
* MRQ - http://mrq.readthedocs.io/en/latest/
* exif-py - https://github.com/ianare/exif-py
* boto s3 library - http://boto.cloudhackers.com/en/latest/ref/s3.html

## To Do
All in all, I had a lot of fun working on this project. I have learned a lot about new libraries and technologies and wish i did have more time to make this a better product. Here are some things to do if I had more time:
* Add specific server/port and authentication configuration. Right now everything is local, and all authentication is open.
* Tinker with the amount of greenlets per worker and amount of mrq-workers spawned to see how to most efficiently use the gevent library to maximize I/O utilization
* Using python limits the ability to truly multithread, so consider using golong or c++ to further optimize efficiency
* Add a more useful api, even to maybe push processing of a s3 bucket on an api call
* Add a GUI on top of the api in order to see/query the exif data
* Add better unit tests / automated testing framework
