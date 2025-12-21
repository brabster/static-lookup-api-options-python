import json
import sys
from json import scanner
from json.decoder import scanstring

# inspired by https://gist.github.com/oberstet/fa8b8e04b8d532912bd616d9db65101a
class InterningJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override the default string parser
        self.parse_string = self._intern_string
        self.scan_once = scanner.py_make_scanner(self)

    def _intern_string(self, string, idx, strict):
        # Use the standard library's pure-Python scanner to get the string
        s, end = scanstring(string, idx, strict)
        # Intern the string before returning
        return sys.intern(s), end