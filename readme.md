### The below content is not gpt generated it is an own content ###
# Overview of Solution 

Our solution is an LLM-powered Intelligent Query–Retrieval System designed to answer complex, domain-specific questions instantly by retrieving and interpreting relevant clauses from multi-format documents.

# It Contains: 

Semantic Search (FAISS + HuggingFace BGE embeddings) for accurate clause retrieval.

Gemini API for context understanding, reasoning, and generating structured JSON answers.

OCR for extracting text from images and scanned documents.

Custom domain logic for specialized queries (Insurance, Legal, HR).

his enables businesses to reduce manual search time, improve customer response speed, and ensure accuracy in decision-making.

# Breakdown of each files present in this repo:

main.py -- it contains FastAPI and access tocken verification with redirecting of process respective modules

cache_manager.py -- it will store the new file as FAISS DB  to reuse the same file without preprocessing again (now implemnt via url hash match)

embedder.py -- here we choose cpu or gpu if available and doing embidding process with huggingface BAAI/bge-base-en model and chunking

llm_reasoner.py -- here the gemini api call with specified prompt with batchprocessing of question to efficiently use a tocken

models.py -- here define the basemodel structure

processor.py -- here we implement to handling different types of file and get the text data as well as image to text by pyteseract module to process that content

retriever.py -- here the semantic search for chunk which match the question by similarity search method which comes under cosine search 

special_handlers.py -- this is handle a special question in hackthon to follow some steps like ping the url and get the data etc..

## Running with Docker (Method 1: Build and run Docker image locally)

1. Build the Docker image (run this from the project root):

   ```bash
   docker build -t hackathon_app .
   ```
### Create a .env file in the project root with your API key:

```bash
GOOGLE_API_KEY=your_api_key_here
```
[get our api here for testing](https://jumpshare.com/s/b5evX9uLEMaaUrkJAUH5)


### Run the Docker container, exposing port 8000 and passing the environment variables:

```bash
docker run -d -p 8000:8000 --env-file .env --name hackathon_container hackathon_app
```

### Access the API : we will add cloudflare tunnelling inside the docker so you got public api endpoint



# Installation Process (Method-2 without docker )

## step 1 clone the git repo
Run the following commands:

```bash
git clone https://github.com/ANAND060218/HackRX_cookies.git
cd HackRX_cookies
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
## step 2 create .env file in root directory with below content 

GOOGLE_API_KEY= xxxx [get our api here for testing](https://jumpshare.com/s/b5evX9uLEMaaUrkJAUH5)

## Install one package before run the code which is pyteseract use for convert imgage to text 
click the below link to download teseract.exe file on Window 

[Download Tesseract OCR (Windows)](https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe)

then setup usual process next->next->next->finish

## run the code 
``` bash
uvicorn main:app --reload
```
## test the api endpoint as 
    http://localhost:8000/api/v1/hackrx/run
