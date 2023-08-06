from sqlalchemy_ds_manager.datasource.manager import DatasourceManager
from sqlalchemy_ds_manager.provider.oracle import OracleProvider
from sqlalchemy_ds_manager.provider.sql_server import SqlServerProvider
from sqlalchemy_ds_manager.cache.file import FileCache
from sqlalchemy import text
import pandas as pd
import time
from os import path

currentDir = path.dirname(__file__)
filename = path.join(currentDir, 'datasource.json')
folder = path.join(currentDir, 'cache_files')

dm = DatasourceManager(filename, providers=dict(
    ORACLE=OracleProvider,
    SQLSERVER=SqlServerProvider
))

datasource = dict(
    golang = dm.get(source_name="golang", uid="go_uid", pwd="go_pwd"),
    rust = dm.get(source_name="rust", uid="rust_uid", pwd="rust_pwd")
)

def main():
    sql = "Select * from table_name"
    fc = FileCache(folder)
    df = getSql(sql, "golang", fc)
    
def getSql(sql, source_name: str, fc):
    exist = fc.find(sql)
    if exist == None:
        with datasource.get(source_name).new().connect() as conn: 
            start = time.time()
            df = pd.read_sql(text(sql), conn)
            duration = round(time.time() - start, 2) 
            filename = fc.add(sql, duration)
            df.to_pickle(filename)
            return df
    else:
        return pd.read_pickle(exist)

if __name__ == "__main__":
    main()