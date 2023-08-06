
class BasicFilter:
    def __init__(self, column_name: str, filter_name: str, value: str):
        self.__column_name = column_name
        self.__value = value
        self.__filter_name = filter_name

    def get_where(self) -> str:
        return f"({self.__column_name},{self.__filter_name},{self.__value})"
