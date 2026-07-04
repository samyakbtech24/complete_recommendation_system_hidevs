# Recommendation System Capstone Project

This project implements a complete recommendation system containing a hybrid recommendation engine, a SQLite database backend with SQLAlchemy models, in-memory caching, API key authentication, request tracing, and an interactive web dashboard.

## Project Structure

* **data/**
  * `database.py`: Establishes the SQLite database connection.
  * `models.py`: Defines the SQLAlchemy database schemas (User, Content, Skill, UserSkill, ContentSkill, Interaction).
  * `repositories.py`: Contains the data access layer for all database operations.
* **engine/**
  * `orchestrator.py`: Implements the RecommendationOrchestrator class to bridge database entities with the engine.
  * `candidate_gen.py`: Audited candidate generation algorithm (collaborative, content-based, popularity, and hybrid).
  * `similarity.py`: Audited similarity calculators (cosine similarity, Jaccard similarity, and Pearson correlation).
  * `scorer.py`: Audited weighted scoring, feature normalization, and candidate ranking.
  * `evaluator.py`: Audited recommendation evaluator calculating Precision@K, Recall@K, and NDCG@K.
  * `sample_data.py`: Auto-generated or runtime data mappings used by candidate_gen.
* **api/**
  * `app.py`: Flask application exposing recommendation, feedback, health check, and metrics endpoints.
  * **templates/**
    * `index.html`: Interactive web dashboard for real-time visualization and testing.
* **scripts/**
  * `seed_data.py`: Database initialization script to seed sample data.
  * `evaluate.py`: Runs offline model evaluations and generates reports.
* **tests/**
  * `test_engine.py`: Unit tests for engine components and orchestrator logic.
  * `test_api.py`: Integration tests for API routes, validation, and security middleware.
* `Dockerfile`: Container configuration for production deployment.
* `requirements.txt`: Python package dependencies.
* `evaluation_report.md`: Summary of evaluation metrics.

## Installation and Setup

### 1. Install Dependencies
Install all required packages listed in the requirements file:
```bash
pip install -r requirements.txt
```

### 2. Initialize and Seed the Database
Generate the SQLite database structure and populate it with sample users, contents, skills, and interactions:
```bash
python scripts/seed_data.py
```

### 3. Run the Application
Start the Flask web server:
```bash
python api/app.py
```
After starting, navigate to `http://127.0.0.1:5000` in a web browser to access the dashboard.

## Verification and Testing

### Run the Test Suite
Execute unit and integration tests using Python's built-in test discovery tool:
```bash
python -m unittest discover -s tests -p "test_*.py"
```

### Run Model Evaluation
Compute offline recommendation quality metrics (Precision@5, Recall@5, NDCG@5) and output the results:
```bash
python scripts/evaluate.py
```

## API Specification

All protected REST API endpoints require authentication via the `X-API-Key` HTTP header or the `api_key` query parameter. The configured key is `capstone-key`.

### 1. Recommendations Request
* **Endpoint**: `GET /recommend/<user_id>`
* **Parameters**: `limit` (optional integer, defaults to 5)
* **Example**:
  ```bash
  curl -H "X-API-Key: capstone-key" "http://127.0.0.1:5000/recommend/1?limit=3"
  ```

### 2. Record User Feedback
* **Endpoint**: `POST /feedback`
* **Content-Type**: `application/json`
* **Example**:
  ```bash
  curl -X POST -H "Content-Type: application/json" -H "X-API-Key: capstone-key" \
    -d '{"user_id": 1, "content_id": 4, "type": "rating", "rating": 5.0}' \
    http://127.0.0.1:5000/feedback
  ```

### 3. Service Health Check
* **Endpoint**: `GET /health`
* **Example**:
  ```bash
  curl http://127.0.0.1:5000/health
  ```

### 4. Performance Metrics
* **Endpoint**: `GET /metrics`
* **Example**:
  ```bash
  curl http://127.0.0.1:5000/metrics
  ```

## Docker Deployment

Build and run the application inside a lightweight container:

### Build Docker Image
```bash
docker build -t recommendation-api .
```

### Start Docker Container
```bash
docker run -d -p 5000:5000 recommendation-api
```
