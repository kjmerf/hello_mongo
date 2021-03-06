#! /usr/bin/env python3

import os

import words_to_insert

WAN_API_KEY = os.getenv("WAN_API_KEY")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
MONGO_DATABASE = os.getenv("MONGO_DATABASE")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

raw_collection = "words"
clean_collection = "words_clean"
clean_max_collection = "words_clean_max"
result_types = ("stimulus", "response")
parts_of_speech = ("noun", "verb", "adjective", "adverb")

words_to_insert = words_to_insert.words
