#!/bin/bash

mkdir /home/ubuntu/Downloads

sudo apt-get update
sudo apt-get install python3.6 python3-pip

cd /home/ubuntu
pip3 install -r BioMage-workload/requirements.txt

cd /home/ubuntu/Downloads
#downloading cellranger
wget -O cellranger-3.1.0.tar.gz "http://cf.10xgenomics.com/releases/cell-exp/cellranger-3.1.0.tar.gz?Expires=1570580309&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cDovL2NmLjEweGdlbm9taWNzLmNvbS9yZWxlYXNlcy9jZWxsLWV4cC9jZWxscmFuZ2VyLTMuMS4wLnRhci5neiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTU3MDU4MDMwOX19fV19&Signature=areB15CbMneWXcI0W29f5sil3xlIetkaxlFFtlholdiG0FQFfWyxSYJ7OIKyWWxy8tpXmcBQyG84K5UswemBDOko0KndGt~x2boUgCuFE3xg-MVN1Dykir3XTaa7hSWYc9gxo8dmYHMB2FhIuUDO43UEkp35ve5UpT5~sJolKblXMy67N5uIWIcVccCxslVCx0ORSFegG~rmahXbZLPWlIDtdWaC77VpqZo7cKgVAUhQY0egqgnTk9rcgkN1X~wiI~G85gL68UEZcPOy4Wt087izCDWKMXxfYqatsVFbroQKOs6h1lt4bG20z1Rz2sGrLPX4vb3twaqmoXmZ0ipWZw__&Key-Pair-Id=APKAI7S6A5RYOXBWRPDA"

tar -xzvf refdata-cellranger-GRCh38-3.0.0.tar.gz

export PATH=/home/ubuntu/Downloads/cellranger-3.1.0:$PATH
echo 'export PATH=/home/ubuntu/Downloads/cellranger-3.1.0:$PATH' >> ~/.bashrc

#downloading human reference genome
wget http://cf.10xgenomics.com/supp/cell-exp/refdata-cellranger-GRCh38-3.0.0.tar.gz

# dropest installation and configuration
#
#
#
