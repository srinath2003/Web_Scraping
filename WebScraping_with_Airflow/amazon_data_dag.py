from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import subprocess

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 4,
    'retry_delay': timedelta(minutes=1),
}

# Define the DAG
with DAG(
    'amazon_data_collector',
    default_args=default_args,
    description='A DAG to scrape Amazon data every 5 minutes and save as separate CSV files',
    schedule_interval=timedelta(minutes=5),
    start_date=datetime(2024, 11, 22),
    catchup=False,
) as dag:

    def run_scraper():
        # Run the web scraping script using subprocess
        subprocess.run(["python3", "/home/srinath2003/Desktop/airflow_mini_project/amazon_scraper.py", "laptop"], check=True)

    scrape_amazon_task = PythonOperator(
        task_id='scrape_amazon_data',
        python_callable=run_scraper,
    )

    scrape_amazon_task
