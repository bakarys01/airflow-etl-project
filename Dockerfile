FROM apache/airflow:2.7.1
RUN pip install Faker pandas sqlalchemy psycopg2-binary