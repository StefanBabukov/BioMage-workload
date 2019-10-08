# BioMage-workload

This project's goal is to automate the process of converting fastq reads files into .bam files which are then further converted to .rds matrices with gene information. The automation_script.py script also creates CSV files with the final information, zips the files and uploads them to AWS Bucket storage.

The aim also is to automatically configure a fresh AWS instance to run these processes with the shell script (boostrap_instance.sh)
