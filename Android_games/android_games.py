import pandas as pd
import matplotlib.pyplot as plt

games = pd.read_csv("android-games.csv")

print(games.columns)
#print(games.head())

# WRITING A FUNCTION TO CONVERT THE INSTALLS VALUE FROM STRING TO NUMERIC

def convert_installs(value):
    value = str(value).strip()
    if 'M' in value:
        return float(value.replace('M', '').strip()) * 1_000_000
    elif 'K' in value:
        return float(value.replace('K', '').strip()) * 1_000
    elif 'B' in value:
        return float(value.replace('B', '').strip()) * 1_000_000_000
    else:
        return float(value) if value.replace('.', '', 1).isdigit() else 0

games['installs'] = games['installs'].apply(convert_installs)


# CHECKING THE NULL VALUES

null_rows = games[games['installs'].isnull()]
#print(null_rows)

# CHECKING THE TOP 5 HIGHEST INSTALLED GAMES

highest_installed = games.sort_values(by='installs',ascending=False)
#print(highest_installed[['title','installs']].head(5))


# RANKING THE GAME CATEGORIES BY HOW MANY INSTALLS THEY HAVE

highest_install_by_cat = games.groupby('category')['installs'].sum().sort_values(ascending=False)
#print(highest_install_by_cat)

# RANKING THE GAMES BY THEIR PRICE

highest_price = games.sort_values(by='price' , ascending=False)
#print(highest_price[['title','price']].head(5))

# GAMES WITH THE HIGHEST REVIEWS

highest_reviews = games.sort_values(by='total ratings' ,  ascending=False)
print(highest_reviews[['title','total ratings']].head())