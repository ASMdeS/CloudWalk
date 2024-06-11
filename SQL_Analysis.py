import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import zscore

# Connect to the database
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='giraffe'
)

# Query the data
query = "SELECT * FROM checkout_2;"
df = pd.read_sql(query, connection)

# Close the connection
connection.close()

# Calculate Z-scores for each column except 'time'
for column in df.columns[1:]:
    df[f'zscore_{column}'] = zscore(df[column])
    print(zscore(df[column]))

# Define a threshold for identifying anomalies (e.g., Z-score > 2 or < -2)
threshold = 1.5

# Identify anomalies
anomalies = df[
    (df.filter(like='zscore_') > threshold).any(axis=1) | (df.filter(like='zscore_') < -threshold).any(axis=1)]

# Plotting the data with anomalies highlighted
plt.figure(figsize=(14, 8))

for column in df.columns[1:6]:  # Only original columns without Z-scores
    plt.plot(df['time'], df[column], label=column)

for column in df.columns[1:6]:  # Highlight anomalies
    plt.scatter(anomalies['time'], anomalies[column], label=f'anomaly_{column}', s=100, edgecolor='red')

plt.xlabel('Time')
plt.ylabel('Values')
plt.title('Hourly Data with Anomalies')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Show plot
plt.show()

# Print anomalies for verification
print(anomalies)
