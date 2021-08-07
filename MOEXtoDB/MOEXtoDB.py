import requests
import pandas as pd
import json
import pyodbc
import datetime as DT

### CONNECTION ####
def connection():
    import pyodbc
    import json

    # setting parameters
    with open('connection.json') as f:
        conn_element = json.load(f)

    # pyodbc connection string
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' 
                          +conn_element["server"]
                          +';DATABASE='
                          +conn_element["database"]
                          +';UID='
                          +conn_element["username"]
                          +';PWD=' 
                          + conn_element["password"], autocommit=True)
    
    # initializing cursor
    cursor = conn.cursor()
    
    print("Successfully connected")
    return(conn,cursor)
    
### MAKING API CALL TO MOEX ###
def api_call(ticker = 'LKOH', date_from=0): 
    
    ### If no date is given, take one week ago from current date
    if date_from==0:
        date_from = (DT.datetime.today()-DT.timedelta(days=7)).strftime('%Y-%m-%d')
     
    ### Check validity of the given date
    try:
        DT.datetime.strptime(date_from, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    ### Making the API call
    url = 'https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/'+ticker+'.json?iss.json=extended&from='+date_from+''
    response = requests.request('GET', url)
    
    ### Parsing JSON object into data structure (list of dict) and then parsing out values
    values = json.loads(response.text)
    data = values[1]['history'][1]
    
    ### Checking the output
    if(not data):
        raise ValueError("Ticker name or date is incorrect")
        
    ### Loading data into pandas dataframe before transfering it to database
    df = pd.DataFrame(data)
    df = df[['TRADEDATE', 'SECID','CLOSE']]
    
    return(df)

### INSERTING DATA IN THE DATABASE ###
def db_insert(cursor, df):

    # creating final table with if-not-exists feature which makes this code universal for the initial run and further ones 
    stmt1 = '''
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='t_stock_history' AND xtype='U')
    CREATE TABLE [dbo].[t_stock_history]
    ([TRADEDATE] date,[SECID] [nvarchar](255) NULL ,[CLOSE] float)'''

    # creating buffer which later gives us update option with deduplication
    stmt2= '''
    CREATE TABLE [dbo].[buff_stock_history]([TRADEDATE] date,[SECID] [nvarchar](255) NULL ,[CLOSE] float )'''

    # executing statements
    for st in [stmt1,stmt2]:
        cursor.execute(st)

    # insert data from API to buffer
    for index, row in df.iterrows():
        cursor.execute('INSERT INTO dbo.buff_stock_history ([TRADEDATE],[SECID],[CLOSE]) VALUES(?,?,?)', row.TRADEDATE, row.SECID, row.CLOSE)

    # deleting from final table rows that are present in the buffer
    stmt3 = '''
    DELETE t1 
    FROM [dbo].[t_stock_history] t1 
    JOIN [dbo].[buff_stock_history] t2 
    ON t1.TRADEDATE = t2.TRADEDATE AND t1.SECID = t2.SECID AND t1.[CLOSE]=t2.[CLOSE]'''

    stmt4= '''
    INSERT INTO [dbo].[t_stock_history] 
    SELECT * FROM [dbo].[buff_stock_history]'''

    # drop buffer
    stmt5 = 'DROP TABLE [dbo].[buff_stock_history]'

    for st in [stmt3, stmt4, stmt5]:
        cursor.execute(st)
    
    return(0)

### CLOSING CONNECTION ###
def close_connection(conn,cursor):
    cursor.close()
    del cursor
    conn.close()
    print("Connection was closed successfully")
    return(0)
   

