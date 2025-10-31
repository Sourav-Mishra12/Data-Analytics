import pandas as pd
import matplotlib.pyplot as plt

games = pd.read_csv("android-games.csv")

#print(games.columns)
#print(games.head())


# CHECKING THE NULL VALUES

null_rows = games[games['installs'].isnull()]
#print(null_rows)

# CHECKING THE TOP 5 HIGHEST INSTALLED GAMES

highest_installed = games.sort_values(by='installs',ascending=False)
#print(highest_installed[['title','installs']].head(5))

print(games.paid)