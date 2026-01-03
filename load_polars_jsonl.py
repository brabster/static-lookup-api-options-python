import polars
import test_harness

def loader(path):
    return polars.read_ndjson(path)


def to_recs_dict(df):
    return dict(zip(df["id"], df["recommended_products"]))


def parse_value(value):
    return value.to_list()

if __name__ == "__main__":
    test_harness.run_test("uncommitted/recommendations_dataset.jsonl",
                          loader=loader,
                          to_recs_dict=to_recs_dict,
                          parse_value=parse_value)