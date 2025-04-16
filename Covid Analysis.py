import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
file_path = "covid-data.xlsx"
df = pd.read_excel(file_path)

# Randomly select three countries for analysis
selected_countries = df['location'].dropna().sample(n=3, random_state=42).tolist()
df_selected = df[df['location'].isin(selected_countries)].copy()
# Display the cleaned dataset
print(df_selected.head())

# Check the percentage of missing values per column
missing_percentage = df_selected.isna().mean() * 100
print("Percentage of missing values per column:")
print(missing_percentage)

df_selected.iloc[:, 4:] = df_selected.iloc[:, 4:].interpolate(method='linear', limit_direction='both') #fill the missing values
df_selected.iloc[:, 4:] = df_selected.iloc[:, 4:].clip(lower=0) #Delete the negative values

# Convert date column to datetime
if 'date' in df_selected.columns:
    df_selected['date'] = pd.to_datetime(df_selected['date'])
    
# Display the cleaned dataset
print(df_selected.head())

# Check the percentage of missing values per column AGAIN
missing_percentage = df_selected.isna().mean() * 100
print("Percentage of missing values per column:")
print(missing_percentage)

# Define columns for plotting as specified in the assignment
columns_to_plot = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths', 
                   'total_cases_per_million', 'new_cases_per_million', 
                   'total_deaths_per_million', 'new_deaths_per_million', 
                   'icu_patients', 'hosp_patients']
                   

# Generate line plots
for country in selected_countries:
    df_country = df_selected[df_selected['location'] == country]
    plt.figure(figsize=(12, 6))
    for column in columns_to_plot:
        if column in df_country.columns:
            plt.plot(df_country['date'], df_country[column], label=column)
    plt.title(f"COVID-19 Trends in {country}")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.legend()
    plt.savefig(f"{country}_line_plot.png")
    plt.show()
    plt.close()
    
# Generate quarterly box plots and calculate quartiles
for country in selected_countries:
    df_country = df_selected[df_selected['location'] == country].copy()
    df_country['quarter'] = df_country['date'].dt.to_period("Q")
    plt.figure(figsize=(12, 6))
    for column in columns_to_plot:
        if column in df_country.columns:
            df_country.boxplot(column=column, by='quarter')
            plt.title(f"Quarterly Box Plot for {column} in {country}")
            plt.xlabel("Quarter")
            plt.ylabel("Value")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f"{country}_{column}_boxplot.png")
            plt.show()
            plt.close()

            # Calculate quartiles
            q1 = df_country[column].quantile(0.25)
            q2 = df_country[column].median()
            q3 = df_country[column].quantile(0.75)
            print(f"{country} - {column} | Q1: {q1}, Median: {q2}, Q3: {q3}")