import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"
)


def get_penguins():
    return df


def count_penguins():
    return len(df)


def islands():
    return df["island"].unique().tolist()
