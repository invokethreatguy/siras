import boto3
import logging
import datetime
import os
import sys
import json
import argparse
import urllib3
from io import BytesIO
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth


##### define standard configurations ####

# Setup the main app logger
app_log = logging.getLogger("app")
app_log.setLevel(level=logging.INFO)
urllib3.disable_warnings()

# Setup the verbose logger
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
tracer = logging.getLogger('elasticsearch')
tracer.setLevel(logging.WARN)

#Setup AWS ElasticAuth.
awsauth = AWS4Auth(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'], os.environ['AWS_REGION'], 'es',
                   session_token=os.environ['AWS_SESSION_TOKEN'])


#Setup timestamp
iso_now_time = datetime.datetime.now().isoformat()

#Setup for ELK general connection
def sendToELK(data, simulation, statusSimulation):
        index_name = 'siras'
        elk_node = os.environ['elk_node']
        es = Elasticsearch(
                hosts=[{'host': elk_node, 'port': 443}],
                http_auth=awsauth,
                use_ssl=True,
                verify_certs=False,
                connection_class=RequestsHttpConnection,
                timeout=60,
                max_retries=10,
                retry_on_timeout=True
                )
        eventInformation = {
        'evenTime': iso_now_time,
        'simulation': simulation,
        'eventInfo': data,
        'simulationStatus': statusSimulation
        }
        es.index(index=index_name, body=eventInformation)
