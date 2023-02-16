from sqlite3 import OperationalError
def process_average_daily_data(cursor, start_date, end_date, symbol):
    result = {}
    columnList = ["open_price", "close_price", "volume"]
    for column in columnList:
        try:
            command = f"SELECT AVG({column}) FROM financial_data WHERE 1=1 AND DATE BETWEEN '{start_date}' AND '{end_date}' AND SYMBOL = '{symbol}'"
            cursor.execute(command)
            result[f"average_daily_{column}"] = cursor.fetchall()[0][0]

        except OperationalError as msg:
            result["error"] = msg
            return result
    return result