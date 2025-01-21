import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = '/home/rraithel/drv1/pythonProjects/Fuch_UMD_Hackathon_2024/Fuch_UMD_Hackathon_2024/synthetic_files/reports_2024-09-26_00-39-17/a_viscosity_dataset.csv'  # Replace with your file path if different
data = pd.read_csv(file_path)

# Strip leading or trailing spaces from column names and data
data['machine'] = data['machine'].str.strip()
data['ing_1'] = data['ing_1'].str.strip()
data['ing_2'] = data['ing_2'].str.strip()
data['ing_3'] = data['ing_3'].str.strip()
data['unit'] = data['unit'].str.strip()

# Combine ingredients into a single string to represent the product
data['product'] = data['ing_1']
data['product'] += data['ing_2'].apply(lambda x: f", {x}" if x else '')
data['product'] += data['ing_3'].apply(lambda x: f", {x}" if x else '')

# Calculate the average viscosity for each combined product representation
average_viscosity = data.groupby('product')['result'].mean().sort_values()

# Plotting the average viscosity for each product
plt.figure(figsize=(14, 8))
average_viscosity.plot(kind='bar', color='skyblue')
plt.title('Average Viscosity by Product')
plt.xlabel('Product')
plt.ylabel('Average Viscosity (cP)')
plt.xticks(rotation=90)
plt.tight_layout()

# Save the plot as an image
plot_file_path = 'average_viscosity_by_product.png'
plt.savefig(plot_file_path)
plt.show()

print(f"Plot saved as {plot_file_path}")
