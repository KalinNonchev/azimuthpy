# azimuthpy
[![Downloads](https://static.pepy.tech/badge/azimuthpy)](https://pepy.tech/project/azimuthpy)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

`azimuthpy` is a lightweight Python package that enables seamless integration with the [Azimuth](https://azimuth.hubmapconsortium.org/) reference mapping framework using [rpy2](https://rpy2.github.io/).  
It lets you map single-cell RNA-seq datasets (in Python `AnnData` format) to Azimuth references **in Python**.

- Supports direct `AnnData` ➔ `Seurat` conversion
- Pulls predictions and annotations back into `AnnData.obs`
- Fully in-memory, no saving intermediate files

---

## Installation

You need to have **R** installed on your machine with the following R packages:

Install:

```
pip install azimuthpy
```


Or using Conda:

```
# takes 15+ min...
conda env create -f environment.yml
conda activate azimuthpy_conda
```

If r-azimuth is not available through Conda, install it manually inside R:

```
install.packages("remotes")
remotes::install_github("satijalab/azimuth")
```

# How to Use

```
import scanpy as sc
from azimuthpy import annotate_adata_azimuth
```

### Load example dataset
```
adata = sc.datasets.pbmc3k()
adata
```
### Preprocess
```
sc.pp.highly_variable_genes(adata, n_top_genes=2000, subset=True, flavor="seurat_v3") # Optional

# Store raw counts in adata.layers["raw_counts"]
adata.layers["raw_counts"] = adata.X

```
### Map to Azimuth reference

### You can download references from https://azimuth.hubmapconsortium.org/


```

# e.g., from https://azimuth.hubmapconsortium.org/references/#Human%20-%20Lung%20v2%20%28HLCA%29
# -> Zenodo: https://zenodo.org/records/6342228
# wget -c https://zenodo.org/api/records/6342228/files-archive
# unzip ...

adata = annotate_adata_azimuth(adata, reference_path="path/to/folder/",
                                        use_layer="raw_counts",
                                        umap_name="ref.umap")
```

### View predicted labels
```
adata.obs[['predicted.celltype.l1', 'prediction.score.celltype.l1']]
```

For a full tutorial, see `tutorial/gettingStarted.ipynb`.

For more info, take a look at the original [azimuth R page](https://github.com/satijalab/azimuth).
















