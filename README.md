# Project Description

This project is on the creation of financial data APIs, one which includes the general data of IBM / Apple Inc. stocks given a specified time range, and the other includes the average daily running of datapoints such as open price etc.

## Tech Stack

Service code: Python 3.9
Database: MySQL
Containerisation: Docker


## How to run and start API service in local environment
1. In the root directory, do the initial DB setup such that `financial_data` table is created first.
    
Example:
```
python3 get_raw_data.py
```


2. Once setup is done, begin the API service by running the following command:


```
python3 -m flask --app financial/app run

```

3. Open a new terminal window to test out sample API requests against the service

- Statistics API with valid start_date, end_date and symbol

```
curl "http://localhost:5000/api/statistics?start_date=2023-05-10&end_date=2023-05-20&symbol=AAPL"

```
- Statistics API with no symbol (ERROR)

```
curl "http://localhost:5000/api/statistics?start_date=2023-05-10&end_date=2023-05-20"

```

- Statistics API with invalid date or format (ERROR)

```
curl "http://localhost:5000/api/statistics?start_date=2023-05-10&end_date=2023-05-200&symbol=AAPL"

```

- Financial API with no optional parameters

```
curl "http://localhost:5000/api/financial_data"

```
- Financial API with valid date range

```
curl "http://localhost:5000/api/financial_data?start_date=2023-05-10&end_date=2023-05-20"

```

- Financial API with pagination and limit

```
curl "http://localhost:5000/api/financial_data?page=1&limit=3

```

- Financial API with invalid page (ERROR)

```
curl "http://localhost:5000/api/financial_data?page=0&limit=3

```

## Further details on API key

Please avoid storing API keys in codebase for production environment - recommendation is to store outside of code repository e.g. in environment variables or external files with encryption
