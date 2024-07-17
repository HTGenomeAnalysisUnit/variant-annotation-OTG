import dask.dataframe as dd
from dask.distributed import LocalCluster
import numpy as np
import argparse
import pandas as pd
import sys
parser = argparse.ArgumentParser(
                    prog='OTG query v2g',
                    description='This program query the OTG variant-to-gene database for a set of variants and gives back the annotations')

parser.add_argument('-v', '--variants_query',
                    type = str,
                    help = 'Set of variants to investigate in the format chr_pos_ref_alt',
					default = False) 

parser.add_argument('-t', '--table_query',
                    type = str,
                    help = 'Set of variants to investigate from a table',
					default = False) 

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
	dtypes = {
	'chr_id': 'object',
	'position': 'int64',
	'ref_allele': 'object',
	'alt_allele': 'object',
	'gene_id': 'object',
	'feature': 'object',
	'type_id': 'object',
	'source_id': 'object',
	'fpred_labels': 'object',
	'fpred_scores': 'float64',
	'fpred_max_label': 'object',
	'fpred_max_score': 'float64',
	'qtl_beta': 'float64',
	'qtl_se': 'float64',
	'qtl_pval': 'float64',
	'qtl_score': 'float64',
	'interval_score': 'float64',
	'qtl_score_q': 'float64',
	'interval_score_q': 'float64',
	'd': 'float64',
	'distance_score': 'float64',
	'distance_score_q': 'float64',
	'overall_score': 'float64',
	'source_list': 'object',
	'source_score_list': 'object'
	}

	#Read reference OTG data
	ddf = dd.read_parquet("/ssu/gassu/reference_data/OpenTargets/22.10/v2g_scored",dtype = dtypes)
	
	columns = list(ddf.columns)
	columns_select = columns[0:8] + columns[10:17] + [columns[20]] + [columns[22]]
	ddf_select = ddf[columns_select]
	
	#Set the SNP variable made of chr_pos_ref_alt
	ddf_select["SNP_id"] = ddf_select["chr_id"] + "_" + ddf_select["position"].astype(str)  + "_" + ddf_select["ref_allele"]  + "_"  + ddf_select["alt_allele"]
	
	#Read variants to query and convert to Dask series
	if(args.variants_query):
		variant_query = dd.read_csv(args.variants_query)
		snp_values = variant_query['SNP_id'].compute()
	elif (args.table_query):
		variant_query = dd.read_csv(args.table_query)
		variant_query["SNP_id"] = variant_query["chr_id"].astype(str) + "_" + variant_query["position"].astype(str)  + "_" + variant_query["ref_allele"]  + "_"  + variant_query["alt_allele"]
		snp_values = variant_query['SNP_id'].compute()
	else:
		
		sys.exit("no query variants specified. Please supply a set of variants using the -v or -t options")
	
	#Join the two tables
	filtered_ddf = ddf_select[ddf_select['SNP_id'].isin(snp_values)].compute()
      
	#Aggregate data produced
	def aggregate_list_qtl(group, type_id):
		filtered_group = group[group['type_id'] == type_id]
		if not filtered_group.empty:
			qtl_scores = filtered_group['qtl_score'].tolist()
			features = filtered_group['feature'].tolist()
			qtl_scores = [np.nan if x is None else x for x in qtl_scores]
			features = [np.nan if x is None else x for x in features]
			sorted_indices = np.argsort(qtl_scores)[::-1]  # Descending order
			qtl_scores = [qtl_scores[i] for i in sorted_indices]
			features = [features[i] for i in sorted_indices]
			max_score_idx = np.nanargmax(qtl_scores)
			max_qtl_score = qtl_scores[max_score_idx]
			max_qtl_feature = features[max_score_idx]
		else:
			qtl_scores, features, max_qtl_score, max_qtl_feature = np.nan, np.nan, np.nan, np.nan

		return qtl_scores,features, max_qtl_score, max_qtl_feature

	def aggregate_list_intervals(group, type_id):
		filtered_group = group[group['type_id'] == type_id]
		interval_scores = filtered_group['interval_score'].tolist() if not filtered_group.empty else np.nan
		#source = filtered_group['source_id'].tolist() if not filtered_group.empty else np.nan
		return (interval_scores)

	# Custom aggregation function
	def custom_agg(group):
		pchic_scores = aggregate_list_intervals(group, 'pchic')
		fantom5_scores = aggregate_list_intervals(group, 'fantom5')
		dhs_scores = aggregate_list_intervals(group, 'dhscor')
		eqtl_scores, eqtl_features, max_eqtl_score, max_eqtl_feature = aggregate_list_qtl(group, 'eqtl')
		pqtl_scores, pqtl_features, max_pqtl_score, max_pqtl_feature = aggregate_list_qtl(group, 'pqtl')
		sqtl_scores, sqtl_features, max_sqtl_score, max_sqtl_feature = aggregate_list_qtl(group, 'sqtl')

		return pd.Series({
		'chr_id': group['chr_id'].iloc[0],
		'position': group['position'].iloc[0],
		'ref_allele': group['ref_allele'].iloc[0],
		'alt_allele': group['alt_allele'].iloc[0],
		'overall_scores': group['overall_score'].iloc[0],
		'distance_score': group['distance_score'].iloc[0],
		'fpred_max': group['fpred_max_score'].max(),
		'fpred_label': group['fpred_max_label'].iloc[0],
		'dhs_scores' :	np.nanmax(dhs_scores) if isinstance(dhs_scores, list) else np.nan,
		'max_pchic_score': np.nanmax(pchic_scores) if isinstance(pchic_scores, list) else np.nan,
		'max_fantom5_score': np.nanmax(fantom5_scores) if isinstance(fantom5_scores, list) else np.nan,
		'max_eqtl_score': max_eqtl_score,
		'max_eqtl_feature': max_eqtl_feature,
		'max_pqtl_score': max_pqtl_score,
		'max_pqtl_feature': max_pqtl_feature,
		'max_sqtl_score': max_sqtl_score,
		'max_sqtl_feature': max_sqtl_feature,
		'eqtl_scores': eqtl_scores,
		'eqtl_features': eqtl_features,
		'pqtl_scores': pqtl_scores,
		'pqtl_features': pqtl_features,
		'sqtl_scores': sqtl_scores,
		'sqtl_features': sqtl_features,
		})

	# Group by SNP_id and gene_id and apply the custom aggregation function
	grouped_filtered = filtered_ddf.groupby(['SNP_id', 'gene_id']).apply(custom_agg).reset_index()
	grouped_filtered = grouped_filtered.replace(np.NaN,'Na')
	grouped_filtered.to_csv(args.out, sep = "\t", index = False)

if __name__ == '__main__':
    main()
