#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)

if(length(args)==0){
	stop("An .rds file must be specified as an argument", call.=FALSE)
}

temp <- readRDS(args[1])
write.csv(temp$aligned_reads_per_cell, args[2])
