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


def as_pickle(recs, file_path):
    import pickle

    path = file_path.with_suffix('.pkl')
    with open(path, 'wb') as out:
        pickle.dump(recs, out)
    return path


def as_interned_pickle(recs, file_path):
    import copy
    import sys

    recs_interned = copy.deepcopy(recs)

    for rec in recs_interned:
        rec['recommended_products'] = [sys.intern(pid) for pid in rec['recommended_products']]
    return as_pickle(recs_interned, file_path.with_stem(file_path.stem + '_interned'))
    

def as_dbm(recs, file_path):
    import dbm

    path = file_path.with_suffix('.dbm')
    print(f'db impl: {dbm.whichdb(path)}')
    with dbm.open(path, 'n') as db:
        for rec in recs:
            db[rec['id']] = json.dumps(rec['recommended_products'])
    return path


def as_shelve(recs, file_path):
    import shelve

    path = file_path.with_suffix('.shelve')
    with shelve.open(path, 'n') as db:
        for rec in recs:
            db[rec['id']] = rec['recommended_products']
    return path


def select_sample(recs):
    import random
    return random.sample(recs, k=100)

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

    sample_ids_path = out_path_root.with_suffix('.sample.json')
    sample_recs = select_sample(recommendations)
    with open(sample_ids_path, 'w') as sample_out:
        json.dump(sample_recs, sample_out)
    print(f'Wrote sample of 100 ids to {sample_ids_path}.')

    json_path = as_json(recommendations, out_path_root)
    print(f'Wrote recommendations JSON to {json_path}.')

    jsonl_path = as_jsonl(recommendations, out_path_root)
    print(f'Wrote recommendations JSONL to {jsonl_path}.')

    pickle_path = as_pickle(recommendations, out_path_root)
    print(f'Wrote recommendations pickle to {pickle_path}.')

    interned_pickle_path = as_interned_pickle(recommendations, out_path_root)
    print(f'Wrote recommendations interned pickle to {interned_pickle_path}.')

    dbm_path = as_dbm(recommendations, out_path_root)
    print(f'Wrote recommendations dbm to {dbm_path}.')

    shelve_path = as_shelve(recommendations, out_path_root)
    print(f'Wrote recommendations shelve to {shelve_path}.')

    print('Done.')
