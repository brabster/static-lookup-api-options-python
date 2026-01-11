# static-lookup-api-options-python

Investigating memory utilisation, load time and lookup latency across different implementations in Python. 

Loading static datasets (examples: reference data, configuration, recommendations, cleaned up or pre-analysed data) to be looked up by key and used by another service is a common need. These are not typically "big data" scale, comprising up to millions of records and low-GB scale on disk when uncompressed.

A preferable solution:

- requires minimal resources, especially memory
- has simple, predictable scaling characteristics
- loads new data quickly
- looks up records quickly
- has a simple implementation
- avoids third-party dependencies

Using Python to load these datasets into memory often needs more memory than expected, with Out-Of-Memory (OOM) crashes and excessive infrastructure costs. The default choice for many data practitioners is Pandas, a tool taught in every data science bootcamp, designed for numerical analysis. This repo explores different options using GitHub actions, and [raw data artefacts are avaiable in the Actions tab](https://github.com/brabster/static-lookup-api-options-python/actions/runs/20674448396).

## Conclusion up front

Pandas and Polars are the wrong tool for this job, in particular consuming far more memory than is necessary.

Using Python's built-in `dbm` module allows records to be looked up directly from disk instead of loading into memory, meeting all the needs listed above. Serving requests from a web API using dbm.ndbm performs similarly to serving the requests from memory.

Other options provide different trade-offs of memory utilisation and loading time.

## Experimental setup

[A dataset is generated](./generate_dataset.py) representing a common lookup scenario: looking up a list of product recommendations for a customer, using UUID strings for both customer and product IDs to avoid any assumptions about IDs. There are 1m customers with 10 product recommendations each. Products are picked from a pool of 10k product IDs. The dataset is saved in a variety of formats to support different consuming implementations, along with a sample of 100 randomly-selected customer IDs. The raw JSON dataset is around 450MB uncompressed.

[A test harness](./test_harness.py) loads the appropriate dataset format ten times, simulating the common reload-in-memory approach that usually requires enough memory to hold two copies of the data in memory to enable the swap. (I avoid mutating in-place as that avoids significant classes of errors and uncertainties). The harness then times a look up of the 100 customer ID samples to measure the lookup latency.

The test suite runs on GitHub Actions `ubuntu-slim` runners that have around 5GB of memory available.

[A simple performance test](./load_dbm_serve_test.py) over the most operable options, using the [Locust load testing framework](https://docs.locust.io/en/stable/index.html) tests a simple Flask/gunicorn webapp that wraps the implementation.

## Results (1m customers with 10 recs from 10k products)

![A scatter plot titled "Data Loading Benchmark: Memory vs. Time" comparing 12 data loading methods](./assets/1m_cust_10recs.png)

### [Pandas](https://pandas.pydata.org/)

A data analysis library, the default choice for many data practitioners. 

[load_pandas_json.py](./load_pandas_json.py) and [load_pandas_jsonl.py](./load_pandas_jsonl.py) are the worst-performing cluster.

**Conclusion: memory-hungry and slow, requires third-party packages.**

### [Polars](https://pola.rs/)

A newer data analysis library and alternative to Pandas written in Rust.

[load_polars_json.py](./load_polars_json.py) and [load_polars_jsonl.py](./load_polars_jsonl.py) consume a similar amound of memory to Pandas, but are much faster to reload at around 5 seconds. Relatively high lookup latency.

**Conclusion: even more memory-hungry, quicker to load, slower to lookup, requires third-party packages**

### [Python-native JSON](https://docs.python.org/3/library/json.html)

Using Python's built-in JSON parsing.

[load_json.py](./load_json.py) and [load_jsonl.py](./load_jsonl.py) consume less memory than Pandas and Polars, and have a similar load latency to Polars, but faster lookup.

**Conclusion: a little less memory-hungry, faster lookups.**

### Python-native JSON with [string interning](https://docs.python.org/3/library/sys.html#sys.intern)

Using Python's built-in JSON parsing, but explicitly interning the product ID strings that we know are duplicated many times.

[load_interned_json.py](./load_interned_json.py) and [load_interned_jsonl.py](./load_interned_jsonl.py) use a lot less memory but the interning means it takes longer to load.

**Conclusion: much less memory-hungry, higher load latency.**

### [Python-native pickle](https://docs.python.org/3/library/pickle.html)

Using pickle to store the dictionary structure to disk. Explicit string interning makes little difference, the internals of pickle may cause interning automatically.

[load_pickle.py](./load_pickle.py) and [load_interned_pickle.py](./load_interned_pickle.py) shift work to the write operation, making the load operation much more memory and time-efficient.

Pickle files can contain executable code and can represent a security risk if the pickle file isn't coming from a trustworthy source.

**Conclusion: much less memory-hungry, much faster to load.**

### Key-value lookup from disk with [dbm](https://docs.python.org/3/library/dbm.html) and [shelve](https://docs.python.org/3/library/shelve.html)

Python ships with persistent key-value storage implementing the dictionary API. Instead of loading the dataset into memory, we look up from database file on-demand. As we are atomically swapping the database, we operate in read-only mode and have no read/write-related concurrency issues.

[load_dbm.py](./load_dbm.py) opens a dbm.ndbm database stored by the data generator. The values are stored as JSON strings, and parsed on lookup. [load_shelve.py](load_shelve.py) does the same, but it uses pickle for values, so comes with the same security considerations. Both "reload" instantly and use negligble additional memory to do so.

**Conclusion: instant atomic reloads in constant time and memory with fast lookup performance.**

## Load testing

The load test runs 100 concurrent users over 4 threads, looking up recommendations for the random sample of customer iDs. This was done in the local dev envronment for the pickle-based solution and for the dbm-based solution. The results are similar for the two implementations, with the dbm-based implementation counterintuitively coming out a little faster over each of three runs, perhaps because there was more memory available for the dbm implementation.

Here are example run stats over 60s. The behaviour was similar over several runs for each implementation.

### dbm.ndbm

Response time percentiles (ms, approximated)
|Type    |Name             |     50%|   95%|  100%|# reqs|
|--------|-----------------|--------|------|------|------|
|GET     |/recommendations |      14|    41|   440| 60570|


###  pickle

Response time percentiles  (ms, approximated)
Type    |Name              |     50%|   95%|  100%|# reqs|
--------|------------------|--------|------|------|------|
GET     |/recommendations  |      16|    40|  5000| 55533|

## Improving on dbm - compressed values

The value strings stored in the dbm database can be compressed using standard libraries, further reducing the size of the database file. Doing so results in around a 50% reduction in file size for the 20-recs version (747MB vs 1.5GB), and more if the number of recommendations increases. Likely a worthwhile optimisation for many cases, for negligible decompression overhead. The compression can be found in [generate_dataset.py](generate_dataset.py), and decompression in [serve/app.py](serve/app.py).

## Running serverless in the Cloud

I'm interested in GCP Cloud Run as a specific target and a team-mate flagged a potential issue. Scratch disk in Cloud Run instances is actually backed by memory, not physical disk. That means some of the benefit of using `dbm` is lost because we're really still working in memory.

This no-physical-disk approach is not universal. AWS Fargate, for example, does appear to provide physical disk ephemeral storage. Where real disk is available, using it with dbm should be a viable option without eating into your precious memory.

I've done some more research into a couple of solutions. I use the same [serve/app.py](serve/app.py), baked into a container image defined by [serve/Dockerfile](serve/Dockerfile), running on Cloud Run for the following investigations. The application takes an environment variable `DB_PATH` that toggles its behaviour for the two variants. I ran the two variants in Cloud Run, with each being freshly deployed, warmed up by 10 refreshes of a single cust ID (to avoid effectively caching the 100 test IDs) before running a three minute locust test up to 20 users. I dropped the number of users (i.e. concurrent requests) as I'm trying to check the performance of the system under load rather than scaling under too much load for a basic Flask app.

I'm running my standard 1m/20recs/10k product pool configuration. he Cloud Run instance is the smallest available in Gen2, i.e. 512MB memory. That means I can't actually run most other options as there isn't enough memory to start the instance.

### Using GCS as physical storage under FUSE

It's possible to "mount" storage from Cloud Storage as if it were disk as part of the Cloud Run offering. [serve_scripts/deploy_fuse.sh](serve_scripts/deploy_fuse.sh) shows how it's configured for my test. The file in storage appears as if it were on a local disk, and I set the `DB_PATH` variable to point to the mounted file.

Response time percentiles (approximated, ms)
Type    |Name                                 |     50%|   66%|   75%|   80%|   90%|   95%|   98%|   99%| 99.9%|99.99%|  100%|# reqs
--------|-------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
GET     |/recommendations                     |      13|    14|    15|    16|    23|    35|  1000|  1000|  1200|  1400|  1400| 85100

The performance is much better than I expected, with a 13ms P50 and 1.4s at the max. The instance handled an average of 470 req/sec, and I saw peaks up to 700req/sec.

This setup might work well, but I see operational challenges with the connection to Cloud Storage, which effectively forms a second tier to the application. Montitoring request volumes, latency and cost back to storage might be important to understand behaviour and costs, expecially as more instances scale out. There may be a learning curve to GCS FUSE in practice too, when I moved the file I got errors about stale references and swapping old data for new might not be trivial.

### Baking the data file into the container image

The Dockerfile also copies over the compressed database file into the image and points the `DB_PATH` variable at the local copy. This is a really neat solution, with no moving parts to go wrong, no need for code to swap new data and linear horizontal scaling. If the data is sensitive there could be arguments against storing it in a container registry, but I'm not sure there's any real difference between that and keeping it in some other storage medium - one to think about.

Response time percentiles (approximated, ms)
Type    |Name                                 |     50%|   66%|   75%|   80%|   90%|   95%|   98%|   99%| 99.9%|99.99%|  100%|# reqs
--------|-------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
GET     |/recommendations                     |      13|    14|    15|    16|    20|    30|  1000|  1000|  1200|  1200|  1400| 92918

Similar performance, a little better as we squeezed a few more requests through - 516 req/sec - but I feel that's likely close enough to be within the error bars. Operability is so much better though - there's no backend to worry about here, the instance operates standalone. Swapping new data in is a replacement of the service, an operation that you need to be familiar with anyway, and fits nicely into an immutable architecture approach. The instance is simpler as there's no code or background threads monitoring for and swapping in the data, there is no I/O or compute overhead during a swap, and healthchecks on each new generation can protect against data issues without putting the service at risk.

Cleaning up old images from the registry might need consideration, but for datasets in the MB-low GB ranges I wouldn't expect the image sizes to be problematically large. I think there's a lot to be said for this approach.