import pandas as pd


df = pd.read_csv(
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"
)


def get_count():
    return df.count()
