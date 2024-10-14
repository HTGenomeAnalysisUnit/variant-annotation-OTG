# variant-annotation-OTG

## Description
Tools for annotating variants using OTG data 

## Usage
To run the program you need to use a sbatch script in the HPC. An example of sbatch script is provided in the script folder like below

```cat script/scheduler_annotation.sbatch```
```
#!/bin/bash
#SBATCH --job-name=v2dg_annotate
#SBATCH --output=logfile_sbatch.txt
#SBATCH --partition=cpuq
#SBATCH --cpus-per-task=5
#SBATCH --mem=10G
#SBATCH --time=00:40:00

source /ssu/gassu/miniconda3/etc/profile.d/conda.sh
conda activate sparkhpc

python main.py --variants_query variants_query.txt --out variants_anno_out

```

This needs to be modified adding the preferred input and output files and the type of annotation that you want to use. The parameters used can be either using the options:

## Input

Input can be given using the --variants_query option:
<details>
<summary>Example of table with variants:</summary>
<pre>
head tests/variants_query.txt
1_154453788_C_T
1_1022868_A_G
1_2211079_A_C
1_2293397_G_A
1_6568959_A_AG
1_8094061_TG_T
1_8447713_G_A
1_9283562_C_T
1_9478595_G_C
</pre>
</details>

## Type of annotation

Two  type of annotation are given:
    -   The variant to gene which will return all the scores that associate a variant with a gene for all the QTL types.
    -   The variant to disease which return all the annotation that associate a variant with a trait from a GWAS.

## Optional parameters

In the variant_disease_gene option the following optional parameters are available:

    --tag which will match the query variants with the tag variants from OTG instead than using the lead ones (Default: false).

    --gnomad_af which will return the allele frequency for the alternate allele from a specific population (Default: gnomad_nfe). The list of population availablefor this parameter are reported below

### Populations for the --gnomad_af parameter
    -   gnomad_nfe non-Finnish Europeans
    -   gnomad_afr Africans
    -   gnomad_amr North Americans
    -   gnomad_asj Ashkenazi jew
    -   gnomad_eas East Asians
    -   gnomad_fin Finnish
    -   gnomad_nfe_est non-Finnish East Europeans
    -   gnomad_nfe_nwe non-Finnish North-Western Europeans
    -   gnomad_nfe_seu non-Finnish South-Eastern Europeans
    -   gnomad_nfe_onf other non-Finnish Europeans
    -   gnomad_oth other

## Output

### variant_gene output
The output from the program look like the one described below when running the sbatch commands described above:

