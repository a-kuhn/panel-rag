from typing import List, Tuple, Dict, Optional
from elasticsearch import Elasticsearch


def get_elasticsearch_client(host: str = "http://localhost:9200") -> Elasticsearch:
    return Elasticsearch(host)


def construct_search_query(
    query: Optional[str], max_results: int, filter: Optional[Dict[str, str]]
) -> Dict:
    search_query = {"size": max_results, "query": {"bool": {"must": [], "filter": []}}}

    if query:
        search_query["query"]["bool"]["must"].append(
            {
                "multi_match": {
                    "query": query,
                    "fields": ["question^4", "text"],
                    "type": "best_fields",
                }
            }
        )
    else:
        search_query["query"]["bool"]["must"].append({"match_all": {}})

    if filter:
        for key, value in filter.items():
            search_query["query"]["bool"]["filter"].append(
                {"term": {f"{key}.keyword": value}}
            )

    return search_query


def retrieve_docs(
    query: Optional[str] = None,
    index_name: str = "faq_elasticsearch_data",
    max_results: int = 5,
    filter: Optional[Dict[str, str]] = None,
    es_client: Optional[Elasticsearch] = None,
) -> Tuple[List[Dict], List[float]]:
    es = es_client or get_elasticsearch_client()

    search_query = construct_search_query(query, max_results, filter)
    response = es.search(index=index_name, body=search_query)

    documents = [hit["_source"] for hit in response["hits"]["hits"]]
    scores = [hit["_score"] for hit in response["hits"]["hits"]]

    return documents, scores
