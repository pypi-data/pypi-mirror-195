import json
import toml


class Fopen:
    def __init__(
        self,
        path,
        delimiter:str=',',
        enc:str='utf-8'
    ):
        self.path = path
        self.delimiter = delimiter
        self.enc = enc

    @property
    def file_format(self) -> str:
        return self.path.rsplit('.', 1)[1]

    @property
    def content(self) -> str:
        f = self._open_file_r()
        content = f.read()
        f.close()
        return content
    
    def to_json_array(self):
        f = self._open_file_r()
        arr = json.dumps([json.loads(line.strip()) for line in f.readlines()])
        f.close()
        return arr
    
    def load(self):
        ftype = self.file_format
        if ftype == 'json': 
            return self._parse_json()
        elif ftype == 'csv': 
            return [line for line in self._csv_read_lines()]
        elif ftype in ['jsonl', 'jl']: 
            return [line for line in self._jsonlines_read_lines()]
        elif ftype == 'toml': 
            return self._parse_toml()
        else:
            return self.content

    def load_lines(self):
        ftype = self.file_format
        if  ftype == 'csv':
            return self._csv_read_lines()
        elif ftype in ['jsonl', 'jl']:
            return self._jsonlines_read_lines()
        else:
            return self._default_read_lines()

    def _jsonlines_read_lines(self):
        f = self._open_file_r()
        for line in f.readlines():
            yield json.loads(line)
        f.close()

    def _csv_read_lines(self):
        f = self._open_file_r()
        for line in f.readlines():
            stripped = line.strip()
            if len(stripped) == 0: continue
            yield stripped.split(self.delimiter)
        f.close()

    def _default_read_lines(self):
        f = self._open_file_r()
        for line in f.readlines():
            stripped = line.strip()
            yield stripped
        f.close()
        
    def _parse_json(self):
        f = self._open_file_r()
        parsed = json.load(f)
        f.close()
        return parsed

    def _parse_toml(self):
        f = self._open_file_r()
        parsed = toml.load(f)
        f.close()
        return parsed
        
    def _open_file_r(self):
        f = open(self.path, 'r', encoding=self.enc)
        return f
