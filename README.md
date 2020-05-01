# hello mongo
This application searches for word associations using the Word Associations API:
https://wordassociations.net/en/api.
The associations are inserted into a MongoDB database called ```code_names``` into a collection called ```words```.

I made it to learn pymongo.

To run, you need a Word Associations API key and a MongoDB cluster. Then setup the following environment variables:
```shell
WAN_API_KEY
MONGO_USER
MONGO_PASSWORD
MONGO_CLUSTER
```
Finally, you need to install the python packages in ```requirements.txt```.

Once the setup is complete, you can run the program as follows:
```python3 api_to_mongo.py --text school```.

The command above inserts words associated with "school" into the target collection and database.
