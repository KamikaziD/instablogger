# InstaBlogger API

## Readme

### Setup


### ENVIRONMENT SETUP
#### Open the terminal and navigate to the project directory

#### Create a virtual environment
```commandline
python -m venv env
```
```commandline
source env/bin/activate
```

#### Install API requirements:
```commandline
pip install -r requirements.txt
```

### SETUP ENV
```dotenv
SERVER_PORT=8001
SERVER_URL=http://localhost:${SERVER_PORT}
DATABASE_URL=sqlite:///./ib_api.db
AUTH_SECRET_KEY={your_own_secret_key}
```

**NB**: generate a new AUTH_KEY_SECRET
```commandline
openssl rand -hex 32
```
* Add the generated key into the .env by AUTH_SECRET_KEY

### RUN APPLICATION
* ```python main.py```
* Browser url: ```http://localhost:8001```
* Swagger url: ```http://localhost:8001/docs```
* ReDoc url: ```http://localhost:8001/redoc```

