import typing as t
import asyncio
import numpy as np
import pickle
import redis.asyncio as redis
from redis.commands.search.field import TagField
from redis.commands.search.field import VectorField
import config
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from search_index import SearchIndex

def read_paper_df() -> t.List:
    with open("arxiv_embeddings_10000.pkl", "rb") as f:
        df = pickle.load(f)
    return df

async def load_vectors(n, redis_conn, *papers):
    semaphore = asyncio.Semaphore(n)
    async def load_paper(paper: dict):
        async with semaphore:
            # Prep the input dictionary for Redis storage
            key = "paper_vector:" + paper['id']
            paper['paper_id'] = paper.pop('id')
            paper['vector'] = np.array(paper['vector'], dtype=np.float32).tobytes()
            paper['categories'] = paper['categories'].replace(",", "|")
            # Store in Redis
            await redis_conn.hset(key, mapping=paper)
    # Gather results with concurrency
    await asyncio.gather(*[load_paper(p) for p in papers])

async def load_all_data():
    redis_conn = redis.from_url(config.REDIS_URL)
    if await redis_conn.dbsize() > 500:
        print("Papers already loaded")
    else:
        print("Loading papers into Redis")
        papers = read_paper_df()
        papers = papers.to_dict('records')

        await load_vectors(200, redis_conn, *papers)
        print("Papers loaded!")

        print("Creating vector search index")
        categories_field = TagField("categories", separator = "|")
        year_field = TagField("year", separator = "|")
        # create a search index
        vector_field = VectorField(
        "vector",
        "HNSW", {
            "TYPE": "FLOAT32",
            "DIM": 768,
            "DISTANCE_METRIC": "IP",
            "INITIAL_CAP": len(papers),
        })
        
        await redis_conn.ft(config.INDEX_NAME).create_index(
            fields = [year_field, categories_field, vector_field],
            definition= IndexDefinition(prefix=["paper_vector:"],
                                        index_type=IndexType.HASH)
        )

        print("Search index created")


if __name__ == "__main__":
    asyncio.run(load_all_data())