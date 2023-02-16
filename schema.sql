CREATE TABLE IF NOT EXISTS financial_data(symbol CHAR, date DATE, open_price DECIMAL(10,2), close_price DECIMAL(10,2), volume UNSIGNED MEDIUMINT, PRIMARY KEY(symbol, date));
