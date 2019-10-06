import yaml
import subprocess
import os
from pathlib import Path

with open("configs.yml",'r') as f:
    stream = yaml.load(f)

FastQ_location = stream["config"]["FastQ_location"]
dna_location = stream["config"]["dna_location"]
output_folder = stream["config"]["output_folder"]
sample_name= stream["config"]["sample_name"]

def execute_command(command, working_dir="/home/ubuntu/"):
    subprocess.run(command.split(), cwd=working_dir)

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

os.rename("/home/ubuntu/cellranger_output/{}/outs/filtered_feature_bc_matrix".format(sample_name), "{}/{}_bc_matrix".format(output_folder, sample_name))
os.rename("/home/ubuntu/cellranger_output/{}/outs/possorted_genome_bam.bam".format(sample_name), "{}/{}.bam".format(output_folder, sample_name))
os.rename("/home/ubuntu/cellranger_output/{}/outs/possorted_genome_bam.bam.bai".format(sample_name), "{}/{}.bam.bai".format(output_folder, sample_name))
os.rename("/home/ubuntu/cellranger_output/{}/{}.rds".format(sample_name, sample_name), "{}/{}.rds".format(output_folder, sample_name))
os.rename("/home/ubuntu/cellranger_output/{}/{}.matrices.rds".format(sample_name, sample_name), "{}/{}.matrices.rds".format(output_folder, sample_name))


# Calling the R script to create CSV files from the .rds outputs

execute_command("Rscipt script.R {}/{}.rds {}/{}_aligned_reads_per_cell.csv".format(output_folder, sample_name, output_folder, sample_name))
