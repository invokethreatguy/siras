import click

from modules.smokers import SGopenSmoker, AWSadminSmoker, CTrailSmoker, S3PublicSmoker
from modules.welcome import home

@click.command()
@click.option("--sg", is_flag=True, help="Create a security group open to 0.0.0.0/0")
@click.option("--ua", is_flag=True, help="Create a user administrator into AWS and nuked it")
@click.option("--ctr", is_flag=True, help="Test AWS Cloudtrail trail creation and deletion")
@click.option("--s3", is_flag=True, help="Create a public s3 bucket")



def main(sg, pa, ua, aca, ctr, s3):

    if sg:
        SGopenSmoker()
    if ua:
        AWSadminSmoker()
    if ctr:
        CTrailSmoker()
    if s3:
        S3PublicSmoker()


if __name__=='__main__':
    home()
    print('Security Incident Response Automated Simulations (SIRAS) \n this is a simple scripting way to test different security alerts\n in order to generate smoke events and test your alerts. This script generates real resources into AWS \n https://github.com/Stuxend/siras  \n #### --help for more info  ####')
    main()