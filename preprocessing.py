from header import *

df = pd.read_csv("data/final.csv", delimiter=",", on_bad_lines="skip")
df = df.dropna()

df_float = df.select_dtypes(include=['float'])

country_list = []
for country in sorted(set(df["Country Name"].values)):
    country_list.append({
        "label": country,
        "value": country
    })

feature_list = []
for col in df_float.columns:
    feature_list.append({
        "label": col,
        "value": col
    })

min_year = df['Year'].min()
max_year = df['Year'].max()
year_list = []
for year in range(min_year, max_year+1):
    year_list.append({
        "label": year,
        "value": year
    })

region_list = []
for value in df["Region"].value_counts().keys():
    region_list.append({
        "label": value,
        "value": value
    })

incomegroup_list = ["All"]
incomegroup_list += list(df["IncomeGroup"].value_counts().keys())

x_list = []
for col in df_float.columns:
    x_list.append({
        "label": col,
        "value": col
    })
y_list = x_list