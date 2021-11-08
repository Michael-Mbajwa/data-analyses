from urllib.request import urlopen
import pprint

# I have attempted an analysis of a dataset without using any python module (excluding url open)

# load the play "Romeo and Juliet" by William Shakespeare into python
with urlopen("https://gist.githubusercontent.com/romba050/a9e23b3ba49423489125deb380d192c8/raw/"
             "a22ffa158028444940628d13003b866207cdfc52/Romeo_and_Juliet.txt") as r_and_j_file:
    # r_and_j_file is a file HTTPResponse object
    # print(type(r_and_j_file))  # <class 'http.client.HTTPResponse'>
    # Decode HTTPResponse according to the UTF-8 character encoding (Unicode Transformation Format – 8-bit).
    r_and_j_file = r_and_j_file.read().decode('utf-8')
    # print(type(r_and_j_file))  # <class 'str'>
    # Split the string by newline character to receive a list of line strings.
    text_list = r_and_j_file.splitlines()
    # The book contains 4318 lines.

# Print the first 10 lines of the play. (The title of the play,
# the declaration of a new act and empty lines all count as lines.)
print(text_list[0:10])


# A list of punctuations regularly occurring in the dataset for cleaning
punctuations = [':', '.', ',', ';', '!', '?', ']', '--', '-', "'", '[', ']']
# An empty dictionary for storing the count of the different occurring words in the dataset
words_count = {}
for line in text_list:
    words = line.split()  # Each line is split into different words
    for word in words:
        if len(word) > 0 and word not in punctuations:  # Skips any empty string or punctuation.
            # I noticed occurrence of words such as 'capulet,--hold', 'himself--I'. These are multiple words joined into
            # one by the -- character. I first clean these words.
            if '--' in word:
                word_list = word.split(sep='--')  # Each word that contains -- is split
                for word2 in word_list:
                    if len(word2) > 0 and word2 not in punctuations:  # Skips any empty string or punctuation.
                        while word2[-1] in punctuations:  # This code cleans strings that end with punctuations e.g
                            # 'better:'
                            word2 = word2.strip(punctuations[punctuations.index(word2[-1])])
                        while word2[0] in punctuations:  # This code cleans strings that begin with punctuations e.g
                            # "'better"
                            word2 = word2.strip(punctuations[punctuations.index(word2[0])])

                        word2 = word2.lower()  # This code ensures every word is stored as a lower case.
                        if word2 not in words_count:  # Code checks if the word is already stored in the dictionary.
                            words_count[word2] = 1  # If the word isn't stored, a key for it is created and 1 used as
                            # it's value.
                        else:
                            words_count[word2] += 1  # If the word already exists, 1 is added to the existing value.
            else:  # For words that do not contain '--'
                while word[-1] in punctuations:  # This code cleans strings that end with punctuations e.g 'better:'
                    word = word.strip(punctuations[punctuations.index(word[-1])])
                while word[0] in punctuations:  # This code cleans strings that begin with punctuations e.g "'better"
                    word = word.strip(punctuations[punctuations.index(word[0])])
                word = word.lower()  # This code ensures every word is stored as a lower case
                if word == '&':  # Because & is the same as 'and', it is changed.
                    word = 'and'
                else:
                    pass
                if word not in words_count:  # Code checks if the word is already stored in the dictionary.
                    words_count[word] = 1  # If the word isn't stored, a key for it is created and 1 used as it's value.
                else:
                    words_count[word] += 1  # If the word already exists, 1 is added to the existing value.
        else:
            pass


# Print out the first 10 entries of the dictionary (i.e. 10 (key, value) pairs).
count = 0
for key, value in words_count.items():
    if count < 10:
        count += 1
        print(key, value, sep=": ")


# How many unique words did Shakespeare use in 'Romeo and Juliet'? How often did he use the words "romeo" and
# "juliet" (regardless of capitalization)

# How many unique words

unique_words = len(words_count)
print("There are", unique_words, "unique words.")

# How often the word Romeo was used
romeo_count = 0
for line in text_list:
    words = line.split()
    for word in words:
        if "romeo" in word.lower():
            romeo_count += 1
print("The word 'romeo' occurs", romeo_count, "times.")


# How often the word Juliet was used
juliet_count = 0
for line in text_list:
    words = line.split()
    for word in words:
        if "juliet" in word.lower():
            juliet_count += 1
print("The word 'juliet' occurs", juliet_count, "times.")


# The next goal of our analysis is to find out which words Shakespeare used the most when writing 'Romeo and Juliet'.
# To achieve this, use a list comprehension to recreate your dictionary, but this time, insert the elements in a
# specific order: start with the most common word and end with the words that only appear once in the whole text.

sorted_dic = [(word, words_count[word]) for word in sorted(words_count, key=words_count.get, reverse=True)]
print(sorted_dic)

print('The ten most used words are:')
print(sorted_dic[:10])
