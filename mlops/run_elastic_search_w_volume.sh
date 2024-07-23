docker run -it --rm --name elasticsearch \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    -v faq_elasticsearch_data:/usr/share/elasticsearch/data \
    docker.elastic.co/elasticsearch/elasticsearch:8.4.3
