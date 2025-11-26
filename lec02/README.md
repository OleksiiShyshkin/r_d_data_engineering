# Sales Data Pipeline

This project contains two Flask-based ETL jobs:
- **Job 1:** Downloads sales data from an external API and stores it in raw JSON files.
- **Job 2:** Reads these JSON files and converts them into Avro format for the staging layer.

---

## Job 1 — API → Raw JSON

**Description:**  
A Flask web service running on port **8081** that fetches sales data from the API  
`https://fake-api-vycpfa6oca-uc.a.run.app/sales` and saves it to the `raw` directory.

### Run the service
```bash
export AUTH_TOKEN=2b8d97ce57d401abd89f45b0079d8790edd940e6
python -m lec02.job1.main
```
### Trigger the job
```
curl -X POST http://localhost:8081/sales \
  -H "Content-Type: application/json" \
  -d '{
        "report_date": "2022-08-09",
        "raw_dir": "/tmp/file_storage/raw/sales/2022-08-09"
      }'
```
### Output example
```
/tmp/file_storage/raw/sales/2022-08-09/sales_2022-08-09_1.json
/tmp/file_storage/raw/sales/2022-08-09/sales_2022-08-09_2.json
...
```
### Key features
- Reads secret token from the environment (AUTH_TOKEN)
- Idempotent — cleans raw_dir before writing new data
- Paginates through API responses until pages end (404)
- Saves each page in a separate JSON file

---

## Job 2 — Raw JSON → Avro (Staging)

**Description:**  
A Flask web service running on port **8082** that reads all JSON files
from the raw directory and converts them into a single Avro file in the stg directory.

### Run the service
```
python -m lec02.job2.main
```

### Trigger the job
```
curl -X POST http://localhost:8082/stg \
  -H "Content-Type: application/json" \
  -d '{
        "raw_dir": "/tmp/file_storage/raw/sales/2022-08-09",
        "stg_dir": "/tmp/file_storage/stg/sales/2022-08-09"
      }'
```

### Output example
```
/tmp/file_storage/stg/sales/2022-08-09/sales_data.avro
```

### Key features
- Reads all .json files from the raw folder
- Automatically generates Avro schema based on JSON keys
- Writes data using fastavro
- Idempotent — cleans stg_dir before writing

## Project Structure
```
lec02/
 ├── job1/
 │    ├── main.py
 │    ├── bll/sales_api.py
 │    └── requirements.txt
 └── job2/
      ├── main.py
      ├── bll/convert_to_avro.py
      └── requirements.txt
```

## How to Verify
1. Run **Job 1** — check JSON files in `/tmp/file_storage/raw/sales/...`
2. Run **Job 2** — check .avro file in `/tmp/file_storage/stg/sales/...`
3. Both Flask servers can run simultaneously on ports **8081** and **8082**