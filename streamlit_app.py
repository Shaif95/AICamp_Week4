import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import warnings

#look for more information here https://docs.streamlit.io/library/cheatsheet

#adding title
st.title("Dizzy Doughnut")
df = pd.read_csv("Fifa.csv")

st.write(df.head(2))

from PIL import Image
import requests
from io import BytesIO
# List of image links
image_links = df["Image Link"].head(20)
# List of labels
labels = df["Known As"].head(20)


# Function to load an image from a URL
def load_image_from_url(url):
  response = requests.get(url)
  image = Image.open(BytesIO(response.content))
  return image


# Calculate the number of rows and columns for the subplot grid
num_images = len(image_links)
num_rows = 2
num_cols = (num_images + 1) // 2


# Create a subplot grid
def display_images():
  # Plot each image in the grid with its corresponding label
  for i, image_link in enumerate(image_links):
    if i < num_images:
      image = load_image_from_url(image_link)
      label = labels[i]

      # Display the image with label
      st.image(image, caption=label, use_column_width=True)


#Spencer :

#Introduction : Write a couple of lines about the dataset Fifa 23

st.header("Using the dataset, who is the GOAT of soccer?")

fig, ax = plt.subplots(figsize=(27, 6))
# Create the bar plot
ax.bar(df["Known As"].head(20), df["Overall"].head(20))
# Customize plot labels and title
ax.set_xlabel("Player")
ax.set_ylabel("Overall Score")
ax.set_title("Overall Ratings of Top Players")
# Display the plot in Streamlit app
st.pyplot(fig)

st.write(
  "By using overall score and the order in which the dataset was presented, we can see that Messi is the top player and is presumably the best player in terms of the data that we have. While some might also suggest that Cristiano is the best player, he is actually 9th in our data and is below Messi in overall score as well."
)

st.title('Image Gallery')
display_images()

st.header(
  "How large is the standard deviation for the players in terms of skill or win rates?"
)

fig, ax = plt.subplots()
df.hist("Overall", ax=ax)
st.pyplot(fig)

st.write("Standard Deviation = 6.788352681607474")
st.write("Range = 44")
st.write("Mean = 65.85204164194401")
st.write(
  "By figuring out the mean, standard deviation, and range, we can see that the mean and SD is actually not as high as what people think. This is due to the fact that many players are hovering in the 60s-70s in overall score and there not being too much outliers in the dataset to really change the average or distance from the mean. However, we still see a wide range of players due to the fact that the range is pretty high."
)

st.header("What is the relationship between age and skill level?")

fig = px.scatter(df,
                 x='Age',
                 y='Overall',
                 color='Age',
                 title="Relationship Between Age and Skill Level")

st.plotly_chart(fig)

st.write(
  "What was most interesting about the correlation between age and skill is how its not as much of a factor as initially hypothosized. There is still a slight curve up when the age goes up and curve down when players are getting older, but the skill level range is high enough to where it does not make much of a difference when seen in the data."
)

st.header(
  "How often do top players be on the top of different skills, such as Balance or Shot Power?"
)

df1 = df.head(20)  #df1 = top 20 players
sorted_df = df.sort_values(by='GK Rating', ascending=False)
df2 = sorted_df.head(20)
intersection_df = pd.merge(df1, df2, on='Known As', how='inner')

# Calculate the number of common rows
intersection_count = len(intersection_df)
# Calculate the number of unique rows in each dataframe
df1_unique_count = len(df1) - intersection_count
df2_unique_count = len(df2) - intersection_count
# Data for the pie chart
labels = ['Intersection', 'DF1 Unique', 'DF2 Unique']
sizes = [intersection_count, df1_unique_count, df2_unique_count]
colors = ['skyblue', 'lightcoral', 'lightgreen']
explode = (0.1, 0, 0)  # explode the first slice (Intersection)
# Plotting the pie chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(sizes,
       explode=explode,
       labels=labels,
       colors=colors,
       autopct='%1.1f%%',
       shadow=True,
       startangle=140)
ax.set_title(
  'Example of an Intersection between Overall Top Players and Top Players in Different Skills'
)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Display the pie chart in Streamlit
st.pyplot(fig)
#Make sure you have both Streamlit and Matplotlib installed (pip install streamlit matplotlib) to run the code correctly. Also, replace the sample data (sizes, labels, colors, explode) with your actual data to create the desired pie chart.

