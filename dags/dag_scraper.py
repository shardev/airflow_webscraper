import os
import ast
from datetime import datetime, timedelta
from pipeline.scrape import scrape_web_data
from pipeline.utils import create_csv, read_csv_and_build_car_listings, data_cleansing
from ddl_scripts import create_car_listings_table
from pipeline.delta_insert import delta_insert
from constants import URL, EMAIL_TO

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.email import EmailOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule
FILENAME  = f"webdata_testing_{datetime.now().strftime('%Y%m%d')}.csv"
USE_LOCAL_STORAGE = 0


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'car_listings_workflow',
    default_args=default_args,
    description='A workflow to scrape web car listings and insert into database',
    schedule_interval='0 10 * * *',
    start_date=days_ago(1),
    catchup=False,
)

def check_local_storage1(**kwargs):
    if USE_LOCAL_STORAGE == 1 and os.path.exists(os.path.join(os.getcwd(), f'{FILENAME}')):
        return 'read_csv_and_build_car_listings_task'
    else:
        return 'scrape_web_data_task'

def check_local_storage2(**kwargs):
    if USE_LOCAL_STORAGE == 1:
        return 'create_csv_task'
    else:
        return 'data_cleansing_task'

def compose_email_content(new_listings):
    # From string to list of dicts
    new_listings = ast.literal_eval(new_listings)
    
    email_content = """
    <h3>New Car Listings:</h3>
    <table style="border-collapse: collapse; width: 100%;">
        <thead>
            <tr>
                <th style="border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2;">Title</th>
                <th style="border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2;">Price</th>
                <th style="border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2;">Link</th>
            </tr>
        </thead>
        <tbody>
    """

    # Add rows to the table for each listing
    for listing in new_listings:
        email_content += f"""
            <tr>
                <td style="border: 1px solid #ddd; padding: 8px;">{listing['title']}</td>
                <td style="border: 1px solid #ddd; padding: 8px;"><b>{listing['price']} KM</b></td>
                <td style="border: 1px solid #ddd; padding: 8px;"><a href='{listing['link']}'>Link</a></td>
            </tr>
        """

    # Close the table tags
    email_content += """
        </tbody>
    </table>
    """

    return email_content

with dag:
    check_local_storage_task1 = BranchPythonOperator(
        task_id='check_local_storage1',
        python_callable=check_local_storage1,
        provide_context=True,
    )

    check_local_storage_task2 = BranchPythonOperator(
        task_id='check_local_storage2',
        python_callable=check_local_storage2,
        provide_context=True,
    )

    read_csv_and_build_car_listings_task = PythonOperator(
        task_id='read_csv_and_build_car_listings_task',
        python_callable=read_csv_and_build_car_listings,
        op_args=[FILENAME],
    )

    scrape_web_data_task = PythonOperator(
        task_id='scrape_web_data_task',
        python_callable=scrape_web_data,
        op_args=[URL],
        execution_timeout=timedelta(minutes=2),
    )

    create_csv_task = PythonOperator(
        task_id='create_csv_task',
        python_callable=create_csv,
        op_args=["{{ task_instance.xcom_pull(task_ids='scrape_web_data_task') }}", FILENAME],
    )

    data_cleansing_task = PythonOperator(
        task_id='data_cleansing_task',
        provide_context=True,
        python_callable=data_cleansing,
        op_args=["{{ task_instance.xcom_pull(task_ids='read_csv_and_build_car_listings_task', key='return_value') if task_instance.xcom_pull(task_ids='read_csv_and_build_car_listings_task') else task_instance.xcom_pull(task_ids='scrape_web_data_task', key='return_value') }}"],
    
    )

    create_car_listings_table_task = PythonOperator(
        task_id='create_car_listings_table_task',
        python_callable=create_car_listings_table,
    )

    delta_insert_task = PythonOperator(
        task_id='delta_insert_task',
        python_callable=delta_insert,
        provide_context=True,
        op_args=["{{ task_instance.xcom_pull(task_ids='data_cleansing_task') }}"],
    )

    build_email_task = PythonOperator(
        task_id='build_email_task',
        python_callable=compose_email_content,
        op_args=["{{ task_instance.xcom_pull(task_ids='delta_insert_task') }}"],
        provide_context=True
    )

    email_operator_task = EmailOperator(
        task_id='email_operator_task',
        to= EMAIL_TO,
        subject='New Car Listings',
        html_content="{{ task_instance.xcom_pull(task_ids='build_email_task') }}",
    )

    data_cleansing_task.trigger_rule = TriggerRule.ONE_SUCCESS


    check_local_storage_task1 >> [read_csv_and_build_car_listings_task, scrape_web_data_task] 
    read_csv_and_build_car_listings_task >> data_cleansing_task
    
    scrape_web_data_task >> check_local_storage_task2 >> [create_csv_task, data_cleansing_task]
    create_csv_task >> data_cleansing_task
    
    data_cleansing_task >> create_car_listings_table_task >> delta_insert_task >> build_email_task >> email_operator_task
    