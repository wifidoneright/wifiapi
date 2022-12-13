# wifiapi

Centralize your scripting. This is an example of how to utilize your existing scripts and make them available via an API. This example uses [Flask](https://flask.palletsprojects.com/) as the API framework as it is simple and lightweight.

## Requirements

- [Python3](https://www.python.org/downloads/)
- pip3
- 

## Importing Scripts

- put your scripts in a folder
- turn the folder into a module by createing an `__init.py` file. You can leave it blank inside.
  - if you have subfolders then they also will need an `__init__.py` file.
- import the needed functions from the scripts
  - `from scripts.folder.file import function,function,function`
- Create your first API route.

```python
@app.route('/nameaps', methods=['POST'])
def nameaps():
    nodeJSON = [{"name": "AP0001", "mac": "de:ad:be:ef:00:01"}]
    site, aps = prep(nodeJSON)
    # succcesses, failed = name_aps(site, aps)
    return jsonify({"site": displayObjs(site),
        "aps": displayObjs(aps)})
```

That's it! You now have a working API that you can have available to run tasks from external sources. lets say you want to make a website to go along with this, well [here](https://www.codementor.io/@chirilovadrian360/flask-website-templates-open-source-seed-projects-1b6tya9jnl) are some good free ones

## Usage

Starting the dev server

- `python3 app.py`
- `flask run`

Docker - runs with uwsgi

- `docker-compose up`

# Disclamer

This project is for development and security measures will need to be in place before it is used in a production environment. It is to be used at your own risk. Most of the following has been disabled for development and demo purposes.

- ssl
- User authentication
- disable CORS
- ssl certificate verification
