import numpy as np
import pandas as pd
import anndata as ad

import rpy2.robjects as ro
from rpy2.robjects import pandas2ri, numpy2ri
from rpy2.robjects.packages import importr
from rpy2.robjects import r as R
from rpy2.robjects import globalenv

# Activate automatic conversion
pandas2ri.activate()
numpy2ri.activate()

# Import required R packages
seurat = importr('Seurat')
seurat_object = importr('SeuratObject')
azimuth = importr('Azimuth')
base = importr('base')

### Core Functions ###


def adata_to_seurat(adata: ad.AnnData, use_layer="raw_counts"):
    # Ensure numpy2ri is activated for conversion between NumPy arrays and R objects
    numpy2ri.activate()
    X = adata.layers[use_layer]
    # Handle sparse or dense matrix: Convert to dense if sparse
    if hasattr(X, "toarray"):
        counts = X.toarray().T  # transpose to genes x cells
    else:
        counts = X.T

    # Convert the numpy array to an R object (R matrix)
    r_counts = numpy2ri.py2rpy(counts)

    # Make sure gene names and cell names are set
    genes = adata.var_names.to_list()
    cells = adata.obs_names.to_list()

    # Pass the counts matrix to the R environment
    globalenv = ro.globalenv
    globalenv['counts'] = r_counts

    # Manually construct the row names and column names assignments
    rownames_code = 'rownames(counts) <- c(' + ', '.join([f'"{g}"' for g in genes]) + ')'
    colnames_code = 'colnames(counts) <- c(' + ', '.join([f'"{c}"' for c in cells]) + ')'

    # Execute the R code for row and column names
    ro.r(rownames_code)
    ro.r(colnames_code)

    # Create Seurat object in R
    ro.r('library(Seurat)')
    ro.r('seurat_query <- CreateSeuratObject(counts = counts)')
    ro.r('DefaultAssay(seurat_query) <- "RNA"')
    seurat_obj = ro.r('seurat_query')

    return seurat_obj


def run_azimuth(query, reference_path):
    # RunAzimuth from Azimuth
    mapped = azimuth.RunAzimuth(query=query, reference=reference_path)
    return mapped


def extract_meta_data(mapped_query, umap_name):
    # Access 'meta.data' slot
    meta_data = mapped_query.slots['meta.data']
    # Extract UMAP
    reductions = mapped_query.slots['reductions']
    ref_umap = reductions.rx2(umap_name)
    umap_embeddings = ref_umap.slots['cell.embeddings']

    return meta_data, umap_embeddings


def annotate_adata_azimuth(
    adata: ad.AnnData,
    reference_path: str,
    use_layer: str = "raw_counts",
    umap_name: str = "ref.umap",
) -> ad.AnnData:
    # Load the reference
    # reference = load_reference(reference_path)

    # Convert AnnData to Seurat
    query_seurat = adata_to_seurat(adata)

    # Map
    mapped_query = run_azimuth(query_seurat, reference_path)

    # Extract predictions
    metadata_df, umap_embeddings = extract_meta_data(mapped_query, umap_name)

    # Merge predictions into adata.obs
    adata.obs = adata.obs.join(metadata_df)

    # Add obsm
    adata.obsm[umap_name] = umap_embeddings
    return adata
