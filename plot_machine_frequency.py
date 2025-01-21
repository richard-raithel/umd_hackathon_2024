import pandas as pd
import matplotlib.pyplot as plt

# Load the master test results CSV file
master_file_path = '/home/rraithel/drv1/pythonProjects/Fuch_UMD_Hackathon_2024/Fuch_UMD_Hackathon_2024/synthetic_files/reports_2024-09-26_00-39-17/answer_key.csv'
master_df = pd.read_csv(master_file_path)

# Strip leading or trailing spaces from the machine names
master_df['machine'] = master_df['machine'].str.strip()

# Calculate the frequency of each machine name
machine_name_counts = master_df['machine'].value_counts()

# Create a bar plot of the machine name frequency
plt.figure(figsize=(10, 6))
machine_name_counts.plot(kind='bar', color='skyblue')
plt.title('Frequency of Machine Names')
plt.xlabel('Machine Name')
plt.ylabel('Frequency')
plt.xticks(rotation=90)
plt.tight_layout()

# Save the plot as an image file
plot_file_path = 'machine_name_frequency.png'
plt.savefig(plot_file_path)
plt.show()

print(f"Bar plot saved as {plot_file_path}")
