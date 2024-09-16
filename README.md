# variant-annotation-OTG

## Description
Tools for annotating variants using OTG data 

## Usage
To run the program you need to use a sbatch script in the HPC. An example of sbatch script is provided in the script folder like below

```cat script/scheduler_annotation.sbatch```
```
#!/bin/bash
#SBATCH --job-name=v2g_annotate
#SBATCH --output=logfile_sbatch.txt
#SBATCH --partition=cpuq
#SBATCH --cpus-per-task=5
#SBATCH --mem=10G
#SBATCH --time=00:40:00

source /ssu/gassu/miniconda3/etc/profile.d/conda.sh
conda activate sparkhpc

python main.py --variants_query variants_query.txt variant_gene --out variants_anno_v2g_out.csv

python main.py --variants_query variants_query.txt variant_disease --out variants_anno_v2d_out.csv
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

Two  type of annotation can be used:
    -   The variant to gene which will return all the scores that associate a variant with a gene for all the QTL types. This option is selected using --variant_gene
    -   The variant to disease which return all the annotation that associate a variant with a trait from a GWAS.

## Optional parameters

In case the variant_disease option is selected the following optional parameters are available:

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

### variant_gene option
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

### variant_disease option
```
study_id        lead_chrom      lead_pos        lead_ref        lead_alt        SNP_id  beta    beta_ci_lower   beta_ci_upper   pval    pmid    trait_reported  ancestry_initial        n_initial       chr_id  position  ref_allele      alt_allele      chr_id_b37      position_b37    rs_id   most_severe_consequence gene_id_any_distance    gene_id_any     gene_id_prot_coding_distance    gene_id_prot_coding     SNP_id  gnomad_nfe
0       GCST008057      6       26267527        A       G       6_26267527_A_G  -0.0027123      -0.0033992016583159     -0.002025398341684      1e-14   PMID:30998689   Varicose veins  ['European=408455']     408455  626267527 A       G       6       26267755        rs7773004       downstream_gene_variant 3886    ENSG00000273983 3886    ENSG00000273983 6_26267527_A_G  0.4972663368914345
1       NEALE2_3063_raw 19      55482069        G       T       19_55482069_G_T -0.0305323999999999     -0.0395691955999999     -0.0214956044   3.5439999999999996e-11          Forced expiratory volume in 1-second (fev1)       ['European=329404']     329404  19      55482069        G       T       19      55993436        rs147110934     missense_variant        3119    ENSG00000090971 3119    ENSG00000090971 19_55482069_G_T 0.020293495505023795
2       NEALE2_23126_raw        19      55482069        G       T       19_55482069_G_T -0.0195978      -0.0263018624   -0.0128937375999999     1.00728e-08             Arm predicted mass (left)       ['European=354653']       354653  19      55482069        G       T       19      55993436        rs147110934     missense_variant        3119    ENSG00000090971 3119    ENSG00000090971 19_55482069_G_T 0.020293495505023795
3       NEALE2_23105_raw        19      55482069        G       T       19_55482069_G_T -40.8364        -53.5117396     -28.1610604     2.71238e-10             Basal metabolic rate    ['European=354825']     354825  1955482069        G       T       19      55993436        rs147110934     missense_variant        3119    ENSG00000090971 3119    ENSG00000090971 19_55482069_G_T 0.020293495505023795
4       NEALE2_23129_raw        19      55482069        G       T       19_55482069_G_T -0.189325       -0.238145268    -0.140504732    2.8999999999999996e-14          Trunk fat-free mass     ['European=354530']     354530    19      55482069        G       T       19      55993436        rs147110934     missense_variant        3119    ENSG00000090971 3119    ENSG00000090971 19_55482069_G_T 0.020293495505023795
5       NEALE2_50_raw   10      79376373        C       A       10_79376373_C_A -0.207289       -0.236445568    -0.178132432    4.0060700000000003e-44          Standing height ['European=360388']     360388  10      79376373  C       A       10      81136129        rs4980067       intergenic_variant      28904   ENSG00000108179 28904   ENSG00000108179 10_79376373_C_A 0.5354218120369166
6       NEALE2_23129_raw        10      79376373        C       A       10_79376373_C_A -0.0633598      -0.078337042    -0.0483825579999999     1.12115e-16             Trunk fat-free mass     ['European=354530']     354530    10      79376373        C       A       10      81136129        rs4980067       intergenic_variant      28904   ENSG00000108179 28904   ENSG00000108179 10_79376373_C_A 0.5354218120369166
7       NEALE2_23105_raw        10      79376373        C       A       10_79376373_C_A -14.7126        -18.6007696     -10.8244304     1.21e-13                Basal metabolic rate    ['European=354825']     354825  1079376373        C       A       10      81136129        rs4980067       intergenic_variant      28904   ENSG00000108179 28904   ENSG00000108179 10_79376373_C_A 0.5354218120369166
8       NEALE2_50_raw   2       232196106       T       C       2_232196106_T_C -0.615194       -0.718153192    -0.512234808    1.13096e-31             Standing height ['European=360388']     360388  2       232196106TC       2       233060816       rs77060225      intron_variant  182618  ENSG00000163283 182618  ENSG00000163283 2_232196106_T_C 0.022052146841354262
```

## Example running the standalone program

To run the program from a cnode you can use also the script main.py after loading the sparkhpc conda environment as shown in the 2 examples below:

```
conda activate sparkhpc

python main.py --variants_query tests/variants_query.txt variant_gene --out variant_gene_out.tsv
```

```
conda activate sparkhpc

python main.py --variants_query tests/variants_query.txt variant_disease --gnomad_af gnomad_nfe --out variant_disease
```