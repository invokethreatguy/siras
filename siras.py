from modules.smokers.SGopenSmoker import SGopenSmoker
from modules.smokers.PanAuthSmoker import PanAuthSmoker
from modules.smokers.AWSadminSmoker import AWSadminSmoker
from modules.smokers.awsConsoleAuthSmoker import awsConsoleAuthSmoker
from modules.smokers.CTrailSmoker import CTrailSmoker
from modules.smokers.S3PublicSmoker import S3PublicSmoker
from modules.smokers.EBSPublicSmoker import EBSPublicSmoker
from modules.smokers.TransitSmoker import TransitSmoker
from modules.smokers.test_logger import test_message
from modules.welcome import home
from modules.logs import siras_logger, siras_s3_logger

import argparse

def main(args):
    data = "siras"
    if args.get('bucket') == True:
        logger = siras_s3_logger('SIRAS')
        if args.get('smoker') == 'test':
            test_message()
        if args.get('smoker') == 'sg':
            SGopenSmoker()
        if args.get('smoker') == 'pa':
            PanAuthSmoker()
        if args.get('smoker') == 'au':
            AWSadminSmoker()
        if args.get('smoker') == 'aca':
            awsConsoleAuthSmoker()
        if args.get('smoker') == 'ctr':
            CTrailSmoker()
        if args.get('smoker') == 's3p':
            S3PublicSmoker()
        if args.get('smoker') == 'esb':
            EBSPublicSmoker()
        if args.get('smoker') == 'all':
            SGopenSmoker()
            PanAuthSmoker()
            AWSadminSmoker()
            awsConsoleAuthSmoker()
            CTrailSmoker()
            S3PublicSmoker()
            EBSPublicSmoker()
    else:
        logger = siras_logger('SIRAS')
        if args.get('smoker') == 'test':
            test_message()
        if args.get('smoker') == 'sg':
            SGopenSmoker()
        if args.get('smoker') == 'pa':
            PanAuthSmoker()
        if args.get('smoker') == 'au':
            AWSadminSmoker()
        if args.get('smoker') == 'aca':
            awsConsoleAuthSmoker()
        if args.get('smoker') == 'ctr':
            CTrailSmoker()
        if args.get('smoker') == 's3p':
            S3PublicSmoker()
        if args.get('smoker') == 'esb':
            EBSPublicSmoker()
        if args.get('smoker') == 'all':
            SGopenSmoker()
            PanAuthSmoker()
            AWSadminSmoker()
            awsConsoleAuthSmoker()
            CTrailSmoker()
            S3PublicSmoker()
            EBSPublicSmoker()

if __name__=='__main__':
    home()
    print('Security Incident Response Automated Simulations (SIRAS) \n this is a simple scripting way to test different security alerts\n in order to generate smoke events and test alerts in your SIEM. \n https://github.com/Stuxend/siras')
    siras_parser = argparse.ArgumentParser()
    siras_parser.version = 'version: 2.0 - stuxned - https://github.com/Stuxend/siras'
    siras_parser.add_argument('-s',help='smoker to run' ,dest='smoker', type=str, required=True)
    siras_parser.add_argument('-b',help='save the results into a bucket' ,dest='bucket', type=bool, required=False)
    args =  siras_parser.parse_args()
    event_map = {'smoker': args.smoker, 'bucket': args.bucket}
    main(event_map)