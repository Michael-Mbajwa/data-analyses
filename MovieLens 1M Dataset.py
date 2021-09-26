import re
from datetime import datetime
import numpy as np
import pandas as pd
import csv
import json
from numpy import nan as NA
from dateutil.parser import parse
import collections
import seaborn as sns
import matplotlib.pyplot as plt

"""
The MovieLens 1M dataset contains 1 million ratings collected from 6,000 users on 4,000 movies.
"""
# If you study the result from, you'll notice the data does not have it's own column names hences it's using
# the first row as a column name. We will solve this problem.
mnames = ['movie_id', 'title', 'genres']
movies_data = '/Users/mac/Desktop/pydata-book-2nd-edition/datasets/movielens/movies.dat'
movies = pd.read_table(movies_data, sep='::', engine='python', names=mnames)

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users_data = '/Users/mac/Desktop/pydata-book-2nd-edition/datasets/movielens/users.dat'
users = pd.read_table(users_data, sep='::', engine='python', names=unames)

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings_data = '/Users/mac/Desktop/pydata-book-2nd-edition/datasets/movielens/ratings.dat'
ratings = pd.read_table(ratings_data, engine='python', sep='::', names=rnames)

# Since this data is spread across different tables, we begin merging
data = pd.merge(pd.merge(ratings, users), movies)

# Let's get the mean tv rating for each movie grouped by gender
mean_ratings = data.pivot_table('rating', columns='gender', index='title', aggfunc='mean')

# To identify movies with more than 250 ratings
ratings_by_title = data.groupby('title').size()
active_titles = ratings_by_title[ratings_by_title > 250].index

# Let's select the movies with more than 250 ratings from our mean_ratings dataset
mean_ratings = mean_ratings.loc[active_titles]

# Let's view the movies highly rated by females
top_female_ratings = mean_ratings.sort_values(by='F', ascending=False)

# Let's inspect the differences in the ratings
mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
