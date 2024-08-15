#

from enum       import Enum
from fastapi    import Request
from sqlalchemy import select

from utils import generic_exceptions as GenException


class FilterOperation(Enum):
    EQ      = 1
    IS_NULL = 2
    IN      = 3
    NOT_IN  = 4
    GT      = 5
    GTE     = 6
    LT      = 7
    LTE     = 8

    @staticmethod
    def from_str(str_val: str):
        lower_case = str_val.lower()
        match lower_case:
            case "is_null":
                return FilterOperation.IS_NULL
            case "in":
                return FilterOperation.IN
            case "not_in":
                return FilterOperation.NOT_IN
            case "gt":
                return FilterOperation.GT
            case "gte":
                return FilterOperation.GTE
            case "lt":
                return FilterOperation.LT
            case "lte":
                return FilterOperation.LTE
            case _:
                return FilterOperation.EQ


class FilterInfo(object):
    field: str
    operation: FilterOperation
    value: any

    def __init__(self, field, operation, value):
        self.field     = field
        self.operation = operation
        self.value     = value

    def __str__(self) -> str:
        return f"field: {self.field}; operation: {self.operation}; value: {self.value}"


class OrderDirection(Enum):
    ASC  = 1
    DESC = 2

    @staticmethod
    def from_str(str_val: str):
        lower_case = str_val.lower()
        match lower_case:
            case "asc":
                return OrderDirection.ASC
            case "desc" | "dsc":
                return OrderDirection.DESC
            case _:
                return OrderDirection.ASC


class OrderInfo(object):
    field: str
    direction: OrderDirection

    def __init__(self, field, direction):
        self.field     = field
        self.direction = direction

    def __str__(self) -> str:
        return f"field: {self.field}; dir: {self.direction}"


class QueryInfo(object):
    search: str | None = None
    filters: list[FilterInfo] = []
    order: OrderInfo | None = None
    limit: int | None = None
    offset: int | None = None

    def __init__(self, filters = [], search = None, order = None, limit = None, offset = None):
        self.search  = search
        self.filters = filters
        self.order   = order
        self.limit   = limit
        self.offset  = offset

    def __str__(self) -> str:
        return f"\n search: {self.search}\n filters: {[str(f) for f in self.filters]}\n order: {self.order}\n limit: {self.limit}\n offset: {self.offset}"


#
def parse_query_params(request: Request):
    query_info = QueryInfo(filters = [])
    if len(request.query_params.items()) == 0:
        return None

    for key, val in request.query_params.items():
        if key == "search":
            query_info.search = val
        elif key == "order":
            fld_dir = val.split("__")
            if len(fld_dir) == 1:
                query_info.order = OrderInfo(field = fld_dir[0], direction = OrderDirection.ASC)
            elif len(fld_dir) == 2:
                order_dir = OrderDirection.from_str(fld_dir[1])
                query_info.order = OrderInfo(field = fld_dir[0], direction = order_dir)
            else:
                raise GenException.FieldErrorException
        elif key == "limit":
            query_info.limit = val
        elif key == "offset":
            query_info.offset = val
        else:
            fld_op = key.split("__")
            if len(fld_op) == 1:
                filter = FilterInfo(field = fld_op[0], operation = FilterOperation.EQ, value = val)
            elif len(fld_op) >= 2:
                fld_operation = FilterOperation.from_str(fld_op[1])
                fld_val = val
                if fld_operation in [FilterOperation.IN, FilterOperation.NOT_IN]:
                    fld_val = val.split(",")
                elif fld_operation == FilterOperation.IS_NULL:
                    if fld_val.lower() == "true":
                        fld_val = True
                    elif fld_val.lower() == "false":
                        fld_val = False
                    else:
                        raise GenException.FieldErrorException
                filter = FilterInfo(field = fld_op[0], operation = fld_operation, value = fld_val)
            query_info.filters.append(filter)

    return query_info
