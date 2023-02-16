## To start localhost for API usage
from flask import Flask, jsonify, request
import sqlite3
import time
from utils import is_date_format_valid, is_date_valid, count_pages
from api.process_average_daily_data import process_average_daily_data
from api.select_financial_data import select_financial_data


app = Flask(__name__)

con = sqlite3.connect('python_assignment.db', check_same_thread=False)
cursor = con.cursor()

@app.route("/api/statistics", methods=['GET'])
def get_statistics():
    start_date = request.args.get("start_date", default="", type=str)
    end_date = request.args.get("end_date", default="", type=str)
    symbol = request.args.get("symbol", default="", type=str)

    response = {}
    response["data"] = {}
    response["info"] = {}

    ## Params validation
    if len(symbol) == 0 or len(start_date) == 0 or len(end_date) == 0:
        response["info"]["error"] = "[Query params invalid] Start date, end date and symbol should not be empty"
        return response, '400'
    if symbol not in ["IBM", "AAPL"]:
         response["info"]["error"] = "[Query params invalid] Symbol should be either IBM or AAPL"
         return response, '400'
    # date is not valid or not in correct format
    if not is_date_format_valid(start_date) or not is_date_format_valid(end_date):
        response["info"]["error"] = "[Query params invalid] Either start date or end date format is not valid"
        return response, '400'
    if not is_date_valid(start_date) or not is_date_valid(end_date):
        response["info"]["error"] = "[Query params invalid] Either start date or end date value is not valid"
        return response, '400'
    if time.strptime(start_date, "%Y-%m-%d") > time.strptime(end_date, "%Y-%m-%d"):
                response["info"]["error"] = "[Query params invalid] Start date cannot be later than end date"
                return response, '400';

    result = process_average_daily_data(cursor, start_date, end_date, symbol)
    if result.get('error') != None:
        response["info"]["error"] = f"[Internal Server Error] {result.get('error')}"
        return response, '500';

    for key,value in result.items():
         response["data"][key] = "{:.2f}".format(value)
         
    response["data"]["start_date"] = start_date
    response["data"]["end_date"] = end_date
    response["data"]["symbol"] = symbol
    return jsonify(response)


@app.route("/api/financial_data", methods=['GET'])
def get_financial_data():
    start_date = request.args.get("start_date", default="1000-01-01", type=str)
    end_date = request.args.get("end_date", default="9999-12-31", type=str)
    symbol = request.args.get("symbol", default="", type=str)
    limit = request.args.get("limit", default=5, type=int)
    page = request.args.get("page", default=1, type=int)

    response = {}
    response["data"] = []
    response["pagination"] = {}
    response["info"] = {}

    ## Params validation
    if page <= 0 or limit <= 0:
        response["info"]["error"] = "[Query params invalid] Page number or limit cannot be less than 0"
        return response, '400'
    if len(symbol) > 0 and symbol not in ["IBM", "AAPL"]:
         response["info"]["error"] = "[Query params invalid] Symbol should be either IBM or AAPL"
         return response, '400'
    # date is not valid or not in correct format
    if not is_date_format_valid(start_date) or not is_date_format_valid(end_date):
        response["info"]["error"] = "[Query params invalid] Either start date or end date format is not valid"
        return response, '400'
    if not is_date_valid(start_date) or not is_date_valid(end_date):
        response["info"]["error"] = "[Query params invalid] Either start date or end date value is not valid"
        return response, '400'
    if time.strptime(start_date, "%Y-%m-%d") > time.strptime(end_date, "%Y-%m-%d"):
                response["info"]["error"] = "[Query params invalid] Start date cannot be later than end date"
                return response, '400';

    result = select_financial_data(cursor, start_date, end_date, symbol)
    if result.get("error") != None:
        response["info"]["error"] = f"[Internal Server Error] {result.get('error')}"
        return response, '500';
    result = result.get("data")
        
    ## Construct api response structure
    for row_index in range(page*limit-limit, min(len(result),page*limit)):
        row_object = {}
        row_object["symbol"] = result[row_index][0]
        row_object["date"] = result[row_index][1]
        row_object["open_price"] = result[row_index][2]
        row_object["close_price"] = result[row_index][3]
        row_object["volume"] = result[row_index][4]
        response["data"].append(row_object)

        response["pagination"]["count"] = len(result)
        response["pagination"]["page"] = page
        response["pagination"]["limit"] = limit
        response["pagination"]["pages"] = count_pages(len(result), limit)
    
    return jsonify(response)