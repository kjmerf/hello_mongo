# hello mongo
This application searches for word associations using the Word Associations API:
https://wordassociations.net/en/api.
The associations are inserted into a MongoDB database.

I made it to learn pymongo.

To run, you need a Word Associations API key and a MongoDB cluster. Then setup the following environment variables:
```shell
WAN_API_KEY
MONGO_USER
MONGO_PASSWORD
MONGO_DATABASE
MONGO_CLUSTER
```
Finally, you need to install the python packages in ```requirements.txt```.

Once the setup is complete, you can run the program by calling and passing arguments to ```api_to_mongo.py```.
To find words associated with the word "school", for instance, and insert them into your database, just run:
```python3 api_to_mongo.py --text school```.
