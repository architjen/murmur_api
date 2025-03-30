![CI](https://github.com/architjen/murmur_api/actions/workflows/code_quality_ci.yml/badge.svg)

# ASR Project using Faster-Whisper and FastAPI

The goal of this project is to provide a fast and efficient ASR service through a web API that can transcribe audio files into text.

The project uses `faster-whisper` model, `FastAPI` for hosting APIs, and `uv` for dependency management and virtual environment handling.  

## Main Features

- **Faster-Whisper Model**: Utilizes the condensed Whisper model by OpenAI, optimized for fast transcription and accuracy.
- **FastAPI Backend**: A high-performance web framework for building APIs (supports inbuilt async and type-checking)
- **Dependency Management with uv**: Simplifies managing dependencies and virtual environments.
- **Docker**: Docker image to quickly reproduce the project, without having to worry about the dependencies

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.12 or higher
- `uv` for managing dependencies
- Docker (optional, but recommended for setting up the environment quickly)
- minikube, 

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

You can deploy this application to various platforms such as AWS, Heroku, or DigitalOcean. If using Docker, you can build a Docker image and push it to Docker Hub or other container registries.

### Deploying to Kubernetes cluster

Make sure to set up the environment variables on Heroku (using the Heroku Dashboard or CLI) for things like `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB`.



## Contributing
