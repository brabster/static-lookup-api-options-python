import polars
import test_harness

def loader(path):
    return polars.read_ndjson(path)


def to_recs_dict(df):
    return dict(zip(df["id"], df["recommended_products"]))


if __name__ == "__main__":
    test_harness.run_test("uncommitted/recommendations_dataset.jsonl", loader, to_recs_dict)