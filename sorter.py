import yaml
from pathlib import Path

class FileSorter:
    def __init__(self, rules):
        self.rules = rules

    def get_path(self, filename):
        ext = Path(filename).suffix.lower()
        result = self.rules.get(ext)
        
        if result is None:
            return []

        if isinstance(result, str):
            return [result]
            
        return result

def config_init(config_path='config.yaml'):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}

def config_parsing():
    config = config_init()

    path = {}
    ext_section = config.get('extensions', {})
    ext_folder = config.get('folders', {})
    sources = config.get('source', [])

    if ext_section and ext_folder:
        for category, ext_list in ext_section.items():
            target_path = ext_folder.get(category)
            if target_path:
                for ext in ext_list:
                    path[ext.lower()] = target_path
    
    return path, sources

if __name__ == "__main__":
    config_parsing()