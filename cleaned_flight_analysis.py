
# Importing necessary libraries

# Web scraping and HTML parsing
import requests
from bs4 import BeautifulSoup

# Data manipulation and analysis
import pandas as pd
import numpy as np

# Data visualization
import matplotlib.pyplot as plt
from matplotlib import dates as mpl_dates
import seaborn as sns

# Time and Date manipulation
from time import sleep
from datetime import datetime, date, timedelta

# Set up for inline plotting (specific to Jupyter notebooks)
sns.set(style="whitegrid")  # Set Seaborn aesthetic style


# Loading the Dataset
# Description:
# The dataset was constructed over several days, and new files were created daily to prevent data corruption and accidental overwriting.

# Reading and concatenating multiple CSV files into a single DataFrame
file_list = ['24MEL.csv', '25MEL.csv', '26MEL.csv']
mdf = pd.concat([pd.read_csv(file) for file in file_list])

# Removing unnecessary columns
mdf.drop(columns=['Unnamed: 0'], inplace=True)

# Converting date and time columns to appropriate data types
mdf['departure_date'] = pd.to_datetime(mdf['departure_date'])
mdf['departure_time'] = pd.to_datetime(mdf['departure_time']).dt.time
mdf['arrival_time'] = pd.to_datetime(mdf['arrival_time'], errors='coerce').dt.time


# Data Cleaning and Transformation

# Handling missing values and duplicates
mdf.dropna(inplace=True)  # Dropping rows with missing values
mdf.drop_duplicates(inplace=True)  # Dropping duplicate rows

# Adding a new column for day of the week
mdf['departure_day'] = mdf['departure_date'].dt.day_name()

# Display basic descriptive statistics of the dataset
print(mdf.describe(include='all'))


# Descriptive Statistics and Additional Analysis
# Overview:
# To gain a deeper understanding of the dataset, we'll look at some key statistics, including the distribution of prices, the most common airlines, and the distribution of departure days.

# Analyzing the distribution of prices
plt.figure(figsize=(10, 6))
sns.histplot(mdf['price'], kde=True, color='blue')
plt.title('Distribution of Flight Prices')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# Most common airlines
common_airlines = mdf['airline'].value_counts()
print("Most Common Airlines:\n", common_airlines)

# Distribution of departure days
plt.figure(figsize=(10, 6))
sns.countplot(y='departure_day', data=mdf, palette='viridis')
plt.title('Flight Departure Days Distribution')
plt.xlabel('Frequency')
plt.ylabel('Day of the Week')
plt.show()


# Data Visualization
# Description:
# The following visualizations examine the relationship between flight prices and departure times, both overall and segmented by class (e.g., Economy, Business).

# Splitting data by class
y_class = mdf[mdf['class'] == 'Economy']
j_class = mdf[mdf['class'] == 'Business']

# Setting up subplots
fig, axs = plt.subplots(2, 2, figsize=(15, 12))

# KDE plot for all classes
sns.kdeplot(ax=axs[0, 0], x='price', y='departure_time', data=mdf, fill=True, cmap="rocket_r")
axs[0, 0].set_title('Price vs Departure Time (All Classes)')

# KDE plot for Economy class
sns.kdeplot(ax=axs[0, 1], x='price', y='departure_time', data=y_class, fill=True, cmap="rocket_r")
axs[0, 1].set_title('Price vs Departure Time (Economy Class)')

# KDE plot for Business class
sns.kdeplot(ax=axs[1, 0], x='price', y='departure_time', data=j_class, fill=True, cmap="rocket_r")
axs[1, 0].set_title('Price vs Departure Time (Business Class)')

# Placeholder plot
sns.kdeplot(ax=axs[1, 1], x='price', y='departure_date', data=j_class, fill=True, cmap="rocket_r")
axs[1, 1].set_title('Price vs Departure Date (Business Class)')

# General plot settings
plt.xticks(rotation=45)
plt.subplots_adjust(hspace=0.4)
plt.show()
