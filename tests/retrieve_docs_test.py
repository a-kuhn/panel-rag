import unittest
from unittest.mock import patch, Mock
from elasticsearch import Elasticsearch
from src.retrieve_docs import (
    retrieve_docs,
    construct_search_query,
    get_elasticsearch_client,
)


class TestRetrieveDocs(unittest.TestCase):

    @patch("src.retrieve_docs.get_elasticsearch_client")
    def test_retrieve_docs(self, mock_get_client):
        mock_es = Mock()
        mock_get_client.return_value = mock_es

        mock_response = {
            "hits": {
                "hits": [
                    {
                        "_source": {
                            "question": "How to refund?",
                            "text": "Refund details",
                        },
                        "_score": 1.0,
                    },
                    {
                        "_source": {
                            "question": "How to reset password?",
                            "text": "Reset password details",
                        },
                        "_score": 0.9,
                    },
                ]
            }
        }
        mock_es.search.return_value = mock_response

        documents, scores = retrieve_docs(query="refund", es_client=mock_es)

        expected_documents = [
            {"question": "How to refund?", "text": "Refund details"},
            {"question": "How to reset password?", "text": "Reset password details"},
        ]
        expected_scores = [1.0, 0.9]

        self.assertEqual(documents, expected_documents)
        self.assertEqual(scores, expected_scores)

    def test_construct_search_query_with_query(self):
        query = "refund"
        max_results = 5
        filter = {"section": "Payments"}

        expected_query = {
            "size": max_results,
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": query,
                                "fields": ["question^4", "text"],
                                "type": "best_fields",
                            }
                        }
                    ],
                    "filter": [{"term": {"section.keyword": "Payments"}}],
                }
            },
        }

        self.assertEqual(
            construct_search_query(query, max_results, filter), expected_query
        )

    def test_construct_search_query_without_query(self):
        query = None
        max_results = 5
        filter = {"section": "Payments"}

        expected_query = {
            "size": max_results,
            "query": {
                "bool": {
                    "must": [{"match_all": {}}],
                    "filter": [{"term": {"section.keyword": "Payments"}}],
                }
            },
        }

        self.assertEqual(
            construct_search_query(query, max_results, filter), expected_query
        )

    @patch("src.retrieve_docs.Elasticsearch")
    def test_get_elasticsearch_client(self, mock_es):
        client = get_elasticsearch_client("http://example.com")
        mock_es.assert_called_with("http://example.com")
        self.assertEqual(client, mock_es.return_value)


if __name__ == "__main__":
    unittest.main()
