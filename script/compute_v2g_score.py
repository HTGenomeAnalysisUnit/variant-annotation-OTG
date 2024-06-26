import pandas as pd
import numpy as np

# Function to calculate the v2g score
def compute_scores(table, source_weights):
    cols = [
        "source_id",
        "chr_id",
        "position",
        "ref_allele",
        "alt_allele",
        "gene_id"
    ]

    # Convert the source weights dictionary to a DataFrame
    weights_df = pd.DataFrame(list(source_weights.items()), columns=['source_id', 'weight'])
    weight_sum = weights_df['weight'].sum()

    # Calculate max values
    agg_df = table.groupby(cols).agg(
        max_qtl=('qtl_score_q', lambda x: np.max(x.fillna(0))),
        max_int=('interval_score_q', lambda x: np.max(x.fillna(0))),
        max_fpred=('fpred_max_score', lambda x: np.max(x.fillna(0))),
        max_distance=('distance_score_q', lambda x: np.max(x.fillna(0))),
    ).reset_index()

    # Calculate source_score
    agg_df['source_score'] = agg_df['max_qtl'] + agg_df['max_int'] + agg_df['max_fpred'] + agg_df['max_distance']

    # Merge with weights
    merged_df = pd.merge(agg_df, weights_df, on='source_id', how='left')

    # Calculate source_score_weighted
    merged_df['source_score_weighted'] = merged_df['weight'] * merged_df['source_score']

    # Calculate overall_score and collect_list
    final_df = merged_df.groupby(cols[1:]).agg(
        ss_list=('source_id', lambda x: list(x)),
        source_scores=('source_score', lambda x: list(x)),
        overall_score=('source_score_weighted', lambda x: x.sum() / weight_sum)
    ).reset_index()

    return final_df