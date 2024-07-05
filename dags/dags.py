from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import os

API_URL = "http://backend:8080"
DATA_ENGINE_URL = "http://data-engine:5000"
MODEL_URL = "http://course-recommendation:5000"
SCHEDULER_URL = "http://airflow-webserver:8080"


def clear_cache():
    base_url = os.getenv("API_URL")
    if not base_url:
        base_url = API_URL
    url = f"{base_url}/api/webhook/clear-course-suggestions"

    response = requests.post(url)
    response.raise_for_status()


def retrain_model():
    base_url = os.getenv("MODEL_URL")
    if not base_url:
        base_url = MODEL_URL
    url = f"{base_url}/recommendation-model/retrain"
    body = {
        "webhook_url": f"{SCHEDULER_URL}/api/v1/dags/clear_courses_in_cache/dagRuns"
    }

    response = requests.post(url, json=body)
    response.raise_for_status()


def preprocess_data():
    base_url = os.getenv("DATA_ENGINE_URL")
    if not base_url:
        base_url = DATA_ENGINE_URL

    url = f"{base_url}/warehouse/process_data"
    body = {"webhook_url": f"{SCHEDULER_URL}/api/v1/dags/retrain_model/dagRuns"}

    response = requests.post(url, json=body)
    response.raise_for_status()


with DAG(
    dag_id="preprocess_data",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
) as dag:
    preprocess_task = PythonOperator(
        task_id="preprocess_data_task",
        python_callable=preprocess_data,
        provide_context=True,
    )

with DAG(
    dag_id="retrain_model",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
) as dag1:
    retrain_task = PythonOperator(
        task_id="retrain_model_task",
        python_callable=retrain_model,
        provide_context=True,
    )

with DAG(
    dag_id="clear_courses_in_cache",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
) as dag2:
    clear_cache_task = PythonOperator(
        task_id="clear_cache_task",
        python_callable=clear_cache,
        provide_context=True,
    )
