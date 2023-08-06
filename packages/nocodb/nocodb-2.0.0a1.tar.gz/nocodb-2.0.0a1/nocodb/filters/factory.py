from ..nocodb import WhereFilter

from .basic_filter import BasicFilter
from .raw_filter import RawTemplateFilter


def basic_filter_class_factory(filter_name: str):
    class WrappedFilter(WhereFilter):
        def __init__(self, column_name: str, value: str):
            self.__filter = BasicFilter(column_name, filter_name, value)
        def get_where(self) -> str:
            return self.__filter.get_where()
    return WrappedFilter

def raw_template_filter_class_factory(template: str):
    class WrappedFilter(WhereFilter):
        def __init__(self, *args, **kwargs):
            self.__filter = RawTemplateFilter(template, *args, **kwargs)
        def get_where(self) -> str:
            return self.__filter.get_where()
    return WrappedFilter

