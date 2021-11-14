class MyIniFile:
    def __init__(self, file_name):
        with open(file_name, "r") as file:
            self._entries = self._process_file_lines(file.readlines())

    def _process_file_lines(self, file_lines):
        result = {}
        for line in file_lines:
            a_pair = line.split('=', 1)
            if len(a_pair) == 2:
                key = a_pair[0].strip("\n\r\t ")
                value = a_pair[1].strip("\n\r\t ")
                if len(key) > 0 and len(value) > 0:
                    result[key] = value
        return result

    def get(self, entry_name):
        if entry_name in self._entries:
            return self._entries[entry_name]
        else:
            return ''
