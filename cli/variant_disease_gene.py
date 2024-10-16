import pyspark.sql.functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, DoubleType
from pyspark.sql.functions import col, broadcast, when

def variant_disease_gene(spark_object, snp_values, out: str, gnomad_af: str, tag: bool):
    spark = spark_object

    #Create V2G table
    print("Creating V2G table")
    ##Create schema
    schema = StructType([
        StructField('chr_id', StringType(), True),
        StructField('position', DoubleType(), True),
        StructField('ref_allele', StringType(), True),
        StructField('alt_allele', StringType(), True),
        StructField('gene_id', StringType(), True),
        StructField('feature', StringType(), True),
        StructField('type_id', StringType(), True),
        StructField('source_id', StringType(), True),
        StructField('fpred_labels', StringType(), True),
        StructField('fpred_scores', FloatType(), True),
        StructField('fpred_max_label', StringType(), True),
        StructField('fpred_max_score', FloatType(), True),
        StructField('qtl_beta', FloatType(), True),
        StructField('qtl_se', FloatType(), True),
        StructField('qtl_pval', FloatType(), True),
        StructField('qtl_score', FloatType(), True),
        StructField('interval_score', FloatType(), True),
        StructField('qtl_score_q', FloatType(), True),
        StructField('interval_score_q', FloatType(), True),
        StructField('d', FloatType(), True),
        StructField('distance_score', FloatType(), True),
        StructField('distance_score_q', FloatType(), True),
        StructField('overall_score', FloatType(), True),
        StructField('source_list', StringType(), True),
        StructField('source_score_list', StringType(), True)
    ])

    #Read v2g OTG table
    ddf = spark.read.parquet("/ssu/gassu/reference_data/OpenTargets/22.10/v2g_scored")

    #subset and process data
    columns_select = ['chr_id', 'position', 'ref_allele', 'alt_allele', 'gene_id', 'feature', 'type_id', 
                      'source_id', 'fpred_max_label', 'fpred_max_score', 'qtl_score', 'interval_score', 
                      'd', 'distance_score', 'overall_score']
    ddf_select = ddf.select(columns_select)
    ddf_select = ddf_select.withColumn("SNP_id", F.concat_ws("_", F.col("chr_id"), F.col("position"), F.col("ref_allele"), F.col("alt_allele")))

    #join with broadcasted SNP id
    snp_values = broadcast(snp_values)
    filtered_ddf = ddf_select.join(snp_values, "SNP_id")
    aggregated_df = filtered_ddf.groupBy('SNP_id', 'gene_id').agg(
        F.first('chr_id').alias('CHROMOSOME'),
        F.first('position').alias('POSITION'),
        F.first('ref_allele').alias('REF'),
        F.first('alt_allele').alias('ALT'),
        F.first('overall_score').alias('V2G_SCORE'),
        F.first('distance_score').alias('DISTANCE_SCORE'),
        F.max('fpred_max_score').alias('FPRED_SCORE'),
        F.first('fpred_max_label').alias('FPRED_LABEL'),
        F.max(when(col('type_id') == 'pchic', F.col('interval_score'))).alias('max_pchic_score'),
        F.max(when(col('type_id') == 'fantom5', F.col('interval_score'))).alias('max_fantom5_score'),
        F.max(when(col('type_id') == 'dhscor', F.col('interval_score'))).alias('max_dhs_score'),
        F.max(when(col('type_id') == 'eqtl', F.col('qtl_score'))).alias('max_eqtl_score'),
        F.max(when(col('type_id') == 'pqtl', F.col('qtl_score'))).alias('max_pqtl_score'),
        F.max(when(col('type_id') == 'sqtl', F.col('qtl_score'))).alias('max_sqtl_score'),
        F.collect_list(when(col('type_id') == 'eqtl', F.col('qtl_score'))).alias('eqtl_scores'),
        F.collect_list(when(col('type_id') == 'pqtl', F.col('qtl_score'))).alias('pqtl_scores'),
        F.collect_list(when(col('type_id') == 'sqtl', F.col('qtl_score'))).alias('sqtl_scores')
    )
    aggregated_df = aggregated_df.withColumn('eqtl_scores_list', F.concat_ws(',', 'eqtl_scores')).drop('eqtl_scores')
    aggregated_df = aggregated_df.withColumn('pqtl_scores_list', F.concat_ws(',', 'pqtl_scores')).drop('pqtl_scores')
    aggregated_df = aggregated_df.withColumn('sqtl_scores_list', F.concat_ws(',', 'sqtl_scores')).drop('sqtl_scores')
    aggregated_df_pd = aggregated_df.toPandas()
    aggregated_df_pd.to_csv(out + "_v2g.tsv", header=True)

    #Create v2d table
    print("Creating V2D table")

    snp_query = snp_values.toPandas()
    #Read OTG V2D dataset
    v2d_variants = spark.read.parquet("/ssu/gassu/reference_data/OpenTargets/22.10/v2d")

    #Subset only for certain columns
    if(tag):
        v2d_variants_select = (v2d_variants.
                    withColumn("SNP_id", F.concat_ws("_", "tag_chrom", "tag_pos", "tag_ref", "tag_alt")).
                    select("study_id","SNP_id","lead_chrom","lead_pos","lead_ref","lead_alt","tag_chrom","tag_pos","tag_ref","tag_alt","beta","beta_ci_lower","beta_ci_upper","pval","pmid","trait_reported","ancestry_initial","n_initial")
                    .dropDuplicates()
                    )
    else:
        v2d_variants_select = (v2d_variants.
                    withColumn("SNP_id", F.concat_ws("_", "lead_chrom", "lead_pos", "lead_ref", "lead_alt")).
                    select("study_id","SNP_id","lead_chrom","lead_pos","lead_ref","lead_alt","beta","beta_ci_lower","beta_ci_upper","pval","pmid","trait_reported","ancestry_initial","n_initial")
                    .dropDuplicates()
                    )

    filtered_ddf_lead = v2d_variants_select.filter(F.col('SNP_id').isin(snp_query.SNP_id.to_list()))

    #Import variants from OTG variant index for allele frequencies
    variant_index = spark.read.parquet("/ssu/gassu/reference_data/OpenTargets/22.10/variant_index")
    variant_index = variant_index.withColumn("SNP_id_index", F.concat_ws("_", "chr_id", "position", "ref_allele", "alt_allele"))
    variant_index_lead = variant_index.filter(F.col('SNP_id_index').isin(snp_query.SNP_id.to_list()))
    variant_index_lead = variant_index_lead.select("SNP_id_index","af")
    
    aggregated_df_subset = aggregated_df.select("SNP_id", "gene_id", "V2G_SCORE").withColumn("SNP_id_v2g", F.col("SNP_id")).drop("SNP_id")
    aggregated_df_subset = aggregated_df_subset.groupBy("SNP_id_v2g") \
    .agg(F.max(F.struct("V2G_SCORE", "gene_id")).alias("max_row")) \
    .select(
        F.col("SNP_id_v2g"), 
        F.col("max_row.gene_id").alias("gene_id"),  # Extract gene_id from the struct
        F.col("max_row.V2G_SCORE").alias("V2G_SCORE_MAX")  # Extract max V2G_SCORE from the struct
    )
    filtered_ddf_lead_variant_index = filtered_ddf_lead.join(variant_index_lead, filtered_ddf_lead.SNP_id == variant_index_lead.SNP_id_index, how='inner').drop("SNP_id_index")
    filtered_ddf_lead_variant_index_v2g = filtered_ddf_lead_variant_index.join(aggregated_df_subset, filtered_ddf_lead_variant_index.SNP_id == aggregated_df_subset.SNP_id_v2g, how='inner').drop("SNP_id_v2g")
    filtered_ddf_lead_variant_index_df = filtered_ddf_lead_variant_index_v2g.toPandas()
    filtered_ddf_lead_variant_index_df['gnomad_nfe'] = filtered_ddf_lead_variant_index_df['af'].apply(lambda x: x[gnomad_af] if hasattr(x, gnomad_af) else None)
    filtered_ddf_lead_variant_index_df = filtered_ddf_lead_variant_index_df.drop(['af'],axis=1)
    filtered_ddf_lead_variant_index_df.to_csv(out + "_v2d.tsv", header=True, sep = '\t', index = False)