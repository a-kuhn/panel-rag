from elasticsearch import Elasticsearch


def retrieve_docs(
    query=None, index_name="faq_elasticsearch_data", max_results=5, filter=None
):
    es = Elasticsearch("http://localhost:9200")

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

    response = es.search(index=index_name, body=search_query)
    documents = [hit["_source"] for hit in response["hits"]["hits"]]
    scores = [hit["_score"] for hit in response["hits"]["hits"]]
    return documents, scores
