#! /usr/bin/env python3

import ssl

import pymongo
import requests

import settings


def get_data(
    api_key,
    text,
    lang="en",
    type="stimulus",
    limit=50,
    pos="noun,adjective,verb,adverb",
):
    """Gets data from Word Association Network API"""

    url = "https://api.wordassociations.net/associations/v1.0/json/search?"
    options = "&".join(
        (
            f"apikey={api_key}",
            f"text={text}",
            f"lang={lang}",
            f"type={type}",
            f"limit={limit}",
            f"pos={pos}",
        )
    )
    response = requests.get(url + options)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.status_code)


def get_mongo_client(cluster, database, user, password):
    """Get MongoDB client"""

    return pymongo.MongoClient(
        f"mongodb+srv://{user}:{password}@{cluster}/{database}?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE,
    )


def insert_data(client, database, collection, data):
    """Inserts data into collection"""

    try:
        result = client[database][collection].insert_one(data)
        print(f"Inserted: {result.inserted_id} into {collection}")
    except pymongo.errors.DuplicateKeyError:
        pass


def clean_data(client, database, raw_collection, clean_collection):
    """Creates clean collection from raw collection"""

    db = client[database]

    # create unique index to reject duplicates in clean collection
    db[clean_collection].create_index(
        [("text", pymongo.DESCENDING), ("type", pymongo.DESCENDING)], unique=True
    )

    for document in db[raw_collection].find():
        response = document["response"][0]
        # type is not included in the response but we want this field in the clean documents
        response["type"] = document["request"]["type"]
        insert_data(client, database, clean_collection, response)


if __name__ == "__main__":

    client = get_mongo_client(
        settings.MONGO_CLUSTER,
        settings.MONGO_DATABASE,
        settings.MONGO_USER,
        settings.MONGO_PASSWORD,
    )

    for text in settings.words_to_insert:
        for type in settings.result_types:
            insert_data(
                client,
                settings.MONGO_DATABASE,
                settings.raw_collection,
                get_data(api_key=settings.WAN_API_KEY, text=text, type=type),
            )

    clean_data(
        client,
        settings.MONGO_DATABASE,
        settings.raw_collection,
        settings.clean_collection,
    )
