#! /usr/bin/env python3

import os

WAN_API_KEY = os.getenv("WAN_API_KEY")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
MONGO_DATABASE = os.getenv("MONGO_DATABASE")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

raw_collection = "words"
clean_collection = "words_clean"
clean_collection_unique_index = "text"
result_types = ("stimulus", "response")

words_to_insert = (
    "Hollywood",
    "Well",
    "Foot",
    "New York",
    "Spring",
    "Court",
    "Tube",
    "Point",
    "Tablet",
    "Slip",
    "Date",
    "Drill",
    "Lemon",
    "Bell",
)
