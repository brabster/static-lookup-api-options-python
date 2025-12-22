import pandas
import test_harness

def loader(path):
    return pandas.read_json(path)


def to_recs_dict(df):
    return {row['id']: row['recommended_products'] for _, row in df.iterrows()}


if __name__ == "__main__":
    test_harness.run_test("uncommitted/recommendations_dataset.json", loader, to_recs_dict)