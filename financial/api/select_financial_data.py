## To start localhost for API usage
from sqlite3 import OperationalError
def select_financial_data(cursor, start_date, end_date, symbol):
    result = {}
    try:
        command = "SELECT * FROM financial_data WHERE 1=1"
        if len(start_date) != 0 and len(end_date) != 0:
            command += f" AND DATE BETWEEN '{start_date}' AND '{end_date}'"
        elif len(end_date) != 0:
            command += f" AND DATE <= '{end_date}'"
        elif len(start_date) != 0:
            command += f" AND DATE >= '{start_date}'"
            
        if len(symbol) != 0:
            command += f" AND SYMBOL= '{symbol}'"
        
        ## It is possible to consider rownum filtering, but because total results before filtering by page / limit is required
        cursor.execute(command)
        result["data"] = cursor.fetchall()

    except OperationalError as msg:
        result["error"] = msg
    
    return result