st.write(
  "There are two types of skill levels: Skills used during play and scores for how each player plays in a position. For the actual skills, there is a low intersection between the players overall score and skill score - many of which are in the low 10s and maybe even lower. There are still some outliers, with some being higher in the 40s. I believe this is the case as many players are good in their own type of skillsets and I theorize many players in different skill intersections are unique and don't come up as much in different skills. For each position on the field, there is a much higher result, with some going into the 30s but with some still in the early 10s. Another thing that could affect this is where the players usually play on the field. A goalie usually isn't good at scoring and a offensive player usually doesn't block shots from reaching the goal. Due to this, many players will not share all of the skill sets that are avaliable in the dataset."
)

#Rishi :

st.header("Who are the players with the best potential for improvement?")

df['Potential-Overall'] = df['Potential'] - df['Overall']
df_sorted = df.sort_values(by='Potential-Overall', ascending=False)
df_filtered = df_sorted.query('Overall >= 85')[:20]
df_filtered[
  'Potential-Overall'] = df_filtered['Potential'] - df_filtered['Overall']
df_sorted = df.sort_values(by='Potential-Overall', ascending=False)
players = df_filtered['Known As']
potential_improvement = df_filtered['Potential-Overall']
plt.figure(figsize=(10, 6))
plt.bar(players, potential_improvement, color='skyblue')
plt.xlabel('Players')
plt.ylabel('Potential Improvement')
plt.title('Players with the Best Potential for Improvement')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
st.write(
  "In order to do this, we first needed to filter out the players that were of low overalls, since there were many with high potential-overall differences since they had a lot of time to play. I did this by ensuring that the data only included players above the rating of 85 so that we only received data from the currently relevant players. This showed that the players with the best potential for improvement included big names such as Pedri, Foden, Vinicius Jr., Haaland, and more."
)

st.header("How does the age of a player affect their potential?")
df['Potential-Overall'] = df['Potential'] - df['Overall']
fig2 = px.scatter(df, x='Age', y='Potential-Overall', color="Overall")
fig2
st.write(
  "Oftentimes, as someone’s body ages, they get worse at the sport they play. This is shown through the graph, where young teenagers with time to go have higher potentials for improvement, whereas older players who are due to retire soon have a lower, or even no potential for improvement."
)

st.header("How does potential affect the value of the release clause?")
fig1 = px.scatter(
  df,
  x='Potential',
  y='Release Clause',
  title='The Relationship between Potential and Release Clause',
  labels={
    'Potential': 'Potential',
    'Release Clause': 'Release Clause Value (in euros)'
  })
fig1
st.write(
  "In this diagram, we can see that, as the potential overall of a player increases, so does the release clause value. This is because clubs apply a higher cost upon their players so that they don't leave, since the clubs want better players to stay and help them win."
)

st.header("How does rating affect international reputation?")
Scatter2 = df.plot.scatter(x='Overall', y='International Reputation')
Scatter2
st.write(
  "In this diagram, we can see that the international reputation of a player is, on average, higher when a player is rated higher. We can see this through the fact that the players at the lower end of the overall spectrum have no international reputation, but players on the highest end of the spectrum have a very high international reputation."
)

#Gabe :

#Who are the Top players based on different Positions ?      : Bar Chart
st.header("what postions are players of a similar rank most likely to play")
import pandas as pd
import matplotlib.pyplot as plt

# Assuming your DataFrame is named 'df'
# Select rows where 'Best Position' is equal to 'CAM'
filtered_df = df[df['Best Position'] == 'CAM']

# Sort the filtered DataFrame by 'Best Position'
sorted_df = filtered_df.sort_values(by='Overall').head(20)

# Plotting a bar chart for Best Position with Known As in X
st.pyplot(plt.figure(figsize=(15, 5)))  # Adjust the figure size if needed

# Plot the bar chart
plt.bar(sorted_df['Known As'], sorted_df['Overall'])
plt.xlabel('Known As')
plt.ylabel('Best Position')
plt.title('Best Position vs. Known As')
plt.xticks(rotation=20)  # Rotate the x-axis labels if they are too long

# Display the chart using Streamlit
st.pyplot()

#How does wage impact Overall ranking?
st.header("how doesa the wage of a player impact their over all ranking?")
val_overall = px.scatter(df,
                         x='Value(in Euro)',
                         y='Overall',
                         color="Nationality")
st.plotly_chart(val_overall)
#Is there any relation between Position played and age ?    : Scatter
st.header(
  "what is the relation between postion played and the age of a player")

pos_age = px.scatter(df, x='Age', y='Positions Played', color="Overall")
#Conclusion :
st.plotly_chart(pos_age)
