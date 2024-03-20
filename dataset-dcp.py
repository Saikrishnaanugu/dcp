import pandas as pd
import numpy as np

# Load data from Excel
data = pd.read_excel('C:/Users/Sai krishna/OneDrive/Documents/dataset dcp.xlsx')

# Assuming you want to use columns 'Column1', 'Column2', 'Column3', 'Column4', 'Column5' as input features
selected_columns = ['AHU01CoolCoilDAT/temperature','AHU01EAT/temperature', 'AHU01OAT/temperature ', 'AHU01RAT/temperature ', 'AHU01SAT/temperature']
input_data = data[selected_columns].values

# Normalize the input data if needed
input_data = input_data.astype('float32')  # Convert to float32 for compatibility with VAE
# You can add additional preprocessing steps if necessary

# Define the sequence length (e.g., 10 for 10 time steps)
sequence_length = 10  # Replace with your desired sequence length

# Reshape the input data into sequences
sequence_length = 10  # Adjust the sequence length as needed
sequences = []
for i in range(len(input_data) - sequence_length + 1):
    sequence = input_data[i:i + sequence_length]
    sequences.append(sequence)

# Convert sequences to a NumPy array
sequences = np.array(sequences)

# Print the shape of the sequences
print("Sequences shape:", sequences.shape)

# Now, you can use 'sequences' for training and testing your VAE model for anomaly detection.



























