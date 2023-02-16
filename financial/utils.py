import re

## check for date validity
def is_date_valid(date):
    def is_leap_year(year):
        year = int(year)
        ## Definition of leap year: https://en.wikipedia.org/wiki/Leap_year#:~:text=calendar%2C%20below.-,Gregorian%20calendar,-%5Bedit%5D
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return True
        return False
    year,month,day = date.split("-")
    max_day_for_month = [0, 31, 29 if is_leap_year(year) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return (1 <= int(month) <= 12 and 1 <= int(day) <= max_day_for_month[int(month)])

## check for date regex
def is_date_format_valid(date):
    return re.search("[0-9]{4}-[0-9]{2}-[0-9]{2}", date)

## determine pagination count, where count is the total number of results returned without considering pagination or limit
def count_pages(count, limit):
    if count % limit == 0:
        return count // limit
    else:
        ## need to add 1 page more if not enough exact pages to contain all data
        ## e.g if 6 results and 4 per page, then 1st page to contain 4, and 2nd page to contain 2
        ## or e.g. if 6 results and 7 per page, you still need min 1 page to contain the results
        return count // limit + 1