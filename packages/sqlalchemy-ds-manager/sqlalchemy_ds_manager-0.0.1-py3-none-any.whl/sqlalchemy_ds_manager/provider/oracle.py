from sqlalchemy_ds_manager.provider.interface import ProviderInterface
from sqlalchemy import create_engine

class OracleProvider(ProviderInterface):
    def __init__(self, config: dict, uid: str, pwd: str):
        server, port, service_name = [config.get(i) for i in ["server", "port", "service_name"]]
        self.params = dict(
            host=server, port=port, password=pwd, user=uid, service_name=service_name
        )
  
    def new(self):
        return create_engine('oracle+oracledb:///', connect_args=self.params)

        