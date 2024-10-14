from pyspark import SparkConf
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import argparse
from cli.variant_disease_gene import variant_disease_gene
#from cli.variant_disease_gene import variant_disease

parser = argparse.ArgumentParser(
                    prog='main',
                    description="Open Targets Genetics annotation")
parser.add_argument('--app_name', type=str, default="OTG Annotation", help='name to give to the spark application')
parser.add_argument('--spark_mem', type=str, default="12g", help='Amount of total memory to give to spark')
parser.add_argument('--spark_cpu', type=str, default="10", help='Total number of cpu to use')
parser.add_argument('--variants_query', type=str, default=None, help='Path of a txt file storing the variants to investigate in the format chr_pos_ref_alt.')
parser.add_argument('--gnomad_af', type=str, default="gnomad_nfe", help='Population for which the allele frequency is to be retrieved. Check the README for a list of available populations.')
parser.add_argument('--tag', type=bool, default=False, help='Flag indicating whether to match both for lead and tag variant. Default is false meaning only the lead variants will be considered.')
parser.add_argument('--out', type=str, default="v2dg_out", help='The name of the file where to store the results of the query.')
args = vars(parser.parse_args())

def main(app_name: str , spark_mem: str , spark_cpu: str, variants_query: str,out: str, gnomad_af: str, tag: bool):
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
    variant_disease_gene(spark_object = spark_session, snp_values = snp_values, out = out, gnomad_af = gnomad_af, tag = tag)

if __name__ == "__main__":
    main(app_name = args['app_name'],
        spark_mem = args['spark_mem'],
        spark_cpu = args['spark_cpu'],
        variants_query = args['variants_query'],
        out = args['out'],
        gnomad_af = args['gnomad_af'],
        tag = args['tag']
        )