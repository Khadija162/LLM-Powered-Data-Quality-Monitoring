"""Download an open-data Iris dataset from its published open-source upstream mirror."""
import argparse
from pathlib import Path
import requests
URL = "https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/sklearn/datasets/data/iris.csv"


def download(output="data/public/iris.csv"):
    response = requests.get(URL, timeout=30)
    response.raise_for_status()
    header = response.text.splitlines()[0].strip()
    if header != "150,4,setosa,versicolor,virginica":
        raise ValueError("Unexpected upstream Iris format")
    # scikit-learn's iris.csv has a metadata first line and 150 numeric rows.
    from io import StringIO
    import pandas as pd
    frame = pd.read_csv(StringIO(response.text), skiprows=1, header=None,
                        names=["sepal length (cm)", "sepal width (cm)",
                               "petal length (cm)", "petal width (cm)", "target"])
    if len(frame) != 150:
        raise ValueError("Unexpected row count")
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="data/public/iris.csv")
    args = p.parse_args()
    print(download(args.output))
