import yaml
import subprocess
import os
from pathlib import Path
import boto3 
import boto3 
import logging
from botocore.exceptions import ClientError
import tarfile


with open("configs.yml",'r') as f:
    stream = yaml.load(f)

FastQ_location = stream["config"]["FastQ_location"]
dna_location = stream["config"]["dna_location"]
output_folder = stream["config"]["output_folder"]
sample_name= stream["config"]["sample_name"]
bucket_name = stream["config"]["bucket_name"]

def execute_command(command, working_dir="/home/ubuntu/BioMage-workload/count_matrix_automation"):
    subprocess.run(command.split(), cwd=working_dir)

def check_bucket_existance(bucket_name):
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        if bucket_name in bucket['Name']:
            return 1

def make_tarfile(output_file, source_dir):
    with tarfile.open(output_file, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
def create_bucket(name):
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket = name, CreateBucketConfiguration={
        'LocationConstraint': 'eu-west-1'})

# creating sam files
execute_command("/home/ubuntu/cellranger-3.1.0/cellranger count --id={} \
                   --nosecondary \
                   --transcriptome={} \
                   --fastqs={} \
                   --sample={} \
                   --expect-cells=1000"\
                   .format(sample_name, dna_location, FastQ_location, sample_name), "/home/ubuntu/cellranger_output")

check_folder_existance = Path(output_folder)
if not check_folder_existance.is_dir():
    os.mkdir(output_folder)

#launching dropest

execute_command("sudo /home/ubuntu/dropEst-0.8.6/build/dropest -V -o {} -L eiEIBA -f \
                -g /home/ubuntu/refdata-cellranger-GRCh38-3.0.0/genes/genes.gtf \
                -c /home/ubuntu/dropEst-0.8.6/data/post_cellranger_analysis/config-10x-cellranger.xml \
                /home/ubuntu/cellranger_output/{}/outs/possorted_genome_bam.bam ".format(sample_name, sample_name), "/home/ubuntu/cellranger_output/{}".format(sample_name))

#moving cellranger and dropest files into the output folder
'''
os.rename("/home/ubuntu/cellranger_output/{}/outs/filtered_feature_bc_matrix".format(sample_name), "{}/{}_bc_matrix".format(output_folder, sample_name))
os.rename("/home/ubuntu/cellranger_output/{}/outs/possorted_genome_bam.bam".format(sample_name), "{}/{}.bam".format(output_folder, sample_name))
os.rename("/home/ubuntu/cellranger_output/{}/outs/possorted_genome_bam.bam.bai".format(sample_name), "{}/{}.bam.bai".format(output_folder, sample_name))
os.rename("/home/ubuntu/cellranger_output/{}/{}.rds".format(sample_name, sample_name), "{}/{}.rds".format(output_folder, sample_name))
os.rename("/home/ubuntu/cellranger_output/{}/{}.matrices.rds".format(sample_name, sample_name), "{}/{}.matrices.rds".format(output_folder, sample_name))
'''
# Calling the R script to create CSV files from the .rds outputs

execute_command("Rscript script_full.R {} {}".format(sample_name, output_folder))

#Uploading the output folder to S3 bucket

make_tarfile("/home/ubuntu/{}.tar.gz".format(sample_name), output_folder)
if not check_bucket_existance(bucket_name):
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration = {
                        'LocationConstraint' : 'eu-west-1'
                         })

with open("/home/ubuntu/{}.tar.gz".format(sample_name), "rb") as f:
    s3.upload_fileobj(f, bucket_name, "{}.tar.gz".format(sample_name))

