# MOEXtoDB
This is a data engineering project which demonstrates concise and effective data pipeline to load [Moscow Exchange](https://www.moex.com/en/) stock data to SQL Server database. 

Competence showed: Database containerization with Docker, raw data ingestion with REST API (calls were setup using Postman), JSON object to pandas dataframe to data structure casts, inserts and cleansing/deduplciation SQL scripts to ensure data quality, Python function programming.


<center>
<img src="https://github.com/Yagunove/MOEXtoDB/blob/f3414ccfcdf1dbe00cae2f383e8db9ed38aac85e/media/conceptual_flowchart.png" style="width:70%;"/>
</center>

## Table of contents

- [Table of contents](#table-of-contents)
- [Getting started](#getting-started)
- [A quick example](#a-quick-example)
- [My case of container virtualization](#my-case-of-container-virtualization)


## Getting started  
The following command will install required dependencies:
```bash
pip install -r requirements.txt
```
## A quick example

Here is an example on real life stock data, demonstrating how easy it is to get the data for any given time period in your database.  
  
First, let's connect to our local database using *pyodbc* library and get connection and cursor objects. The connection details should be specified in ```connection.json``` file.  

```python 
>>> conn,cursor = connection()
'Connected succesfully'
```

To make GET call to MOEX database, specify the required ticker and start date (default parameters are "LKOH" and one week prior to the current date). Function returns Pandas dataframe object to be loaded in the database.   

```python 
>>> df = api_call('MGNT')
>>> df
```
Output:
```
       TRADEDATE	SECID	CLOSE
0	2021-07-30	MGNT	5337.0
1	2021-08-02	MGNT	5321.0
2	2021-08-03	MGNT	5383.0
3	2021-08-04	MGNT	5415.0
4	2021-08-05	MGNT	5489.5
5	2021-08-06	MGNT	5458.5
```

Now we can insert results into database table *t_stock_history*. To deal with deduplication, we create a buffer and update results in the final table if they are already present in the final table. All SQL queries and data manupulation are included in *db_insert* function. 

```python 
>>> db_insert(cursor,df) # returns zero if success
0
```
Finally, we can close connection to the database to allow changes:

```python 
>>> close_connection(conn, cursor)
'Connection was closed successfully'
```

We can now enjoy quering our data with any database GUI - my tool of choice is Azure Data Studio since there is no SQL Server Management Studio for macOS.

<center>
<img src="https://github.com/Yagunove/MOEXtoDB/blob/16fada4f16168ee792f62c559743741e63f1047f/media/sample_answerset.png" style="width:70%;"/>
</center>


## My case of container virtualization

Developing this project on Apple computer implied Docker container usage to host SQL Server.

To get started we will need to download [Docker for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac?tab=description)  and follow the installation instructions.

```bash
# run following command to install the SQL Server and run its image
docker run -d --name sql_server -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=someThingComplicated1234' -p 1433:1433 mcr.microsoft.com/mssql/server:2019-latest
```
