import pandas as pd


data = pd.read_table("/Users/mac/Downloads/human-descriptions.csv", names=["Photo_ID", "UI_description"])


def char_cnt(x):
    """
    counts the number of characters in each text
    :param x:
    :return:
    """
    return len(x)


data["Char_count"] = data["UI_description"].map(char_cnt)

# Description with the shortest count
min_char_count = data.Char_count.min()
# Description with the longest count
max_char_count = data.Char_count.max()

# Their associated characters
char_max_count = data[data["Char_count"] == min_char_count]["UI_description"]
char_min_count = data[data["Char_count"] == max_char_count]["UI_description"]

mean_char_count = data["Char_count"].mean()

print(min_char_count)
print(max_char_count)

print(char_max_count)
print(char_min_count)

print(mean_char_count)