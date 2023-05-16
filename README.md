# Congressional Member ETL

This project is the backend component of a visualization web app that utilizes an ETL (Extract, Transform, Load) pipeline to gather congressional member information and voting data. The backend is implemented using Python, Postgres, and an existing public API.

## Features

- Extracts congressional member information and voting data from a public API.
- Transforms and cleans the data to ensure consistency and accuracy. Transformations utilize a mixture of Python and SQL.
- Loads the processed data into a Postgres database for easy querying and analysis. Inserts and table creation scripts handled with a mixture of Python's SQLAlchemy and Psycopg2 modules and SQL scripts.

## Requirements

- Python 3.7 or higher
- Postgres database
- Internet connectivity to access the public API

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Clavvv/Congress-Data-Project.git
```

## Configuration

The database connection details are stored in a `.ini` file named `database.ini`. Follow the steps below to set up the database configuration:

1. Create a new file named `database.ini` in the project directory.
2. Open `database.ini` in a text editor and enter the following configuration:

```ini
[postgresql]
host=<DATABASE_HOST>
port=<DATABASE_PORT>
database=<DATABASE_NAME>
user=<DATABASE_USER>
password=<DATABASE_PASSWORD>
```

## Automation

The `daily_update.py` script is scheduled to run everyday after that day's session has ended via Windows Task Scheduler.

### Scheduling with Windows Task Scheduler

Here's how to set up the Windows Task Scheduler to run the `daily_update.py` script automatically

1. Open the Task Scheduler application on your Windows machine.
2. Click on "Create Basic Task" or "Create Task" to create a new task.
3. Specify a name and description for the task.
4. Choose a trigger (e.g., daily, weekly) that suits your needs.
5. Select "Start a program" as the action.
6. Provide the path to the Python executable (`python`) as the program/script.
7. Set the arguments to the full path of the `daily_update.py` script.
8. Set the "Start in" field to the directory where the `daily_update.py` script is located.
9. Review the settings and click "Finish" to create the task.



## Error Handling

After every attempt at ingesting the data to Postgres, a log is written to the log.txt file. Each log includes an error code, a brief description of the error and a timestamp of when the error occurred.

Here's the description of possible error codes:

- **Status: 500** - Data Retrieved but Not Ingested to Database: This error indicates that the data retrieval process was successful, but there was an issue with ingesting the data into the database. It could be due to a connection problem, data formatting error, or any other issue preventing the successful ingestion of data.

- **Status: 204** - No New Data to Process: This code signifies that there is no new data available to process. It means that the extraction process was successful, but there were no updates or new data to be transformed and loaded into the database.

- **Status: 200** - Data Retrieved and Ingested Successfully: This status indicates that the data retrieval, transformation, and ingestion processes were successful. It means that the pipeline successfully retrieved the data from the source, transformed it as required, and loaded it into the database without any issues.


