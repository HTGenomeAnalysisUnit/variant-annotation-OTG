import dask.dataframe as dd
from dask.distributed import LocalCluster
import numpy as np
import argparse
import pandas as pd

parser = argparse.ArgumentParser(
                    prog='OT query for annotations',
                    description='This program query the OT database for a set of genes and gives back the annotations')

parser.add_argument('-i', '--input',
                    type = str,
                    help = 'Set of genes to investigate') 

parser.add_argument('-o', '--out',
                    type = str,
                    help = 'File name of the output',
                    )

args = parser.parse_args()

#Here I create a simple local cluster for the node where the program run. I could create a Dask cluster directly though it didn't seem worthed for the computation

def main():
	cluster = LocalCluster()
	client = cluster.get_client()


    	# Your Dask code here

	# Define the data types for the columns read
	dtypes_associations = {
	'targetId': 'object',
	'score': 'float64',
	'diseaseId': 'object'
	}


    	# Your Dask code here

	# Define the data types for the columns read
	dtypes_disease = {
	'name': 'object',
	'id': 'object',
	}


    # Your Dask code here

	# Define the data types for the columns read
	dtypes_targets = {
	'id': 'object',
	'approvedSymbol': 'object',
	'biotype': 'object',
	'approvedName': 'object',
	'hallmarks': 'object',
	'pathways': 'object'
	}
	
	targets = dd.read_parquet("/ssu/gassu/reference_data/OpenTargets/24.03/targets",columns = dtypes_targets)
	associations = dd.read_parquet("/ssu/gassu/reference_data/OpenTargets/24.03/associationByOverallDirect",columns = dtypes_associations)
	disease = dd.read_parquet("/ssu/gassu/reference_data/OpenTargets/24.03/diseases",columns = dtypes_disease)
	
	genes_query = dd.read_csv("/ssu/gassu/GAU_tools/OT_notate/samples_genes.txt")
	genes_values = genes_query['id'].compute()
	
    #intersect the 2 tables
	filtered_targets_genes = targets[targets['id'].isin(genes_values)].compute()
	intersection_ddf = filtered_targets_genes.merge(associations, left_on='targetId', right_on='id', how='inner') \
                            .merge(disease, left_on='diseaseId', right_on='id', how='left')
	print(intersection_ddf)