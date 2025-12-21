import argparse
import json
import pathlib
import random
import uuid



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a recommendations dataset.")
    parser.add_argument(
        '--num_samples',
        type=int,
        default=1000000,
        help='Number of samples to generate in the dataset.'
    )
    parser.add_argument(
        '--output_file_path_no_extension',
        type=str,
        default='./uncommitted/recommendations_dataset',
        help='Path to the output file where the dataset will be saved.'
    )
    parser.add_argument(
        '--num_recommendations',
        type=int,
        default=10,
        help='Number of recommendations to generate for each sample.'
    )
    parser.add_argument(
        '--product_pool_size',
        type=int,
        default=10000,
        help='Pool of potential products to recommend from.'
    )
    return parser.parse_args()

def as_json(recs, file_path):
    path = file_path.with_suffix('.json')
    with open(path, 'w') as out:
        json.dump(recs, out)
    return path


def as_jsonl(recs, file_path):
    path = file_path.with_suffix('.jsonl')
    with open(path, 'w') as out:
        for rec in recs:
            json.dump(rec, out)
            out.write('\n')
    return path


if __name__ == '__main__':
    args = parse_args()

    product_pool = [str(uuid.uuid4()) for _ in range(args.product_pool_size)]
    print(f'Generated {len(product_pool)} product_ids ({len(set(product_pool))} unique) like "{product_pool[0]}" for product pool.')

    recommendations = [{
        'id': str(uuid.uuid4()),
        'recommended_products': [random.choice(product_pool) for _ in range(args.num_recommendations)]
    }
    for _ in range(args.num_samples)]

    print(f'Generated {len(recommendations)} recommendations like "{recommendations[0]}".')

    out_path_root = pathlib.Path(args.output_file_path_no_extension)
    out_path_root.parent.mkdir(parents=True, exist_ok=True)

    json_path = as_json(recommendations, out_path_root)
    print(f'Wrote recommendations JSON to {json_path}.')

    jsonl_path = as_jsonl(recommendations, out_path_root)
    print(f'Wrote recommendations JSONL to {jsonl_path}.')
    print('Done.')
