__version__ = "0.1.2"
__citation__ = """Singh, Wu, Berger. "Granger causal inference on DAGs identifies genomic loci regulating transcription."  ICLR 2022. 
 Wu, Singh, Walsh, Berger. "An econometric lens resolves cell-state parallax." bioRxiv."""
from . import (
    train,
    utils,
)

from .utils import preprocess_multimodal, schema_representations, identify_all_peak_gene_link_candidates, construct_dag, infer_knngraph_pseudotime, dag_orient_edges, load_multiome_data
from .train import run_gridnet, gridnet_multimodal

__all__ = [
    "train",
    "utils",
    "preprocess_multimodal",
    "schema_representations",
    "identify_all_peak_gene_link_candidates",
    "construct_dag",
    "infer_knngraph_pseudotime",
    "dag_orient_edges",
    "load_multiome_data",
    "run_gridnet",
    "gridnet_multimodal",
]
