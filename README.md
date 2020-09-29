# Tree of Life Swagger OpenAPI 3 server

## Overview
This Swagger API return Tree of Life pre-allocated public names, taken from [ToL sample naming](https://gitlab.com/wtsi-grit/darwin-tree-of-life-sample-naming) project. Please note that you can not allocate new names using this API.

This application uses the [Connexion](https://github.com/zalando/connexion) library on top of Flask.

This server was initially generated by the [swagger-codegen](https://github.com/swagger-api/swagger-codegen) project, using language "python-flask". 
You can easily generate a server stub by using the [OpenAPI-Spec](https://github.com/swagger-api/swagger-core/wiki) from a remote server.  



## Requirements
Python 3.5.2+

## Setup
- First create a local Python virtual enviroment
```
python3 -m venv venv
```

- Activate the Python virtual enviroment
```
source venv/bin/activate
```

- Read and run the pre-reqs in setup.py
```
python3 setup.py install
```

- Install all required Python libraries
```
pip3 install -r requirements.txt
```

- Install connexion with extra install: 
```
pip3 install 'connexion[swagger-ui]'
```


## Usage
To run the server, first make the "start.sh" executable 
```
chmod +x ./start.sh
```

then run "start.sh" 
```
./start.sh
```

or alternatively execute the following from the root directory:
```
source venv/bin/activate
python -m swagger_server
```

and open your browser to here:
```
http://localhost:8080/ui/
```

You can directly test the server:
```
curl -X GET "http://localhost:8080/public-name?searchString=9606" -H  "accept: application/json"
```

The Swagger definition lives here:
```
http://localhost:8080/swagger.json
```

To launch the integration tests, use tox:
```
sudo pip install tox
tox
```

## Example usage and output
You can search for NCBI taxonomy ids in the "/public-name" end-point. You can also use CURL like this:
```
curl -X GET "http://localhost:8080/public-name?searchString=6344" -H  "accept: application/json"
```

The output for NCBI tax id 6344 will look something like this:
```
{
  "data": [
    {
      "class": "Polychaeta",
      "common_name": "lugworm",
      "family": "Arenicolidae",
      "genus": "Arenicola",
      "order": "None",
      "phylum": "Annelida",
      "prefix": "wuAreMari",   <- This is the PUBLIC_NAME field
      "species": "Arenicola marina",
      "taxid": "6344"
    }
  ]
}
```

In the DToL manifest this maps to:
```
ORDER_OR_GROUP: Capitellida
FAMILY: Arenicolidae	
GENUS: Arenicola	
TAXON_ID: 6344	
SCIENTIFIC_NAME: Arenicola marina
COMMON_NAME: lugworm			
```
This is the URL from NCBI for id [6344](https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=6344)


## Rebuild the local sqlite3 database
The database is rebuilt from scratch each time you use the "start.sh" script. 
You can alternatively run the script "reset_database.sh"

## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
docker build -t swagger_server .

# starting up a container
docker run -p 8080:8080 swagger_server
```