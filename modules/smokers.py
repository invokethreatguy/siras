import boto3
import json
import logging
import datetime
import os
import sys
from io import BytesIO
from botocore.exceptions import ClientError
import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from .loggerELK import sendToELK

##### define standard configurations ####

# Setup the verbose logger
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Setup timestamp
iso_now_time = datetime.datetime.now().isoformat()

#smoker for security open group
def SGopenSmoker():
    TAG = [
        {"Key": "Department", "Value": "engineering"},
        {"Key": "DataClassification", "Value": "SIRAS"},
        {"Key": "ComplianceScope", "Value": "none"},
        {"Key": "Purpose", "Value": "SIRAS"}
    ]
    descript = ' SIRAS smoke security group ' + iso_now_time
    name = ' SIRAS_smoke_group'
    ec2 = boto3.client('ec2')
    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
    try:
        response = ec2.create_security_group(GroupName=name,
                                            Description=descript,
                                            VpcId=vpc_id)
        security_group_id = response['GroupId']
        logger.info(' Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ], )
        logger.info(' Ingress Successfully Set %s' % data)
    except ClientError as e:
        logger.info(e)
    try:
        response = ec2.delete_security_group(GroupId=security_group_id)
        logger.info(' Security Group Deleted')
    except ClientError as e:
        logger.info(e)

#smoker for loca aws admin creation
def AWSadminSmoker():
    TAG = [
        {"Key": "Department", "Value": "engineering"},
        {"Key": "DataClassification", "Value": "SIRAS"},
        {"Key": "ComplianceScope", "Value": "none"},
        {"Key": "Purpose", "Value": "SIRAS"}
    ]
    descript = ' SIRAS smoke iam localuser ' + iso_now_time
    name = ' SIRAS_smoke_user'
    iam = boto3.client('iam')
    logger.info(' Creating the user SIRAS-ADMIN %s' % iso_now_time)
    response = iam.create_user(UserName='SIRAS-ADMIN',Tags=TAG)
    user_id = response['User']['UserId']
    user_arn = response['User']['Arn']
    logger.info(' Attaching the user to "AdministratorAccess" policy %s' % iso_now_time)
    iam.attach_user_policy(
        UserName = 'SIRAS-ADMIN', 
        PolicyArn='arn:aws:iam::aws:policy/AdministratorAccess'
    )
    logger.info(' User Created: %s' % iso_now_time + " ID: " + user_id + " ARN: " + user_arn)
    logger.info(' Rollback now %s' % iso_now_time)
    iam.detach_user_policy(
        UserName = 'SIRAS-ADMIN', 
        PolicyArn='arn:aws:iam::aws:policy/AdministratorAccess'
    )
    iam.delete_user( UserName='SIRAS-ADMIN')
    logger.info(' DONE %s' % iso_now_time)


#smoker for cloudtrail (creation and delete)
def CTrailSmoker():
    name = "SIRAS_smoke_cloudtrail"
    bucket_name = "siras-smoke-cloudtrail"
    TAG = [
        {"Key": "Department", "Value": "engineering"},
        {"Key": "DataClassification", "Value": "SIRAS"},
        {"Key": "ComplianceScope", "Value": "none"},
        {"Key": "Purpose", "Value": "SIRAS"}
    ]
    # policy for bucket
    policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "AWSCloudTrailAclCheck20150319",
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "cloudtrail.amazonaws.com"
                        },
                        "Action": "s3:GetBucketAcl",
                        "Resource": "arn:aws:s3:::siras-smoke-cloudtrail"
                    },
                    {
                        "Sid": "AWSCloudTrailWrite20150319",
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "cloudtrail.amazonaws.com"
                        },
                        "Action": "s3:PutObject",
                        "Resource": "arn:aws:s3:::siras-smoke-cloudtrail/*",
                        "Condition": {
                            "StringEquals": {
                                "s3:x-amz-acl": "bucket-owner-full-control"
                            }
                        }
                    }
                ]
            }
    # Create s3 bucket
    s3 = boto3.client('s3')
    logger.info("Creating bucket named: "+bucket_name+" "+iso_now_time)
    s3_smoke = s3.create_bucket(ACL='private',Bucket=bucket_name)
    # set bucketpolicy
    bucket_policy = json.dumps(policy)
    s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
    # Create cloudtrial
    logger.info("Creating cloudtrail named: "+name+" "+iso_now_time)
    client = boto3.client('cloudtrail')
    response = client.create_trail(Name=name,S3BucketName=bucket_name)
    logger.info("detailed info: "+str(response))
    logger.info("Starting the trail: "+iso_now_time)
    response = client.start_logging(Name=name)
    logger.info("detailed info: "+str(response))
    logger.info(' Deleting trail now %s' % iso_now_time)
    response = client.delete_trail(Name=name)
    logger.info("detailed info: "+str(response))
    logger.info(' Deleting s3 now %s' % iso_now_time)
    # delete objects
    s3o = boto3.resource('s3')
    bucket = s3o.Bucket(bucket_name)
    bucket.objects.all().delete()
    # delete bucket now
    delete_bucket = s3.delete_bucket(Bucket=bucket_name)
    logger.info("detailed info: "+str(delete_bucket))
    logger.info(iso_now_time +  ' done!')


#smoker for s3 public (creation and delete)
def S3PublicSmoker():
    bucket_name = "siras-smoke-s3public-nuke"
    TAG = [
        {"Key": "Department", "Value": "engineering"},
        {"Key": "DataClassification", "Value": "SIRAS"},
        {"Key": "ComplianceScope", "Value": "none"},
        {"Key": "Purpose", "Value": "SIRAS"}
    ]
    # Create s3 bucket
    s3 = boto3.client('s3')
    logger.info("Creating bucket named: "+bucket_name+" "+iso_now_time)
    s3_smoke = s3.create_bucket(ACL='public-read',Bucket=bucket_name)
    logger.info("detailed info creation: "+str(s3_smoke))
    # delete objects
    s3o = boto3.resource('s3')
    bucket = s3o.Bucket(bucket_name)
    bucket.objects.all().delete()
    # delete bucket now
    delete_bucket = s3.delete_bucket(Bucket=bucket_name)
    logger.info("detailed info delete: "+str(delete_bucket))
    logger.info(iso_now_time +  ' done!')