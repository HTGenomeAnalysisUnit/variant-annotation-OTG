import pyspark.sql.functions as F
import click
import cloup

@cloup.command("variant_disease", no_args_is_help=True)
@cloup.option_group(
    "V2D parameters",
    cloup.option(
        "--gnomad_af", 
        default="nfe", 
        help="population for which the allele frequency is to be retrieved. Check the README for a list of available populations."),
    cloup.option(
        "--tag",
        default=False,
        is_flag = True,
        help="Flag indicating whether to match both for lead and tag variant. Default is false meaning only the lead variants will be considered."),
    cloup.option(
        "--out",
        default="v2d_out.txt",
        help="The name of the file where to store the results of the query.")
)
@click.pass_context
def variant_disease(ctx,  out: str, gnomad_af: str, tag: bool):
    spark = ctx.obj['spark']
    snp_query = ctx.obj['snp_list'].toPandas()
    #Read OT dataset
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
    #Import variants from OT for allele frequencies
    variant_index = spark.read.parquet("/ssu/gassu/reference_data/OpenTargets/22.10/variant_index")
    variant_index = variant_index.withColumn("SNP_id", F.concat_ws("_", "chr_id", "position", "ref_allele", "alt_allele"))

    filtered_ddf_lead = v2d_variants_select.filter(F.col('SNP_id').isin(snp_query.SNP_id.to_list()))
    variant_index_lead = variant_index.filter(F.col('SNP_id').isin(snp_query.SNP_id.to_list()))
    filtered_ddf_lead_variant_index = filtered_ddf_lead.join(variant_index_lead, filtered_ddf_lead.SNP_id == variant_index_lead.SNP_id, how='inner')
    filtered_ddf_lead_variant_index_df = filtered_ddf_lead_variant_index.toPandas()
    filtered_ddf_lead_variant_index_df['gnomad_nfe'] = filtered_ddf_lead_variant_index_df['af'].apply(lambda x: x.gnomad_nfe if hasattr(x, gnomad_af) else None)
    filtered_ddf_lead_variant_index_df = filtered_ddf_lead_variant_index_df.drop(['af','cadd'],axis=1)
    filtered_ddf_lead_variant_index_df.to_csv(out, header=True, sep = '\t', index = False)