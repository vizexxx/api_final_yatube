# Yatube API

An API of a simple social network. Supports posts, comments, followers and authentications. Check the `redoc` endpoint for usage documentation.

## Installation

Clone the project using `git clone`, switch into the created folder and do the following:

1. Create and activate python virtual environment (e.g. using `venv`) and install the dependencies:

```
python -m venv venv
. .\venv\Scripts\activate.ps1
pip install -r requirements.txt
```

2. Apply the migrations:

```
python .\yatube_api\manage.py migrate
```

3. Run the server in debug mode:

```
python .\yatube_api\manage.py runserver
```
