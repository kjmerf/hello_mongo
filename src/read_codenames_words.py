
with open("../codenames_words.txt") as f:
    raw = f.readlines()

word_list = []
for line in raw:
    word_list.append(line.split("\t"))

word_list = [item.strip("\n") for sublist in word_list for item in sublist]
