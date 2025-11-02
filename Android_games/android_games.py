import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


games = pd.read_csv("android-games.csv")

#print(games.columns)
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

games['category'] = games['category'].str.replace("GAME" , " " , case=False)  # CLEANED THE NAME OF THE CATEGORIES IN THE COLUMN 'CATEGORY'

# CHECKING THE NULL VALUES

null_rows = games[games['installs'].isnull()]
#print(null_rows)

# CHECKING THE TOP 5 HIGHEST INSTALLED GAMES

highest_installed = games.sort_values(by='installs',ascending=False)
#print(highest_installed[['title','installs']].head(5))


# RANKING THE GAME CATEGORIES BY HOW MANY INSTALLS THEY HAVE

highest_install_by_cat = games.groupby('category')['installs'].sum().sort_values(ascending=False).reset_index()
#print(highest_install_by_cat)

# RANKING THE GAMES BY THEIR PRICE

highest_price = games.sort_values(by='price' , ascending=False)
#print(highest_price[['title','price']].head(5))

# GAMES WITH THE HIGHEST REVIEWS

highest_reviews = games.sort_values(by='total ratings' ,  ascending=False)
#print(highest_reviews[['title','total ratings']].head())

# PLOTTING THE ANALYSIS WE PERFORMED

highest_install_by_cat['installs_millions'] = highest_install_by_cat['installs'] / 1_000_000

plt.figure(figsize=(9,6))
sns.barplot(x='installs_millions', y='category', data=highest_install_by_cat, palette='viridis')
plt.title("Ranking Game Categories by Total Installs")
plt.xlabel("Total Installs")
plt.ylabel("Game Category")
plt.tight_layout()
#plt.show()

# MOST REVIEWD GAME CATEGORY 

plt.figure(figsize=(10,6))
sns.barplot(x="title" , y="total ratings" , data=highest_reviews.head(5) , palette="viridis")
plt.title("MOST REVIEWED GAMES BY CATEGORIES")
plt.xlabel("TOTAL REVIEWS")
plt.ylabel("GAME TITLE")
plt.tight_layout()
plt.xticks(rotation=10)
#plt.show()


# WHICH GAMES ARE PAID WHICH ARE NOT

games['is_paid'] = games['price'] > 0
sns.boxplot(x='is_paid', y='installs', data=games)
plt.title("Free vs Paid Game Installs")
plt.xlabel("Is Paid Game?")
plt.ylabel("Installs")
plt.show()


