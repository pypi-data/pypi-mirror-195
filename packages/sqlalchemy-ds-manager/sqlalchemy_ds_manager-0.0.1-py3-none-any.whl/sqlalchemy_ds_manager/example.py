from sqlalchemy_ds_manager.datasource.manager import DatasourceManager
from sqlalchemy_ds_manager.provider.oracle import OracleProvider
from sqlalchemy_ds_manager.provider.sql_server import SqlServerProvider
from sqlalchemy import text
import pandas as pd
from os import path

def main():
    currentDir = path.dirname(__file__)
    filename = path.join(currentDir, 'datasource.json')

    sql = "Select * from table_name"

    dm = DatasourceManager(filename, providers=dict(
        ORACLE=OracleProvider,
        SQLSERVER=SqlServerProvider
    ))

    datasource = dict(
        golang = dm.get(source_name="golang", uid="go_uid", pwd="go_pwd"),
        rust = dm.get(source_name="rust", uid="rust_uid", pwd="rust_pwd")
    )
    
    with datasource.get('golang').new().connect() as conn:
        df = pd.read_sql(text(sql), conn)
    
if __name__ == "__main__":
    main()