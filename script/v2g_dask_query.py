import dask.dataframe as dd
from dask.distributed import LocalCluster
import argparse

parser = argparse.ArgumentParser(
                    prog='OTG query v2g',
                    description='This program query the OTG variant-to-gene database for a set of variants and gives back the annotations')

parser.add_argument('-i', '--input',
                    type = str,
                    help = 'Set of variants to investigate') 

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
	columns_select = columns[0:8] + columns[12:14] + [columns[22]]
	ddf_select = ddf[columns_select]
	
	#Set the SNP variable made of chr_pos_ref_alt
	ddf["SNP_id"] = ddf["chr_id"] + "_" + ddf["position"].astype(str)  + "_" + ddf["ref_allele"]  + "_"  + ddf["alt_allele"]
	
	#Read variants to query and convert to Dask series
	variant_query = dd.read_csv(args.input)
	snp_values = variant_query['SNP_id'].compute()
	
	#Join the two tables
	filtered_ddf = ddf_select[ddf_select['SNP_id'].isin(snp_values)].compute()
	filtered_ddf.to_csv(args.out, sep = "\t")


if __name__ == '__main__':
    main()


