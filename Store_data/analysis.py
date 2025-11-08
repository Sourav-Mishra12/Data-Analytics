import pandas as pd 

data = pd.read_csv("retail_sales_dataset.csv")

# print(data.head(10))
# print(data.info())
# print(data.isnull().sum())


data['Date'] = pd.to_datetime(data['Date'])
# print(data.duplicated())

data['Month'] = data['Date'].dt.month_name()
data['Year'] = data['Date'].dt.year

data['Revenue' ] = data['Quantity'] * data['Price per Unit']

print(data.head())

# WE FOUND NO NULL AND DUPLICATED VALUES SO WE WILL BE MOVING TOWARDS SOME BASIC STATISTICAL ANALYSIS OF THE DATA

# total_revenue = data['Total Amount'].sum()
# print(f"\nTHE TOTAL REVENUE IS : {total_revenue} \n")

# total_transactions = data.shape[0]
# print(f" THE TOTAL NUMBER OF TRANSACTIONS ARE : {total_transactions} \n ")

# total_customers = data['Customer ID'].nunique()
# print(f" THE TOTAL NUMBER OF CUSTOMERS ARE : {total_customers} \n ")

# avg_transactions = data['Revenue'].mean()
# print(f" THE AVERAGE TRANSACTION IS : {avg_transactions}")

# avg_age = data['Age'].mean()
# print(f"THE AVERAGE AGE GROUP DOING THE PURCHASE : {round(avg_age)}")

# best_selling_cat = data.groupby('Product Category')['Revenue'].sum().sort_values(ascending=False)
# print(f" THE BEST SELLING CATEGORY : \n {best_selling_cat} \n")

# most_sold_cat = data.groupby('Product Category')['Quantity'].sum().sort_values(ascending=False)
# print(f" THE MOST SOLD CATEGORY : \n {most_sold_cat}")

# gender_sales = data.groupby('Gender')['Revenue'].sum().sort_values(ascending=False)
# print(f" HOW MUCH EACH GENDER SPENDS : {gender_sales}")    # females tend to spend more 

# avg_gender_sales = data.groupby('Gender')['Revenue'].mean()
# print("THE AVERAGE SPENDINGS BY EACH GENDER : " , avg_gender_sales)

female_data = data.loc[data['Gender'] == 'Female']

female_sales_data = (
    female_data.groupby('Product Category').agg(total_revenue = ('Revenue' , 'sum')).sort_values(by= 'total_revenue',ascending=False)
)
print(female_sales_data)

top_female_category = female_sales_data.index[0]
print(f"THE MOST SPENT CATEGORY BY FEMALE : {top_female_category}")   # the females are spending more on the clothing category



male_data = data.loc[data['Gender'] == 'Male']

male_sales_data = (
    male_data.groupby('Product Category').agg(total_revenue = ('Revenue' , 'sum')).sort_values(by= 'total_revenue',ascending=False)
)
print(male_sales_data)

top_male_category = male_sales_data.index[0]
print(f"THE MOST SPENT CATEGORY BY FEMALE : {top_male_category}")   

