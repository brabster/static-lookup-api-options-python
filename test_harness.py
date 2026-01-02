import json
import pathlib
import resource
import sys
import time

iterations = 10

def max_memory_usage_gb():
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return usage / 1024 / 1024


def default_to_recs_dict(list_of_dicts):
    return {item['id']: item['recommended_products'] for item in list_of_dicts}


def run_test(path, loader, to_recs_dict=default_to_recs_dict):
    live = None
    start = time.time()

    for _ in range(iterations):
        temp_data = loader(path)

        live = to_recs_dict(temp_data)
        print(f'{len(live)} records, {max_memory_usage_gb()}GB MaxRSS')

    end = time.time()
    elapsed = end - start

    print(f'Example record: {next(iter(live.items()))}')
    print(f'Done - {max_memory_usage_gb()}GB MaxRSS')

    script_name = pathlib.Path(sys.argv[0]).stem
    out_path = pathlib.Path('uncommitted') / 'outputs' / 'logs' / (script_name + '_log.json')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(out_path, 'w') as log:
        log.write(json.dumps({
            'script': script_name,
            'num_records': len(live),
            'max_memory_gb': max_memory_usage_gb(),
            'elapsed_time_s': elapsed,
            'mean_time_per_iteration_s': elapsed / iterations
        }))
