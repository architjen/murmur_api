# ASR Project using Faster-Whisper and FastAPI
![CI](https://github.com/architjen/murmur_api/actions/workflows/code_quality_ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)  
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)


The goal of this project is to provide a fast and efficient ASR service through a web API that can transcribe audio files into text.

The project uses `faster-whisper` model, `FastAPI` for hosting APIs, and `uv` for dependency management and virtual environment handling.  

## Technologies

- **Faster-Whisper Model**: Utilizes the condensed Whisper model by OpenAI, optimized for fast transcription and accuracy.
- **FastAPI Backend**: A high-performance web framework for building APIs (supports inbuilt async and type-checking)
- **Dependency Management with uv**: Simplifies managing dependencies and virtual environments.
- **Docker**: Docker image to quickly reproduce the project, without having to worry about the dependencies

## Features 🚀
- ✅ Whisper Model
- ✅ FastAPI integration 
- ✅ Metrics on database
- ✅ Postgres Database (Persistent)
- ✅ Dockerized
- ✅ Unit test coverage
- ✅ CI Workflows

### Extra Feature 
- ✅ Queue Implementation (branch: adding_queue) 
- ✅ local deployment


## Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.12 or higher
- `uv` for managing dependencies
- Docker (optional, but recommended for setting up the environment quickly)
- `minikube` and `kompose`

### Install Dependencies

You can install the project dependencies using `uv`. To do so, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/architjen/murmur_api.git
   cd murmur_api
   ```

2. Set up the environment using `uv`:

   ```bash
   uv install
   ```
   OR
   ```bash
   uv sync
   ```



   This will install the dependencies specified in `pyproject.toml` and `uv.lock`.

3. Activate the virtual environment (if using `uv`):

   ```bash
   uv venv
   ```
   OR
    ```bash
   source .venv/bin/activate #unix/macOS
   ```

### Running FastAPI locally

If you prefer to run the app locally, you could:
```bash
   uv run fastapi run api/main.py
   ```
NOTE: Although this would get the FastAPI up and running, you wont be able to perform any CRUD operations on the endpoints, as they all are linked to postgres db. 

If you'd still want to run locally, make sure you have a postgres instance running, with a database and [table_schema](/app/db/create_table.sql)

### Set Up Docker (Recommended)

The simpler way would be using the `docker-compose.yml` to spin up the containers and access the application at `localhost`. This will handle both the FastAPI, postgres creation, default table construction, setting up the env for you or any necessary background services.  

**NOTE**: Please save your postgres string connectinos in the `.env` file at the root level of the project before running instances. 

1. Build and start the services:

    ```bash
    docker compose up -d 
    ```

2. This will set up a FastAPI application accessible at `http://localhost:8000`.

If you're using VSCode, you may download the docker extention as well, makes it lot easier to connect to each instance from the IDE terminal, looking at logs, etc and avoiding typing in docker cli commands.

### Environment Variables

As we looked earlier, your `.env` file should be in the root of the project to define necessary environment variables such as database credentials or API keys.  
An example `.env` file might look like this:

```bash
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_database_name
```

## Usage

Once the app is running, you can interact with the ASR API using `POST` requests to transcribe audio files.

### Example Requests

**1. Transcribe Audio File**

To send an audio file for transcription, use the `/transcribe/` endpoint:

```bash
curl -X 'POST' \
  'http://localhost:8000/transcribe/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@path_to_your_audio_file.wav'
```

**Response Example**

The API will return a JSON response with the transcribed text:

```json
{
  "text": "This is the transcribed text of the audio file."
}
```

**2. Getting Metrics**

To get the metrics (**median_latency**, **number of calls**, **median_audio_duration**) of our system, use the `/metrics/` endpoint:

```bash
curl -X 'GET' \
  'http://localhost:8000/metrics/' \
  -H 'accept: application/json' 
```
**Response Example**

The API will return a JSON response with the metrics data:

```json
{
  "median_latency": 2.342629551887512,
  "median_audio_length": 11.598374999999999,
  "total_no_of_calls": 24
}
```

At the same time we have API documentation as well for interactive use

### API Documentation

FastAPI provides auto-generated documentation for the API. You can view the interactive API docs by navigating to:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc UI: `http://localhost:8000/redoc`

### Available Endpoints

- **`POST /transcribe/`**: Transcribe an audio file.
  - **Request**: A `.wav`, `.mp3`, or `.mpeg` audio file.
  - **Response**: The transcribed text.

- **`GET /get_data/`**: To get all the transcription data
  - **Response**: list of all the transcriptions

- **`GET /metrics/`**: To get the metrics on overall transcription 
  - **Response**: a dictionary of important KPIs

## Development

### Format/Linting

To make sure that the code is readable, well formatted, avoiding unnecessary imports, etc and follows strict PEP standards. Ruff is used here to perform code checks, make sure to download it before using. 

Run following commands before any push to repo

```bash
uvx ruff check # checks the code
```

```bash
uvx ruff format # formats the code based on criteria
```

NOTE: If you dont perform either of the check and still push the code to the repo, the CI workflow will fail and notify you.

### Running Tests

All the unit tests are added in the `.py` in `tests` folder, if you dont follow the same structure make sure to reflect the changes accordingly in `pyproject.toml`

```
[tool.pytest.ini_options]
testpaths = ["tests/"]
```

To run the tests for the project, use the following command:

```bash
uv run -m pytest 
```

Make sure you have all the dependencies installed, and the `.env` file is configured correctly before running the tests.

## Deployment

### Deploying to Kubernetes cluster

To deploy on the Kubernetes cluster we are going to use `minikube` and `kompose` 

**minikube**: helps run cluster locally  
**kompose**: helps you build `.yml` files from `docker-compose.yml` for kubernetes deployment

#### Steps to deploy: 
1. To run k8s locally  

```bash
minikube start
```

2. Create the .ymls files for deployment  

```bash
kompose convert -f docker-compose.yml --out manifests/
```
This will create the `.yml` manifests for deployment in the folder `manifests`

3. Deploy to minikube

```bash
kubectl apply -f manifests/.
```

4. Check pods
Check the pods running using the command below

```bash
kubectl get pods
```

5. Get IP
Get the IP to access the API app
```bash
minikube ip
```

6. Access the app

Check the running app by going to the browser and typing the IP from the command above with port we expose example `http://10.96.184.178:8000` and you should see your app 

## Improvements and Optimization

Few improvements that could be made to the overall project for better performance:

### Processesing Audio
- downsample the audio rates, for ex to 16kHz, could be achieved by using librosa
- applying VAD to reduce the processing time on audio 
- Use protocol buffers between endpoint and functions to optimise serializing and deserializing

### API
- Authentication on endpoints
- Adding cProfile on the endpoints to find bottlenecks
- perform load testing on the APIs
- Adding functional tests
- Setting up middleware-logging  

### Database
- Setting up triggers to calculate metrics, instead of running them every time.
- Avoid the use SQL request for CRUD operations
- Avoid pushing the same audio file twice in the database 
- Use of asynpg + postgres to extend the FastAPI async capabilities

### Operations
- Setting up centralised logging to monitor peformance, state, and actions
- Adding CI for docker pubish on major-release  

