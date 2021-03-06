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


def insert_data(client, database, collection, data, print_message=None):
    """Inserts data into collection"""

    try:
        result = client[database][collection].insert_one(data)
        print_message = print_message or result.inserted_id
        print(f"Inserted {print_message} into {collection}")
    except pymongo.errors.DuplicateKeyError:
        pass


def get_document(client, database, collection, text, type, pos):
    """Get document from collection"""

    db = client[database]
    return db[collection].find_one({"text": text, "type": type, "pos": pos})


def clean_data(client, database, raw_collection, clean_collection):
    """Creates clean collection from raw collection"""

    db = client[database]

    # create unique index to prevent duplicates in clean collection
    db[clean_collection].create_index(
        [
            ("text", pymongo.DESCENDING),
            ("type", pymongo.DESCENDING),
            ("pos", pymongo.DESCENDING),
        ],
        unique=True,
    )

    for document in db[raw_collection].find():
        response = document["response"][0]
        # type and pos are not in response but we want them in clean documents
        response["type"] = document["request"]["type"]
        response["pos"] = document["request"]["pos"]
        insert_data(
            client=client,
            database=database,
            collection=clean_collection,
            data=response,
            print_message=(response["text"], response["type"], response["pos"]),
        )


def get_max(client, database, clean_collection, clean_max_collection):
    """Creates clean max collection from clean collection"""

    # create unique index to prevent duplicates in clean collection
    client[database][clean_max_collection].create_index(
        [("text_type", pymongo.DESCENDING)], unique=True,
    )

    for text in settings.words_to_insert:
        for type in settings.result_types:
            max = {}
            for pos in settings.parts_of_speech:
                document = get_document(
                    client, database, settings.clean_collection, text, type, pos
                )
                if document:
                    for item_dct in document["items"]:
                        if item_dct["item"] not in max:
                            max[item_dct["item"]] = item_dct["weight"]
                        elif item_dct["weight"] > max[item_dct["item"]]:
                            max[item_dct["item"]] = item_dct["weight"]
                else:
                    print(f"{text}, {type}, {pos} not found in {clean_collection}")

            insert_data(
                client=client,
                database=database,
                collection=clean_max_collection,
                data={"text_type": f"{text}_{type}", "items": max},
                print_message=(text, type),
            )


if __name__ == "__main__":

    client = get_mongo_client(
        settings.MONGO_CLUSTER,
        settings.MONGO_DATABASE,
        settings.MONGO_USER,
        settings.MONGO_PASSWORD,
    )

    for text in settings.words_to_insert:
        for type in settings.result_types:
            for pos in settings.parts_of_speech:
                insert_data(
                    client=client,
                    database=settings.MONGO_DATABASE,
                    collection=settings.raw_collection,
                    data=get_data(
                        api_key=settings.WAN_API_KEY,
                        text=text,
                        type=type,
                        limit=300,
                        pos=pos,
                    ),
                    print_message=(text, type, pos),
                )

    clean_data(
        client,
        settings.MONGO_DATABASE,
        settings.raw_collection,
        settings.clean_collection,
    )

    get_max(
        client,
        settings.MONGO_DATABASE,
        settings.clean_collection,
        settings.clean_max_collection,
    )
