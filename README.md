# panel-rag

## Overview

`panel-rag` is a Python-based project designed to facilitate the retrieval and augmentation of documents using Elasticsearch. The project includes various scripts and modules to handle document retrieval, prompt augmentation, and response generation.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/panel-rag.git
    cd panel-rag
    ```

2. Install dependencies using Pipenv:
    ```sh
    pipenv install
    ```

3. Activate the virtual environment:
    ```sh
    pipenv shell
    ```
    (can also use requirements.txt to create venv)

## Usage

### Running the Application

To run the main application, execute the following command:
```sh
panel serve src/app.py [--autoreload]
```
_see Docker setup below for - ElasticSearch is required, ollama setup is optional_  
_OpenAI API Key is required if using OpenAIResponseGenerator_  
  
### Running Tests
To run the tests, use:
```sh
pytest
```

### Docker Setup
To set up and run Elasticsearch using Docker, navigate to the mlops directory and run:
_must have the FAQ docs indexed & saved as a volume first_
```sh
bash run_elastic_search_w_volume.sh
```

## Project Modules
`src/app.py`: Main application entry point  
`src/retrieve_docs.py`: Module for retrieving relevant documents from ElasticSearch  
`src/augment_prompt.py`: Module for contextualizing prompts w relevant FAQs  
`src/generate_response.py`: Module for generating responses (OpenAI or Ollama)    
  
## Documentation
The project documentation, including class diagrams and system context, can be found in the docs directory.

