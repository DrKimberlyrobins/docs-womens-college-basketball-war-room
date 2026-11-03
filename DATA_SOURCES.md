# Source and licensing register

The system does **not** assert authorization to scrape ESPN, NCAA, Her Hoop Stats, Torvik, CJH, Kambi or Kalshi.

## Supported immediately
Source-labeled JSON exports that the repository owner is permitted to use. The ingest command is:

`python data_pipeline.py permitted_schedule.json --output data/dashboard.json`

Expected schema:
```json
{"source":"provider and license reference","retrieved_utc":"2026-11-03T12:00:00Z","games":[{"id":"provider-stable-id","away":"Visitor","home":"Host","tipoff_utc":"2026-11-04T01:00:00Z","status":"scheduled"}]}
```

No live provider has yet been connected or licensed. Missing records are not silently imputed.
