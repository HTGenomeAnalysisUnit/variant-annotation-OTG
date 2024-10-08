from pyspark import SparkConf
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import click
import cloup
from cli.variant_disease_gene import variant_disease_gene
#from cli.variant_disease_gene import variant_disease


@cloup.group(name="main", help="Open Targets Genetics annotation", no_args_is_help=True)
@cloup.option_group(
    "Spark parameters",
    cloup.option(
        "--app_name", 
        default="OTG Annotation", 
        help="Path of a txt file storing the variants to investigate in the format chr_pos_ref_alt."),
    cloup.option(
        "--spark_mem",
        default="12g",
        help="The name of the file where to store the results of the query."),
    cloup.option(
        "--spark_cpu",
        default="10",
        help="The name of the file where to store the results of the query."),
    cloup.option(
        "--variants_query", 
        default="variants to query on OTG", 
        help="Path of a txt file storing the variants to investigate in the format chr_pos_ref_alt.")
)

@click.pass_context
def cli_init(ctx, app_name: str , spark_mem: str , spark_cpu: str, variants_query: str) -> SparkSession:
    conf = (
        SparkConf()
        .set("spark.driver.memory", spark_mem)
    )
    spark_session = SparkSession\
        .builder\
        .master(f"local[*]")\
        .appName("test") \
        .config("spark.local.dir", "/scratch/bruno.ariano/tmp_pyspark") \
        .getOrCreate()
    
    variant_query = spark_session.read.csv(variants_query)
    snp_values = variant_query.withColumn("SNP_id",F.col("_c0")).drop("_c0")
    # Passing the Spark session and variants into the context
    ctx.obj = {"spark": spark_session,
                "snp_list": snp_values}  
    return ctx.obj
    
def main():
    cli_init.add_command(variant_disease_gene)
    cli_init(obj={})

if __name__ == "__main__":
    main()