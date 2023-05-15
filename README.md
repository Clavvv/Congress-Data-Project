# Congressional Member ETL Backend

This project is the backend component of a visualization web app that utilizes an ETL (Extract, Transform, Load) pipeline to gather congressional member information and voting data. The backend is implemented using Python, Postgres, and an existing public API.

## Features

- Extracts congressional member information and voting data from a public API.
- Transforms and cleans the data to ensure consistency and accuracy.
- Loads the processed data into a Postgres database for easy querying and analysis.

## Requirements

- Python 3.7 or higher
- Postgres database
- Internet connectivity to access the public API

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Clavvv/Congress-Data-Project.git```

## Configuration

Before running the ETL pipeline, you need to configure some settings. 

### Database Configuration

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
