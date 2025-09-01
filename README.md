# CS340-Term-Project

## Installation

### Download Application Source
```bash
$ git clone https://github.com/aneugart/CS340-Term-Project
```

### Virtual Python Environment (Strongly recomended)
Create and activate a vertual environment.  Using venv this may be done as follows:
```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

### Create database config
Create a file in the same directory as the static_config.py file named db_config.py and give it the following contents:
```python
db_hostname = ""    # Eg. "classmysql.engr.oregonstate.edu"
db_database = ""    # Eg. "cs340_OSUUsername
db_username = ""    # Eg. "cs340_OSUUsername
db_password = ""    # Eg. last four digits of OSUID
```
### Create tables
Either via the command line interface or PhPMyAdmin source the Group_67_DDL.sql file in the application's root directory.

### Install web application
From the directroy containing the pyproject.toml file, run the following.
```bash
$ source venv/bin/activate
(venv) $ pip install --editable .
```

### Run the server
From the root directory of the application (the directory containing app.py), run the server.  Replace XXXX with an open
port that the user has access to eg. 6767
```bash
(venv) $ gunicorn --error-logfile gunicorn_error.log -b 0.0.0.0:9231 -D 'web_app:create_app()'
```

### Stop the application
Stop the application when you are done with it and no longer wish for it to be accessable at the given port.

Replace OSUUsername with your username.
```bash
(venv) $ pkill -u OSUUsername gunicorn
```
