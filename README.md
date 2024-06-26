# variant-annotation-OTG

## Description
Tools for annotating variants using OTG data 

## Usage
To run the program I need to use the HPC sbatch run like indicated in the script scheduler_annotation.sbatch:

sbatch scheduler_annotation.sbatch

This needs to be modified adding the preferred input and output files using the parameters -i and -o

To run the program from a srun I can use the script v2g_dask_query.py after loading the tiledb conda environment:

conda activate tiledb

python v2g_dask_query.py -i <input-file> -o <output-file>

## Output

The output from the program look like the one described below when running the sbatch commands described above:


 
chr_id	position	ref_allele	alt_allele	gene_id	feature	type_id	source_id	qtl_beta	qtl_se	overall_score	SNP_id
1	19544640	C	T	ENSG00000178828	unspecified	distance	canonical_tss			0.03319919517102615	1_19544640_C_T
1	156136394	T	C	ENSG00000132702	unspecified	distance	canonical_tss			0.0	1_156136394_T_C
1	172113953	A	G	ENSG00000180999	UBERON_0001255	pchic	jung2019			0.07303822937625754	1_172113953_A_G
1	172113953	A	G	ENSG00000180999	NAIVE_CD8	pchic	javierre2016			0.07303822937625754	1_172113953_A_G
1	172113953	A	G	ENSG00000180999	UBERON_0002421	pchic	jung2019			0.07303822937625754	1_172113953_A_G
1	172113953	A	G	ENSG00000180999	NAIVE_B	pchic	javierre2016			0.07303822937625754	1_172113953_A_G
1	172113953	A	G	ENSG00000180999	TOTAL_CD4_ACTIVATED	pchic	javierre2016			0.07303822937625754	1_172113953_A_G
1	172113953	A	G	ENSG00000180999	NAIVE_CD4	pchic	javierre2016			0.07303822937625754	1_172113953_A_G
1	172113953	A	G	ENSG00000180999	TOTAL_CD4_NONACTIVATED	pchic	javierre2016			0.07303822937625754	1_172113953_A_G





