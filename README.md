bank-transaction-etl/
│
├── data/
│   ├── raw/              # original data
│   ├── processed/        # cleaned data
│   └── output/           # analytics results
│
├── notebooks/            # for exploration (Pandas)
│
├── src/
│   ├── ingestion/        # loading data
│   ├── cleaning/         # validation + cleaning
│   ├── transformation/   # feature engineering
│   ├── analytics/        # analysis
│   ├── anomaly/          # anomaly detection
│   └── utils/            # helper functions
│
├── sql/                  # SQL queries
│
├── config/               # configs (paths etc.)
│
├── main.py               # pipeline runner
├── requirements.txt
└── README.md