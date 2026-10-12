# Data source

The Iris dataset originated at the UCI Machine Learning Repository: https://archive.ics.uci.edu/dataset/53/iris (CC BY 4.0; DOI 10.24432/C56C76).

`python -m quality.data` downloads the scikit-learn mirror with the original 150 examples, normalizes its header into named columns and writes `iris.csv`. The file is openly licensed with attribution and is not sensitive. No customer or private data is uploaded.

Iris is a deliberately small demonstration dataset. A production observability platform should support larger open datasets, schema contracts, streaming volumes, drift tracking and historical baselines.
