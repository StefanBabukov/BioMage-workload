library(Matrix)
args = commandArgs(trailingOnly=TRUE)
# First argument is the sample name, second is the output folder location (.rds files also must be there)
sample <- args[1]
output_folder <- args[2]
`+` <- function(e1, e2) {
  if (is.character(e1) | is.character(e2)) {
    paste0(e1, e2)
  } else {
    base::`+`(e1, e2)
  }
}

dat <- readRDS(output_folder + "/" + sample + ".rds")

write(x = rownames(dat$cm), file = output_folder + "/" + sample + ".all.genes.tsv")
write(x = colnames(dat$cm), file = output_folder + "/" + sample + ".all.cells.tsv")

writeMM(dat$cm, file = output_folder + "/" + sample + ".all.mm")

#reading velocyto matrices

dat2 <- readRDS(output_folder + "/" + sample + ".matrices.rds")

write(x = rownames(dat2$intron), file = output_folder + "/" + sample + ".intron.genes.tsv")
write(x = colnames(dat2$intron), file = output_folder + "/" + sample + ".intron.cells.tsv")
write(x = rownames(dat2$exon), file = output_folder + "/" + sample + ".exon.genes.tsv")
write(x = colnames(dat2$exon), file = output_folder + "/" + sample + ".exon.cells.tsv")
write(x = rownames(dat2$spanning), file = output_folder + "/" + sample + ".spanning.genes.tsv")
write(x = colnames(dat2$spanning), file = output_folder + "/" + sample + ".spanning.cells.tsv")

writeMM(dat2$intron, file = output_folder + "/" + sample + ".intron.mm")
writeMM(dat2$exon, file = output_folder + "/" + sample + ".exon.mm")
writeMM(dat2$spanning, file = output_folder + "/" + sample + ".spanning.mm")
