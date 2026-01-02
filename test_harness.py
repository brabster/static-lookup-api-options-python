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


def parse_value_default(value):
    return value


def load_sample():
    path = pathlib.Path('uncommitted/recommendations_dataset.sample.json')
    with open(path, 'r') as f:
        return json.load(f)


def run_test(path, loader, to_recs_dict=default_to_recs_dict, parse_value=parse_value_default):
    live = None
    start = time.time()

    for _ in range(iterations):
        temp_data = loader(path)

        live = to_recs_dict(temp_data)
        print(f'{len(live)} records, {max_memory_usage_gb()}GB MaxRSS')
    
    end = time.time()
    load_elapsed = end - start

    sample = load_sample()

    start = time.time()

    for record in sample:
        recs = parse_value(live[record['id']])
        assert recs == record['recommended_products']
    
    end = time.time()
    sample_elapsed = end - start

    print(f'Example record: {live[sample[0]['id']]}')
    print(f'Done - {max_memory_usage_gb()}GB MaxRSS')
    print(f'Load elapsed time over {iterations} iterations: {load_elapsed}s')
    print(f'Request sample elapsed time: {sample_elapsed * 1000}ms')

    script_name = pathlib.Path(sys.argv[0]).stem
    out_path = pathlib.Path('uncommitted') / 'outputs' / 'logs' / (script_name + '_log.json')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(out_path, 'w') as log:
        log.write(json.dumps({
            'script': script_name,
            'num_records': len(live),
            'max_memory_gb': max_memory_usage_gb(),
            'load_elapsed_time_s': load_elapsed,
            'load_mean_time_per_iteration_s': load_elapsed / iterations,
            'req_sample_elapsed_time_ms': sample_elapsed * 1000,
            'req_sample_mean_time_per_req_ms': (sample_elapsed / len(sample)) * 1000
        }))
