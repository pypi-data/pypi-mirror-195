from sqlalchemy_ds_manager.provider.interface import ProviderInterface
from sqlalchemy import create_engine

class SqlServerProvider(ProviderInterface):
    def __init__(self, config: dict, uid: str, pwd: str):
        server, database = [config.get(i) for i in ["server", "database"]]
        azure = server.split(".database.windows.net") # for azure database
        user = f"{uid}@{azure[0]}" if len(azure) > 1 else uid 
        self.params = dict(
            host=server, database=database, password=pwd, user=user, charset="utf8"
        )
        
    def new(self):
        return create_engine('mssql+pymssql:///', connect_args=self.params)
