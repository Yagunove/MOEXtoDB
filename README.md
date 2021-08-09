# MOEXtoDB
This is a data engineering project which demonstrates concise and effective data pipeline to load [Moscow Exchange](https://www.moex.com/en/) stock data to SQL Server database. 

Competence showed: Database containerization with Docker, raw data ingestion with REST API (calls setup with Postman), JSON object to pandas dataframe to data structure casts, inserts and cleansing/deduplciation SQL scripts to ensure data quality, Python function programming.


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
  
First, let's connect to our local database using *pyodbc* library:  
```python
docker run -d --name sql_server -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=someThingComplicated1234' -p 1433:1433 mcr.microsoft.com/mssql/server:2019-latest
```

## My case of container virtualization

Developing this project on Apple computer implied Docker container usage to host SQL Server.

To get started we will need to download [Docker for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac?tab=description)  and follow the installation instructions.

```bash
# run following command to install the SQL Server and run its image
docker run -d --name sql_server -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=someThingComplicated1234' -p 1433:1433 mcr.microsoft.com/mssql/server:2019-latest
```
