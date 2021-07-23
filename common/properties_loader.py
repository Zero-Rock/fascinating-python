import os
import re
import tempfile


class Properties:

    def __init__(self, file_name: str):
        """

        :param file_name:
        """
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

    def has_key(self, key: str) -> bool:
        """

        :param key: attribute key
        :return:
        """
        return key in self.properties

    def get(self, key: str, default_value='') -> str:
        """

        :param key: attribute key
        :param default_value: default value
        :return: attribute value
        """
        if key in self.properties:
            return self.properties[key]
        return default_value

    def put(self, key: str, value: str) -> None:
        """

        :param key:
        :param value:
        :return:
        """
        self.properties[key] = value
        Properties.replace_property(self.file_name, key + '=.*', key + '=' + value, True)

    @staticmethod
    def replace_property(file_name: str, from_regex: str, to_str: str, append_on_not_exists=True) -> None:
        """

        :param file_name:
        :param from_regex:
        :param to_str:
        :param append_on_not_exists:
        :return:
        """
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
