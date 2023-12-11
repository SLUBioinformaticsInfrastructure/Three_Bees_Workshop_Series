#addition reading
#pca from vcf: https://speciationgenomics.github.io/pca/
#plink manual: https://www.cog-genomics.org/plink/1.9/strat
#pca from dartseq: http://georges.biomatix.org/dartR
#summarized experiments: https://www.bioconductor.org/help/course-materials/2019/BSS2019/04_Practical_CoreApproachesInBioconductor.html
#rnaseq workflow: https://master.bioconductor.org/packages/release/workflows/vignettes/rnaseqGene/inst/doc/rnaseqGene.html
#code for the tutorial: https://bioconductor.org/packages/devel/bioc/vignettes/PCAtools/inst/doc/PCAtools.html

library(PCAtools)
library(airway)
library(magrittr)
library(tidyverse)
library(DESeq2)
library(org.Hs.eg.db)

data('airway')
dim(airway)
dimnames(airway)
colData(airway)

ens <- rownames(airway)

symbols <- AnnotationDbi::mapIds(org.Hs.eg.db, keys = ens,
                  column = c('SYMBOL'), keytype = 'ENSEMBL')
symbols <- symbols[!is.na(symbols)]
symbols <- symbols[match(rownames(airway), names(symbols))]
rownames(airway) <- symbols
keep <- !is.na(rownames(airway))
airway <- airway[keep,]

head(symbols)

dds <- DESeqDataSet(airway, design = ~ cell + dex)
dds <- DESeq(dds)
vst <- assay(vst(dds))

p <- pca(vst, metadata = colData(airway), removeVar = 0.1)
screeplot(p, axisLabSize = 18, titleLabSize = 22)
biplot(p)

biplot(p, showLoadings = TRUE,
       labSize = 5, pointSize = 5, sizeLoadingsNames = 5)

plotloadings(p, labSize = 3)

