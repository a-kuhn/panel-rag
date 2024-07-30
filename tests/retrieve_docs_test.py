import pytest
from unittest.mock import MagicMock
from elasticsearch import Elasticsearch
from src.retrieve_docs import (
    get_elasticsearch_client,
    construct_search_query,
    retrieve_docs,
)


def test_get_elasticsearch_client():
    client = get_elasticsearch_client("http://testhost:9200")
    assert isinstance(client, Elasticsearch)


@pytest.mark.parametrize(
    "query, max_results, filter, expected",
    [
        (
            "test query",
            5,
            {"status": "active"},
            {
                "size": 5,
                "query": {
                    "bool": {
                        "must": [
                            {
                                "multi_match": {
                                    "query": "test query",
                                    "fields": ["question^4", "text"],
                                    "type": "best_fields",
                                }
                            }
                        ],
                        "filter": [{"term": {"status.keyword": "active"}}],
                    }
                },
            },
        ),
        (
            None,
            10,
            None,
            {
                "size": 10,
                "query": {
                    "bool": {
                        "must": [{"match_all": {}}],
                        "filter": [],
                    }
                },
            },
        ),
    ],
)
def test_construct_search_query(query, max_results, filter, expected):
    assert construct_search_query(query, max_results, filter) == expected


def test_retrieve_docs():
    mock_client = MagicMock()
    mock_response = {
        "hits": {
            "hits": [
                {
                    "_source": {
                        "question": "What is pytest?",
                        "answer": "A testing framework",
                    },
                    "_score": 1.0,
                },
                {
                    "_source": {
                        "question": "What is mock?",
                        "answer": "A testing utility",
                    },
                    "_score": 0.8,
                },
            ]
        }
    }
    mock_client.search.return_value = mock_response

    docs, scores = retrieve_docs(
        query="test query",
        index_name="test_index",
        max_results=5,
        filter={"status": "active"},
        es_client=mock_client,
    )

    expected_docs = [
        {"question": "What is pytest?", "answer": "A testing framework"},
        {"question": "What is mock?", "answer": "A testing utility"},
    ]
    expected_scores = [1.0, 0.8]

    assert docs == expected_docs
    assert scores == expected_scores
    mock_client.search.assert_called_once_with(
        index="test_index",
        body={
            "size": 5,
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": "test query",
                                "fields": ["question^4", "text"],
                                "type": "best_fields",
                            }
                        }
                    ],
                    "filter": [{"term": {"status.keyword": "active"}}],
                }
            },
        },
    )
