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





def extract_elements(x, element):
	if x is np.nan:
		return []
	element_parsed = [item.get(element) for item in x]
	return element_parsed

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

	genes_query = dd.read_csv(args.input)
	genes_values = genes_query['id'].compute()

	#intersect the 2 tables
	filtered_targets_genes = targets[targets['id'].isin(genes_values)]
	intersection_ddf = filtered_targets_genes.merge(associations, left_on='id', right_on='targetId', how='inner').merge(disease, left_on='diseaseId', right_on='id', how='left')
	filtered_df = intersection_ddf.dropna(subset=['score'])
	filtered_df = filtered_df.rename(columns={'id_x': 'id'})
	filtered_df_pd = filtered_df.compute()
	max_score_indices = filtered_df_pd.groupby('id')['score'].idxmax()
	max_score_df = filtered_df_pd.loc[max_score_indices]
	max_score_df['pathways'].fillna(value=np.nan,inplace=True)
	max_score_df['Reactome_pathway_topLevelTerm'] = max_score_df['pathways'].apply(extract_elements, element = "topLevelTerm")
	max_score_df['Reactome_pathway'] = max_score_df['pathways'].apply(extract_elements, element = "pathway")
	max_score_df = max_score_df.rename(columns={"name":"disease_name"})
	columns_to_remove = ['pathways', 'hallmarks','id_y','diseaseId','targetId']

	df_filtered = max_score_df.drop(columns=columns_to_remove)

	def remove_duplicates(arr):
		return list(set(arr))

	df_filtered['Reactome_pathway'] = df_filtered['Reactome_pathway'].apply(remove_duplicates)
	df_filtered['Reactome_pathway_topLevelTerm'] = df_filtered['Reactome_pathway_topLevelTerm'].apply(remove_duplicates)
	df_filtered.to_csv(args.out, sep = "\t", index = False)

if __name__ == '__main__':
    main()