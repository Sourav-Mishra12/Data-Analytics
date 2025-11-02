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
plt.show()

# MOST REVIEWD GAME CATEGORY 

plt.figure(figsize=(10,6))
sns.barplot(x="title" , y="total ratings" , data=highest_reviews.head(5) , palette="viridis")
plt.title("MOST REVIEWED GAMES BY CATEGORIES")
plt.xlabel("TOTAL REVIEWS")
plt.ylabel("GAME TITLE")
plt.tight_layout()
plt.xticks(rotation=10)
plt.show()


# 💵 ANALYSIS 3 — REVENUE & INSTALLS: FREE VS PAID
games['is_paid'] = games['price'] > 0
games['revenue'] = games['price'] * games['installs']

# Average installs and revenue by game type
avg_installs = games.groupby('is_paid', as_index=False)['installs'].mean()
avg_revenue = games.groupby('is_paid', as_index=False)['revenue'].mean()

# Convert revenue to millions for clarity
avg_revenue['revenue'] = avg_revenue['revenue'] / 1_000_000

# 📊 VISUALIZATION 3 — REVENUE: FREE VS PAID
plt.figure(figsize=(7,5))
sns.barplot(x='is_paid', y='revenue', data=avg_revenue, palette='magma')
plt.title("Average Estimated Revenue: Free vs Paid Games")
plt.xlabel("Game Type")
plt.ylabel("Average Estimated Revenue (Millions USD)")
plt.xticks([0, 1], ['Free', 'Paid'])
plt.tight_layout()
plt.show()



# REVENUE PER CATEGORY

games['revenue'] = games['price'] * games['installs']
revenue_by_cat = games.groupby('category')['revenue'].sum().sort_values(ascending=False).reset_index()
sns.barplot(x='revenue', y='category', data=revenue_by_cat, palette='cubehelix')
plt.title("Estimated Revenue by Category")
plt.tight_layout()
plt.show()