```
SNP_id  gene_id chr_id  position        ref_allele      alt_allele      overall_scores  distance_score  fpred_max       fpred_label     dhs_scores  max_pchic_score  max_fantom5_score       max_eqtl_score  max_eqtl_feature        max_pqtl_score  max_pqtl_feature        max_sqtl_score  max_sqtl_feature     eqtl_scores     eqtl_features   pqtl_scores     pqtl_features   sqtl_scores     sqtl_features
10_100901494_G_T        ENSG00000055950 10      100901494       G       T       0.3537223340040241      Na      Na      Na      Na      Na      Na  118.58407558702882       eQTLGen-UBERON_0000178  Na      Na      34.200921849443056      GTEx-sQTL-Muscle_Skeletal       [118.58407558702882, 18.587262331759675, 17.06112117973061, 16.961510980610807, 15.105935502118502, 14.478369036388168, 14.184736465147271, 14.087789638213293, 13.88319972163204, 11.771591941108486, 11.592918566217657, 11.592186055740262, 11.122663214747925, 10.37502317632599, 9.812265004885148, 9.005837319949105, 8.943792865754721, 8.876115706539991, 8.762735325382447, 8.6893767750619, 8.179416319366963, 8.164764883945658, 7.493423267571631, 6.878269491594207, 6.710107949709511, 6.480473886741257, 6.370809642409146, 6.186947023422965, 6.147916664153372, 5.854822246876875, 5.815413607346549, 5.794259867490539, 5.40340180489523, 5.372326968233383, 5.320681144979089, 5.258136458314456]     ['eQTLGen-UBERON_0000178', 'Fairfax_2014-MONOCYTE_NAIVE', 'Fairfax_2014-MONOCYTE_NAIVE', 'Fairfax_2014-MONOCYTE_IFN24', 'Fairfax_2014-MONOCYTE_IFN24', 'CEDAR-T-CELL_CD4', 'Fairfax_2014-MONOCYTE_LPS24', 'CEDAR-MONOCYTE_CD14', 'Fairfax_2014-MONOCYTE_LPS24', 'CEDAR-T-CELL_CD4', 'Fairfax_2012-B-CELL_CD19', 'Fairfax_2014-MONOCYTE_NAIVE', 'Fairfax_2014-MONOCYTE_LPS2', 'CEDAR-T-CELL_CD4', 'ROSMAP-BRAIN_NAIVE', 'Fairfax_2012-B-CELL_CD19', 'CEDAR-B-CELL_CD19', 'TwinsUK-SKIN', 'Fairfax_2014-MONOCYTE_LPS24', 'Fairfax_2014-MONOCYTE_NAIVE', 'Fairfax_2014-MONOCYTE_LPS2', 'CEDAR-MONOCYTE_CD14', 'CEDAR-T-CELL_CD8', 'CEDAR-T-CELL_CD8', 'Fairfax_2014-MONOCYTE_IFN24', 'Fairfax_2012-B-CELL_CD19', 'CEDAR-B-CELL_CD19', 'CEDAR-T-CELL_CD4', 'CEDAR-T-CELL_CD8', 'Fairfax_2012-B-CELL_CD19', 'CEDAR-RECTUM', 'GTEx-eQTL-HEART_ATRIAL_APPENDAGE', 'GTEx-eQTL-THYROID', 'Lepik_2017-BLOOD', 'Kasela_2017-T-CELL_CD4', 'CEDAR-ILEUM']  Na      Na      [34.200921849443056, 26.750694062319997, 26.494622039347426, 25.765583131393473, 25.094451437569244, 22.640507528682587, 22.004223221249816, 19.547824909030304, 19.483531692914486, 18.469099819080128, 17.3370968808413, 16.828624791303444, 16.65841640269263, 16.521248575505066, 16.08540663123789, 15.433408343076177, 14.61355665353395, 13.385259462600235, 12.619239005366403, 12.114646920599958, 11.895341885471055, 11.724311245850876, 11.332513480936186, 10.462109959674253, 10.40886469615502, 9.923869014352546, 9.909438393542494, 9.877472493295018, 9.62411627961921, 9.582583613066339, 9.553597539768088, 9.006001244848298, 8.827380814874285, 8.67127113573313, 8.315076755317442, 8.049706290099317, 7.580439237911799, 7.443521064582637, 6.965488617394595, 6.891074787116783, 6.671974881626759, 6.342018449571714, 6.289723302234493, 6.192680902861099, 5.770451979278031, 5.763049011438777, 5.66243974480897, 5.22741857574579, 5.075471187431519, 5.009605109266121, 4.981766941914716, 4.981363630222444]        ['GTEx-sQTL-Muscle_Skeletal', 'GTEx-sQTL-Whole_Blood', 'GTEx-sQTL-Lung', 'GTEx-sQTL-Skin_Sun_Exposed_Lower_leg', 'GTEx-sQTL-Thyroid', 'GTEx-sQTL-Adipose_Subcutaneous', 'GTEx-sQTL-Artery_Tibial', 'GTEx-sQTL-Skin_Not_Sun_Exposed_Suprapubic', 'GTEx-sQTL-Testis', 'GTEx-sQTL-Heart_Left_Ventricle', 'GTEx-sQTL-Esophagus_Mucosa', 'GTEx-sQTL-Esophagus_Muscularis', 'GTEx-sQTL-Nerve_Tibial', 'GTEx-sQTL-Cells_Cultured_fibroblasts', 'GTEx-sQTL-Heart_Atrial_Appendage', 'GTEx-sQTL-Adipose_Visceral_Omentum', 'GTEx-sQTL-Colon_Transverse', 'GTEx-sQTL-Muscle_Skeletal', 'GTEx-sQTL-Breast_Mammary_Tissue', 'GTEx-sQTL-Pancreas', 'GTEx-sQTL-Artery_Aorta', 'GTEx-sQTL-Brain_Nucleus_accumbens_basal_ganglia', 'GTEx-sQTL-Prostate', 'GTEx-sQTL-Stomach', 'GTEx-sQTL-Brain_Frontal_Cortex_BA9', 'GTEx-sQTL-Colon_Sigmoid', 'GTEx-sQTL-Brain_Caudate_basal_ganglia', 'GTEx-sQTL-Pituitary', 'GTEx-sQTL-Esophagus_Gastroesophageal_Junction', 'GTEx-sQTL-Artery_Coronary', 'GTEx-sQTL-Adrenal_Gland', 'GTEx-sQTL-Liver', 'GTEx-sQTL-Brain_Cerebellum', 'GTEx-sQTL-Brain_Cortex', 'GTEx-sQTL-Spleen', 'GTEx-sQTL-Brain_Frontal_Cortex_BA9', 'GTEx-sQTL-Artery_Tibial', 'GTEx-sQTL-Brain_Hippocampus', 'GTEx-sQTL-Skin_Sun_Exposed_Lower_leg', 'GTEx-sQTL-Adipose_Visceral_Omentum', 'GTEx-sQTL-Esophagus_Muscularis', 'GTEx-sQTL-Small_Intestine_Terminal_Ileum', 'GTEx-sQTL-Heart_Left_Ventricle', 'GTEx-sQTL-Cells_EBV-transformed_lymphocytes', 'GTEx-sQTL-Nerve_Tibial', 'GTEx-sQTL-Brain_Putamen_basal_ganglia', 'GTEx-sQTL-Colon_Transverse', 'GTEx-sQTL-Brain_Hypothalamus', 'GTEx-sQTL-Brain_Anterior_cingulate_cortex_BA24', 'GTEx-sQTL-Lung', 'GTEx-sQTL-Esophagus_Gastroesophageal_Junction', 'GTEx-sQTL-Thyroid']
10_100901494_G_T        ENSG00000075290 10      100901494       G       T       0.0066398390342052305   2.2805797233656794e-06  Na      Na      Na  Na       Na      Na      Na      Na      Na      Na      Na      Na      Na      Na      Na      Na      Na
10_100901494_G_T        ENSG00000075826 10      100901494       G       T       0.013279678068410461    2.6203390718759008e-06  Na      Na      Na  Na       Na      Na      Na      Na      Na      Na      Na      Na      Na      Na      Na      Na      Na
10_100901494_G_T        ENSG00000075891 10      100901494       G       T       0.04647887323943661     6.020542089609748e-06   Na      Na      Na  1.0      Na      Na      Na      Na      Na      Na      Na      Na      Na      Na      Na      Na      Na
10_100901494_G_T        ENSG00000095539 10      100901494       G       T       0.09959758551307847     1.4703720041170417e-05  Na      Na      Na  Na       Na      6.51817341282354        CommonMind-DLPFC_NAIVE  Na      Na      Na      Na      [6.51817341282354]      ['CommonMind-DLPFC_NAIVE']  Na       Na      Na      Na
10_100901494_G_T        ENSG00000107807 10      100901494       G       T       0.03319919517102615     4.351496479639348e-06   Na      Na      Na  Na       Na      Na      Na      Na      Na      Na      Na      Na      Na      Na      Na      Na      Na
10_100901494_G_T        ENSG00000107815 10      100901494       G       T       0.11951710261569416     Na      Na      Na      Na      Na      Na  16.52747757708312        eQTLGen-UBERON_0000178  Na      Na      Na      Na      [16.52747757708312]     ['eQTLGen-UBERON_0000178']      Na      Na  Na       Na
10_100901494_G_T        ENSG00000107816 10      100901494       G       T       0.11307847082494969     Na      Na      Na      Na      1.0     Na  7.045557278705984        BLUEPRINT-MONOCYTE      Na      Na      5.549584908758971       GTEx-sQTL-Esophagus_Muscularis  [7.045557278705984, 5.985240119222274]       ['BLUEPRINT-MONOCYTE', 'Schmiedel_2018-MONOCYTE_NAIVE'] Na      Na      [5.549584908758971]     ['GTEx-sQTL-Esophagus_Muscularis']
10_100901494_G_T        ENSG00000107819 10      100901494       G       T       0.07303822937625754     7.707723138584862e-06   Na      Na      Na  Na       Na      6.790565417809094       eQTLGen-UBERON_0000178  Na      Na      Na      Na      [6.790565417809094]     ['eQTLGen-UBERON_0000178']  Na       Na      Na      Na
```

