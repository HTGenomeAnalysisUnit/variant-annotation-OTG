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


```
SNP_id	gene_id	chr_id	position	ref_allele	alt_allele	distance_score	fpred_max	fpred_label	dhs_scores	max_pchic_score	max_fantom5_score	eqtl_scores	eqtl_features	pqtl_scores	pqtl_features	sqtl_scores	sqtl_features	overall_scores
10_100901494_G_T	ENSG00000055950	10	100901494	G	T							[6.710107949709511, 15.105935502118502, 16.961510980610807, 5.794259867490539, 8.164764883945658, 14.087789638213293, 6.370809642409146, 8.943792865754721, 5.320681144979089, 9.812265004885148, 5.372326968233383, 8.762735325382447, 13.88319972163204, 14.184736465147271, 8.179416319366963, 11.122663214747925, 6.186947023422965, 10.37502317632599, 11.771591941108486, 14.478369036388168, 8.6893767750619, 11.592186055740262, 17.06112117973061, 18.587262331759675, 118.58407558702882, 5.40340180489523, 5.815413607346549, 8.876115706539991, 5.854822246876875, 6.480473886741257, 9.005837319949105, 11.592918566217657, 6.147916664153372, 6.878269491594207, 7.493423267571631, 5.258136458314456]	['Fairfax_2014-MONOCYTE_IFN24', 'Fairfax_2014-MONOCYTE_IFN24', 'Fairfax_2014-MONOCYTE_IFN24', 'GTEx-eQTL-HEART_ATRIAL_APPENDAGE', 'CEDAR-MONOCYTE_CD14', 'CEDAR-MONOCYTE_CD14', 'CEDAR-B-CELL_CD19', 'CEDAR-B-CELL_CD19', 'Kasela_2017-T-CELL_CD4', 'ROSMAP-BRAIN_NAIVE', 'Lepik_2017-BLOOD', 'Fairfax_2014-MONOCYTE_LPS24', 'Fairfax_2014-MONOCYTE_LPS24', 'Fairfax_2014-MONOCYTE_LPS24', 'Fairfax_2014-MONOCYTE_LPS2', 'Fairfax_2014-MONOCYTE_LPS2', 'CEDAR-T-CELL_CD4', 'CEDAR-T-CELL_CD4', 'CEDAR-T-CELL_CD4', 'CEDAR-T-CELL_CD4', 'Fairfax_2014-MONOCYTE_NAIVE', 'Fairfax_2014-MONOCYTE_NAIVE', 'Fairfax_2014-MONOCYTE_NAIVE', 'Fairfax_2014-MONOCYTE_NAIVE', 'eQTLGen-UBERON_0000178', 'GTEx-eQTL-THYROID', 'CEDAR-RECTUM', 'TwinsUK-SKIN', 'Fairfax_2012-B-CELL_CD19', 'Fairfax_2012-B-CELL_CD19', 'Fairfax_2012-B-CELL_CD19', 'Fairfax_2012-B-CELL_CD19', 'CEDAR-T-CELL_CD8', 'CEDAR-T-CELL_CD8', 'CEDAR-T-CELL_CD8', 'CEDAR-ILEUM']			[16.521248575505066, 9.582583613066339, 9.923869014352546, 9.553597539768088, 16.08540663123789, 10.462109959674253, 12.114646920599958, 12.619239005366403, 5.075471187431519, 5.770451979278031, 16.65841640269263, 19.483531692914486, 6.891074787116783, 15.433408343076177, 6.671974881626759, 16.828624791303444, 22.640507528682587, 7.580439237911799, 22.004223221249816, 13.385259462600235, 34.200921849443056, 17.3370968808413, 11.895341885471055, 8.049706290099317, 10.40886469615502, 19.547824909030304, 4.981363630222444, 25.094451437569244, 6.192680902861099, 6.965488617394595, 25.765583131393473, 6.289723302234493, 18.469099819080128, 9.006001244848298, 8.315076755317442, 5.009605109266121, 26.494622039347426, 5.66243974480897, 14.61355665353395, 4.981766941914716, 9.62411627961921, 26.750694062319997, 5.22741857574579, 9.877472493295018, 8.827380814874285, 9.909438393542494, 5.763049011438777, 11.332513480936186, 8.67127113573313, 11.724311245850876, 6.342018449571714, 7.443521064582637]	['GTEx-sQTL-Cells_Cultured_fibroblasts', 'GTEx-sQTL-Artery_Coronary', 'GTEx-sQTL-Colon_Sigmoid', 'GTEx-sQTL-Adrenal_Gland', 'GTEx-sQTL-Heart_Atrial_Appendage', 'GTEx-sQTL-Stomach', 'GTEx-sQTL-Pancreas', 'GTEx-sQTL-Breast_Mammary_Tissue', 'GTEx-sQTL-Brain_Anterior_cingulate_cortex_BA24', 'GTEx-sQTL-Nerve_Tibial', 'GTEx-sQTL-Nerve_Tibial', 'GTEx-sQTL-Testis', 'GTEx-sQTL-Adipose_Visceral_Omentum', 'GTEx-sQTL-Adipose_Visceral_Omentum', 'GTEx-sQTL-Esophagus_Muscularis', 'GTEx-sQTL-Esophagus_Muscularis', 'GTEx-sQTL-Adipose_Subcutaneous', 'GTEx-sQTL-Artery_Tibial', 'GTEx-sQTL-Artery_Tibial', 'GTEx-sQTL-Muscle_Skeletal', 'GTEx-sQTL-Muscle_Skeletal', 'GTEx-sQTL-Esophagus_Mucosa', 'GTEx-sQTL-Artery_Aorta', 'GTEx-sQTL-Brain_Frontal_Cortex_BA9', 'GTEx-sQTL-Brain_Frontal_Cortex_BA9', 'GTEx-sQTL-Skin_Not_Sun_Exposed_Suprapubic', 'GTEx-sQTL-Thyroid', 'GTEx-sQTL-Thyroid', 'GTEx-sQTL-Cells_EBV-transformed_lymphocytes', 'GTEx-sQTL-Skin_Sun_Exposed_Lower_leg', 'GTEx-sQTL-Skin_Sun_Exposed_Lower_leg', 'GTEx-sQTL-Heart_Left_Ventricle', 'GTEx-sQTL-Heart_Left_Ventricle', 'GTEx-sQTL-Liver', 'GTEx-sQTL-Spleen', 'GTEx-sQTL-Lung', 'GTEx-sQTL-Lung', 'GTEx-sQTL-Colon_Transverse', 'GTEx-sQTL-Colon_Transverse', 'GTEx-sQTL-Esophagus_Gastroesophageal_Junction', 'GTEx-sQTL-Esophagus_Gastroesophageal_Junction', 'GTEx-sQTL-Whole_Blood', 'GTEx-sQTL-Brain_Hypothalamus', 'GTEx-sQTL-Pituitary', 'GTEx-sQTL-Brain_Cerebellum', 'GTEx-sQTL-Brain_Caudate_basal_ganglia', 'GTEx-sQTL-Brain_Putamen_basal_ganglia', 'GTEx-sQTL-Prostate', 'GTEx-sQTL-Brain_Cortex', 'GTEx-sQTL-Brain_Nucleus_accumbens_basal_ganglia', 'GTEx-sQTL-Small_Intestine_Terminal_Ileum', 'GTEx-sQTL-Brain_Hippocampus']	0.3537223340040241
10_100901494_G_T	ENSG00000075290	10	100901494	G	T	2.2805797233656794e-06												0.0066398390342052305
10_100901494_G_T	ENSG00000075826	10	100901494	G	T	2.6203390718759008e-06												0.013279678068410461
10_100901494_G_T	ENSG00000075891	10	100901494	G	T	6.020542089609748e-06				1.0								0.04647887323943661
10_100901494_G_T	ENSG00000095539	10	100901494	G	T	1.4703720041170417e-05						[6.51817341282354]	['CommonMind-DLPFC_NAIVE']			0.09959758551307847
```



