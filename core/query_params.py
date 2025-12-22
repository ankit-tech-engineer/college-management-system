from typing import Optional
from fastapi import Query
import json

class QueryParams:
    def __init__(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        sort: Optional[str] = Query(None),
        filter: Optional[str] = Query(None),
        search: Optional[str] = Query(None),
        select: Optional[str] = Query(None),
        no_limit: bool = Query(False)
    ):
        self.skip = skip
        self.limit = None if no_limit else limit
        self.sort = sort
        self.filter = filter
        self.search = search
        self.select = select
        self.no_limit = no_limit
    
    def parse_filter(self):
        return json.loads(self.filter) if self.filter else {}
    
    def parse_search(self):
        if self.search:
            search_terms = self.search.split(":")
            if len(search_terms) == 2:
                return {search_terms[0]: {"$regex": search_terms[1], "$options": "i"}}
        return None
    
    def parse_select(self):
        if self.select:
            fields = self.select.split(",")
            return {field.strip(): 1 for field in fields}
        return None
    
    def parse_sort(self):
        if self.sort:
            sort_list = []
            for item in self.sort.split(","):
                parts = item.split(":")
                if len(parts) == 2:
                    field, order = parts
                    sort_list.append((field.strip(), 1 if order.strip() == "asc" else -1))
            return sort_list if sort_list else None
        return [("id", 1)]
