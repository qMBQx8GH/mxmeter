class MyIniFile:
    def __init__(self, fileName):
        with open(fileName, "r") as file:
            self._entries = file.readlines()

    def get(self, entryName):
        search = entryName + '='
        for line in self._entries:
            if line.startswith(search):
                return line[len(search):].rstrip("\n\r\t ")
        return ''
