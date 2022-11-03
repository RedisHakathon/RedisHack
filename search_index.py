import re

from config import INDEX_NAME
from redis.commands.search.query import Query
import redis
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.field import VectorField
from typing import Optional, Pattern


class TokenEscaper:
    # Characters that RediSearch requires us to escape during queries.
    DEFAULT_ESCAPED_CHARS = r"[,.<>{}\[\]\\\"\':;!@#$%^&*()\-+=~\/ ]"

    def __init__(self, escape_chars_re: Optional[Pattern] = None):
        if escape_chars_re:
            self.escaped_chars_re = escape_chars_re
        else:
            self.escaped_chars_re = re.compile(self.DEFAULT_ESCAPED_CHARS)

    def escape(self, value: str) -> str:
        def escape_symbol(match):
            value = match.group(0)
            return f"\\{value}"

        return self.escaped_chars_re.sub(escape_symbol, value)

class SearchIndex:

    escaper = TokenEscaper()

    async def create_hnsw(
        self,
        *fields,
        redis_conn: redis,
        number_of_vectors: int,
        prefix: str,
        distance_metric: str='COSINE'
    ):
        vector_field = VectorField(
            "vector",
            "HNSW", {
                "TYPE": "FLOAT32",
                "DIM": 768,
                "DISTANCE_METRIC": distance_metric,
                "INITIAL_CAP": number_of_vectors,
            }
        )
        await self._create(
            *fields,
            vector_field,
            redis_conn=redis_conn,
            prefix=prefix
        )

    async def _create(
        self,
        *fields,
        redis_conn: redis,
        prefix: str
    ):
        # Create Index
        await redis_conn.ft(INDEX_NAME).create_index(
            fields = fields,
            definition= IndexDefinition(prefix=[prefix], index_type=IndexType.HASH)
        )

    def vector_query(
        self,
        search_type: str="KNN",
        number_of_results: int=5
    ) -> Query:
        base_query = f'*=>[{search_type} {number_of_results} @vector $vec_param AS vector_score]'
        return Query(base_query)\
            .sort_by("vector_score")\
            .paging(0, number_of_results)\
            .return_fields("paper_id", "vector_score")\
            .dialect(2)
