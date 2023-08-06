import os
import json

def _load(path: str):
    connections = []
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path) as f:
        config = json.load(f)
        for i in config:
            for y in i.get('source'):
                connections.append({
                    "provider": i.get('provider'),
                    **y
                })
    
    return connections

class DatasourceManager:
    def __init__(self, path: str, providers: dict):
        self.config = _load(path)
        self.providers = providers
    
    def get(self, source_name: str, uid: str, pwd: str):
        config = next((x for x in self.config if x.get('name') == source_name), None)
        if not config:
            raise ValueError(f"Server not found: {server}")
        
        provider = config.get('provider')
        provider_instance = self.providers.get(provider, None)
        
        if provider_instance == None:
            raise ValueError(f"Provider: {provider} is not defined")

        return provider_instance(config, uid, pwd)