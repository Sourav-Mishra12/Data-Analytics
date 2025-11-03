import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

games = pd.read_csv("android-games.csv")

#  FUNCTION TO CONVERT INSTALLS (K, M, B → NUMERIC)
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

# APPLY CONVERSION FUNCTION
games['installs'] = games['installs'].apply(convert_installs)

#  CLEANING CATEGORIES (REMOVE THE WORD 'GAME')
games['category'] = games['category'].str.replace("GAME", "", case=False).str.strip()

#  BASIC DATA CHECKS
print("Total rows:", len(games))
print("Null installs:", games['installs'].isnull().sum())
print("\nColumns:", list(games.columns))

#  TOP 5 HIGHEST INSTALLED GAMES
highest_installed = games.sort_values(by='installs', ascending=False)
print("\nTop 5 most installed games:\n", highest_installed[['title', 'installs']].head())

# RANKING GAME CATEGORIES BY INSTALLS
highest_install_by_cat = (
    games.groupby('category')['installs']
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
highest_install_by_cat['installs_millions'] = highest_install_by_cat['installs'] / 1_000_000

#  PLOT 1: INSTALLED GAMES BY CATEGORY
plt.figure(figsize=(9,6))
sns.barplot(x='installs_millions', y='category', data=highest_install_by_cat, palette='viridis')
plt.title("Ranking Game Categories by Total Installs")
plt.xlabel("Total Installs (Millions)")
plt.ylabel("Game Category")
plt.tight_layout()
plt.show()

#  TOP 5 MOST REVIEWED GAMES
highest_reviews = games.sort_values(by='total ratings', ascending=False)
plt.figure(figsize=(10,6))
sns.barplot(x="total ratings", y="title", data=highest_reviews.head(5), palette="magma")
plt.title("Top 5 Most Reviewed Games")
plt.xlabel("Total Reviews")
plt.ylabel("Game Title")
plt.tight_layout()
plt.show()

#  REVENUE & INSTALLS — FREE VS PAID
games['is_paid'] = games['price'] > 0
games['revenue'] = games['price'] * games['installs']

avg_revenue = games.groupby('is_paid', as_index=False)['revenue'].mean()
avg_revenue['revenue'] = avg_revenue['revenue'] / 1_000_000  # Convert to millions

plt.figure(figsize=(7,5))
sns.barplot(x='is_paid', y='revenue', data=avg_revenue, palette='magma')
plt.title("Average Estimated Revenue: Free vs Paid Games")
plt.xlabel("Game Type")
plt.ylabel("Average Estimated Revenue (Millions USD)")
plt.xticks([0, 1], ['Free', 'Paid'])
plt.tight_layout()
plt.show()

#  REVENUE BY CATEGORY
revenue_by_cat = (
    games.groupby('category')['revenue']
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
plt.figure(figsize=(10,7))
sns.barplot(x='revenue', y='category', data=revenue_by_cat, palette='cubehelix')
plt.title("Estimated Revenue by Category")
plt.xlabel("Revenue (USD)")
plt.ylabel("Category")
plt.tight_layout()
plt.show()

#  CORRELATION ANALYSIS
corr = games[['price','installs','total ratings']].corr()
plt.figure(figsize=(6,5))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Between Installs, Reviews, and Price")
plt.tight_layout()
plt.show()


# GROWTH ANALYSIS

growth_by_cat = games.groupby('category', as_index=False).mean(numeric_only=True)[['category','growth (30 days)','growth (60 days)']]
growth_by_cat['growth_diff'] = growth_by_cat['growth (30 days)'] - growth_by_cat['growth (60 days)']

plt.figure(figsize=(10,7))
sns.barplot(
    y='category',
    x='growth_diff',
    data=growth_by_cat.sort_values('growth_diff', ascending=False),
    palette='coolwarm'
)
plt.title("Recent Growth Momentum by Category (30d - 60d)")
plt.xlabel("Growth Difference (Higher = Faster Recent Growth)")
plt.ylabel("Category")
plt.tight_layout()
plt.show()


# QUALITY ANALYSIS

avg_rating_by_cat = games.groupby('category', as_index=False)['average rating'].mean().sort_values(by='average rating', ascending=False)

plt.figure(figsize=(10,7))
sns.barplot(x='average rating', y='category', data=avg_rating_by_cat, palette='crest')
plt.title("Average Rating by Game Category")
plt.xlabel("Average Rating")
plt.ylabel("Category")
plt.tight_layout()
plt.show()


# RATING DISTRIBUTION

rating_columns = ['5 star ratings','4 star ratings','3 star ratings','2 star ratings','1 star ratings']
rating_dist = games[rating_columns].sum().reset_index()
rating_dist.columns = ['Rating Level','Count']

plt.figure(figsize=(8,5))
sns.barplot(x='Rating Level', y='Count', data=rating_dist, palette='flare')
plt.title("Overall Rating Distribution Across All Games")
plt.tight_layout()
plt.show()


