import resource

def max_memory_usage_gb():
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return usage / 1024 / 1024

def default_to_recs_dict(list_of_dicts):
    return {item['id']: item['recommended_products'] for item in list_of_dicts}

def run_test(path, loader, to_recs_dict=default_to_recs_dict):
    live = None

    for _ in range(10):
        temp_data = loader(path)

        live = to_recs_dict(temp_data)
        print(f'{len(live)} records, {max_memory_usage_gb()}GB MaxRSS')

    print(f'Example record: {next(iter(live.items()))}')
    print(f'Done - {max_memory_usage_gb()}GB MaxRSS')
