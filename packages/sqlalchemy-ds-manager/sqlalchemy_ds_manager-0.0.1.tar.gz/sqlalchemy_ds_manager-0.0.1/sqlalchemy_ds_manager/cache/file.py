import json
from os import makedirs, path
import uuid
from sqlalchemy_ds_manager.helper.utils import hash

class FileCache:
    def __init__(self, folder: str):
        self.folder = folder
        self.cache = _JsonCache(folder)
    
    def find(self, sql: str):
        token_str = hash(sql)
        found = self.cache.find(token_str)
        if found != None:
            filePath = path.join(self.folder, f'{found.get("id")}.pkl')
            if path.exists(filePath):
                return filePath
        return None
    
    def add(self, sql: str, duration) -> str:
        token_str = hash(sql)
        id = str(uuid.uuid4())
        self.cache.append({
            "hash": token_str,
            "id": id,
            "duration": duration
        })
        return path.join(self.folder, f'{id}.pkl')

class _JsonCache:
    def __init__(self, dir: str, name: str = "map.json"):
        filePath = path.join(dir, name)
        self.filePath = filePath

        if not path.exists(dir):
            makedirs(dir)

        if not path.exists(filePath):
            self.write('[]', 'a+')

        with open(filePath) as f:
            self.data = json.load(f)       
   
    def append(self, item: dict):
        self.data.append(item)
        json_obj = json.dumps(self.data, indent=4)
        self.write(json_obj, 'w+')
        
    def find(self, hash : str):
        return next((i for i in self.data if i.get('hash') == hash), None) 
            
    def write(self, payload, params: str):
        with open(self.filePath, params) as f:
            f.write(payload)
