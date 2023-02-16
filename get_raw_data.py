import requests
import sqlite3
from sqlite3 import OperationalError, IntegrityError

## check how to store the api key in dev and production, and error handling if api were to change

def runSqlScript(filename, con, command=""):
    if (len(command) == 0):
        # Open schema.sql file and run in read mode
        fd = open(filename, "r")
        sqlFile = fd.read()
        fd.close()
        sqlCommands = sqlFile.split(";")
    else:
        sqlCommands = [command]

    for command in sqlCommands:
        try:
            con.execute(command)
        except IntegrityError as msg:
            ## for debug purposes
            # print(command)
            # print(msg)
            print("[WARN] Data has already been inserted")
        except OperationalError as msg:
            ## for debug purposes
            # print(command)
            print("[ERROR] Command skipped due to: ", msg)
            return True
    return False

# STEP 1: Setup DB table with schema
con = sqlite3.connect('python_assignment.db')
## Initialise financial_data table first if it does not exist yet
db_setup_failure = runSqlScript("schema.sql", con)

if db_setup_failure:
    print(f"FAILURE: DB table setup failure")

else:
    ## STEP 2: Retrieve API result for 2 companies IBM and Apple Inc and do the required processing of data
    apiKey = "MRF6VRT0VHQXCLI7"
    processed_data = []
    api_failure = False
    api_error_message = ""
    for company in ["IBM", "AAPL"]:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={company}&outputsize=compact&apikey={apiKey}"
        response = requests.get(url)
        data = response.json()
        ## Error handling - since status 200 is returned even when there is error, check 'Error Message' key in the response data instead
        if data.get('Error Message') != None:
            api_error_message = data['Error Message']
            ## If any API call failures, do not persist any data in DB table
            api_failure = True
            break
        else:
            ## days might not be accurate to 2 weeks since weekends are skipped i.e saturday and sunday
            days = 14
            symbol = data["Meta Data"]["2. Symbol"]
            ## skip metadata and go into time series daily data
            daily_data = data["Time Series (Daily)"]
            insertSyntax = "INSERT INTO financial_data (symbol, date, open_price, close_price, volume) VALUES('{symbol}', '{date}', '{open_price}', '{close_price}', '{volume}');"
            for index, key in enumerate(daily_data):
                if index >= days: 
                    break
                temp = {}
                temp["symbol"] = symbol
                temp["date"] = key
                temp["open_price"] = daily_data[key]["1. open"]
                temp["close_price"] = daily_data[key]["4. close"]
                temp["volume"] = daily_data[key]["6. volume"] 
                processed_data.append(temp)
             
    if api_failure:
        print(f"FAILURE: API call issue - {api_error_message}")
    else:
        ## STEP 3: Persist data in DB table (financial_data)
        sqlFailure = False
        for row in processed_data:
            sqlFailure &= runSqlScript("", con, insertSyntax.format(symbol=row["symbol"], date=row["date"], open_price=row["open_price"], close_price=row["close_price"], volume=row["volume"]))
        if sqlFailure:
            print(f"FAILURE: Error while executing SQL statements for inserting processed financial data")
        else:
            ## Persist and commit all transactions made 
            con.commit()
            print(f"SUCCESS: All non-duplicated records are persisted in local DB table")
