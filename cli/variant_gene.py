from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, DoubleType
import pyspark.sql.functions as F
from pyspark.sql.functions import col, broadcast, when
import cloup
import click

@cloup.command("variant_gene", no_args_is_help=True)
@cloup.option_group(
    "V2G parameters",
    cloup.option(
        "--out",
        default="v2g_out.txt",
        help="The name of the file where to store the results of the query.")
)
@click.pass_context
def variant_gene(ctx, out: str = "out_v2d"):
    spark = ctx.obj['spark']  # Fetch the Spark session from the context
    snp_values = ctx.obj['snp_list']
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
    ddf = spark.read.parquet("/ssu/gassu/reference_data/OpenTargets/22.10/v2g_scored")

    columns_select = ['chr_id', 'position', 'ref_allele', 'alt_allele', 'gene_id', 'feature', 'type_id', 
                      'source_id', 'fpred_max_label', 'fpred_max_score', 'qtl_score', 'interval_score', 
                      'd', 'distance_score', 'overall_score']
    
    ddf_select = ddf.select(columns_select)
    ddf_select = ddf_select.withColumn("SNP_id", F.concat_ws("_", F.col("chr_id"), F.col("position"), F.col("ref_allele"), F.col("alt_allele")))
    
    # Read variants to query
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
    aggregated_df_pd.to_csv(out, header=True)
