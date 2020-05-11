# hello mongo
This repo can be used to seed a MongoDB database from the Word Associations API:
https://wordassociations.net/en/api.

I made it to learn pymongo.

To run, you need a Word Associations API key and a MongoDB cluster. Then setup the following environment variables:
```shell
WAN_API_KEY
MONGO_CLUSTER
MONGO_DATABASE
MONGO_USER
MONGO_PASSWORD
```
Finally, you need to install the python packages in ```requirements.txt```.

Once the setup is complete, you can run the program as follows:
```python3 api_to_mongo.py```.
