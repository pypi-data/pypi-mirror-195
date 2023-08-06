# funEnsemble

Clustering Functional Data Using Ensemble Clustering

## Instructions

1. Install:

```
pip install funEnsemble
```

2. Call the data decomposition module

```python
import funEnsemble.functional_ensemble_clustering as ec

# Data Decomposition Step
data_smooth, mean, principal_componenets, eigen_functions = ec.functional_data_decomposition(data, eigen_dimensions, b_spline_length)

```

3. Call the ensemble clustering module

```python

# Ensemble Clustering Step
membership_matrices, labels = ec.functional_data_clustering(principal_components, K)
```