### variant_disease output
```
study_id        SNP_id  lead_chrom      lead_pos        lead_ref        lead_alt        beta    beta_ci_lower   beta_ci_upper   pval    pmid    trait_reported  ancestry_initial     n_initial       gene_id V2G_SCORE_MAX   gnomad_nfe
NEALE2_50_raw   1_6568959_A_AG  1       6568959 A       AG      -0.130629       -0.174965376    -0.086292624    7.710480000000002e-09           Standing height ['European=360388']  360388  ENSG00000171680 0.23239436619718312
NEALE2_20015_raw        1_8447713_G_A   1       8447713 G       A       0.0622522999999999      0.041171128     0.0833334719999999      7.1347300000000015e-09          Sitting height       ['European=360066']     360066  ENSG00000142599 0.2937625754527163
NEALE2_1697     1_8447713_G_A   1       8447713 G       A       0.0132827999999999      0.0093519416    0.0172136583999999      3.5228999999999995e-11          Comparative height size at age 10    ['European=355331']     355331  ENSG00000142599 0.2937625754527163
NEALE2_50_raw   1_8447713_G_A   1       8447713 G       A       0.151467        0.1149931639999999      0.187940836     3.9853399999999996e-16          Standing height ['European=360388']  360388  ENSG00000142599 0.2937625754527163
NEALE2_50_raw   1_10148710_T_C  1       10148710        T       C       0.212667        0.163939832     0.261394168     1.1902e-17              Standing height ['European=360388']  360388  ENSG00000130939 0.29336016096579476
NEALE2_20015_raw        1_10148710_T_C  1       10148710        T       C       0.0888988       0.060734384     0.117063216     6.15406e-10             Sitting height  ['European=360066']  360066  ENSG00000130939 0.29336016096579476
NEALE2_50_raw   1_1022868_A_G   1       1022868 A       G       0.0908756999999999      0.0605976199999999      0.1211537799999999      4.04012e-09             Standing height      ['European=360388']     360388  ENSG00000187608 0.37344064386317904
NEALE2_50_raw   1_8094061_TG_T  1       8094061 TG      T       -0.1170369999999999     -0.1545431679999999     -0.079530832    9.596650000000001e-10           Standing height      ['European=360388']     360388  ENSG00000116288 0.36720321931589534
NEALE2_50_raw   1_2293397_G_A   1       2293397 G       A       0.106066        0.075624848     0.136507152     8.553e-12               Standing height ['European=360388'] 360388   ENSG00000157933 0.07987927565392354
```

Please note for the v2d_table above that for each SNP_id only one gene is reported which is the one with the highest V2G score taken from the v2g_table.

## Example running the standalone program

To run the program from a cnode you can use also the script main.py after loading the sparkhpc conda environment as shown in the 2 examples below:

```
conda activate sparkhpc

python main.py --variants_query tests/variants_query.txt variant_disease_gene --out variant_gene_out
``