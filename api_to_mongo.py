#! /usr/bin/env python3

import argparse
import os
import ssl

import pymongo
import requests


def get_data(text, lang, type, limit, pos):
    """Gets data from Word Association Network API"""

    api_key = os.getenv("WAN_API_KEY")

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


def insert_data(data):
    """Inserts data into Mongo DB"""

    user = os.getenv("MONGO_USER")
    password = os.getenv("MONGO_PASSWORD")
    cluster = os.getenv("MONGO_CLUSTER")
    database = "code_names"

    client = pymongo.MongoClient(
        f"mongodb+srv://{user}:{password}@{cluster}/{database}?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE,
    )
    db = client[database]
    collection = db["words"]
    result = collection.insert_one(data)
    print(f"One post: {result.inserted_id}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Gets data from Word Association Network API"
    )

    parser.add_argument(
        "--text",
        dest="text",
        required=True,
        help="Word or phrase with which to find associations",
    )

    parser.add_argument(
        "--lang", dest="lang", required=False, default="en", help="Query language",
    )

    parser.add_argument(
        "--type",
        dest="type",
        required=False,
        default="stimulus",
        help="Type of result. Must be either stimulus or response",
    )

    parser.add_argument(
        "--limit",
        dest="limit",
        required=False,
        default="50",
        help="Maximum number of results",
    )

    parser.add_argument(
        "--pos",
        dest="pos",
        required=False,
        default="noun,adjective,verb,adverb",
        help="Parts of speech to return. Must be noun, adjective, verb and/or adverb",
    )

    args = parser.parse_args()

    insert_data(
        get_data(
            text=args.text,
            lang=args.lang,
            type=args.type,
            limit=args.limit,
            pos=args.pos,
        ),
    )
