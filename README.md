# Web scraping with Airflow Orchestration

This project involves web scraping car listings from web, processing the data, and storing it in a PostgreSQL database. It's orchestrated using Apache Airflow for task scheduling and email notifications for new listings.

### Project Components
- Web Scraping: Scrapes car listings from web using selenium.
   
- Data Processing: Cleanses and processes the scraped data using Python scripts.
  
- Database: Stores the processed data in a PostgreSQL database using SQLAlchemy for ORM operations.
  
- Apache Airflow: Orchestrates the data scraping and processing tasks using Airflow's Directed Acyclic Graphs (DAGs).
  
- Email Notifications: Notifies users of new car listings via email using Airflow's EmailOperator.


### Required Pip Installs
To set up and run the project, you'll need to install the following Python packages:

- **selenium**: For scraping dynamic web pages.

- **SQLAlchemy**: For ORM operations with the PostgreSQL database.

- **psycopg2**: PostgreSQL adapter for Python.

- **apache-airflow**: For task orchestration and scheduling.

- **smtplib**: For sending emails.

- **jinja2**: Templating engine used by Airflow.

