import os
import re
import tempfile


class Properties:

    def __init__(self, file_name):
        if not os.path.exists(file_name):
            raise ReferenceError('file "{}" not exit'.format(file_name))
        self.file_name = file_name
        self.properties = {}
        with open(self.file_name, 'r', encoding="utf8") as f:
            for line in f:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    temp_str = line.split('=')
                    self.properties[temp_str[0].strip()] = temp_str[1].strip()

    def has_key(self, key) -> bool:
        return key in self.properties

    def get(self, key, default_value='') -> str:
        if key in self.properties:
            return self.properties[key]
        return default_value

    def put(self, key, value):
        self.properties[key] = value
        Properties.replace_property(self.file_name, key + '=.*', key + '=' + value, True)

    @staticmethod
    def replace_property(file_name, from_regex, to_str, append_on_not_exists=True):
        if not os.path.exists(file_name):
            raise ReferenceError('file "{}" not exit'.format(file_name))
        temp_file = tempfile.TemporaryFile()
        pattern = re.compile(r'' + from_regex)
        found = None
        with open(file_name, 'r', encoding="utf8") as f:
            for line in f:
                if pattern.search(line) and not line.strip().startswith('#'):
                    found = True
                    line = re.sub(from_regex, to_str, line)
                b = bytes(line, encoding="utf8")
                temp_file.write(b)
            if not found and append_on_not_exists:
                b_str = bytes("\n" + to_str, encoding="utf8")
                temp_file.write(b_str)
            temp_file.seek(0)
            content = temp_file.read()
            with open(file_name, 'wb+') as w:
                w.write(content)
            temp_file.close()


if __name__ == "__main__":
    file_path = '../util_test/test.properties'
    props = Properties(file_path)
    print(props.get('user'))
    props.put('key_a', 'value_a')
