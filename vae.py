import pandas as pd
import numpy as np
import tensorflow as tf
import tf2onnx
from tensorflow import keras
from sklearn.model_selection import train_test_split
from tf2onnx import convert

# Load data from Excel
data = pd.read_excel('C:/Users/Sai krishna/OneDrive/Documents/dataset dcp.xlsx')

# Assuming you want to use columns 'Column1', 'Column2', 'Column3', 'Column4', 'Column5' as input features
selected_columns = ['AHU01CoolCoilDAT/temperature','AHU01EAT/temperature', 'AHU01OAT/temperature ', 'AHU01RAT/temperature ', 'AHU01SAT/temperature']
input_data = data[selected_columns].values

# Normalize the input data if needed
input_data = input_data.astype('float32')  # Convert to float32 for compatibility with VAE
input_data[np.isnan(input_data)] = np.nanmean(input_data)


# Reshape the input data into sequences
# Modified code to include all data samples
sequence_length = 1
sequences = []
for i in range(len(input_data) - sequence_length + 1):
    sequence = input_data[i:i + sequence_length]
    sequences.append(sequence)

# Check if there are any remaining data samples that don't fit into a full sequence
remaining_samples = len(input_data) % sequence_length

# If there are remaining samples, add them to the last sequence
if remaining_samples > 0:
    last_sequence = input_data[-sequence_length:]
    sequences.append(last_sequence)

# Convert sequences to a NumPy array
sequences = np.array(sequences)
# Print the shape of the sequences
print("Sequences shape:", sequences.shape)


# Split data into training and testing sets
X_train, X_test = train_test_split(sequences, test_size=0.2, random_state=42)

# Define the VAE model

# Define the encoder model
latent_dim = 2  # Adjust the latent space dimension
input_shape = (sequence_length, 5)  # Input shape: (sequence_length, num_features)

# Encoder
encoder_inputs = keras.layers.Input(shape=input_shape)
x = keras.layers.Flatten()(encoder_inputs)
x = keras.layers.Dense(128, activation='relu')(x)
z_mean = keras.layers.Dense(latent_dim, name='z_mean')(x)
z_log_var = keras.layers.Dense(latent_dim, name='z_log_var')(x)

# Reparameterization trick
def sampling(args):
    z_mean, z_log_var = args
    epsilon = tf.keras.backend.random_normal(shape=(tf.shape(z_mean)[0], latent_dim))
    return z_mean + tf.exp(0.5 * z_log_var) * epsilon

z = keras.layers.Lambda(sampling, output_shape=(latent_dim,))([z_mean, z_log_var])

# Define the decoder model
# Decoder
decoder_inputs = keras.layers.Input(shape=(latent_dim,))
x = keras.layers.Dense(128, activation='relu')(decoder_inputs)
x = keras.layers.Dense(sequence_length * 5, activation='sigmoid')(x)
decoded_outputs = keras.layers.Reshape((sequence_length, 5))(x)

# Define the VAE model
encoder = keras.models.Model(encoder_inputs, [z_mean, z_log_var, z], name='encoder')
decoder = keras.models.Model(decoder_inputs, decoded_outputs, name='decoder')
vae_outputs = decoder(encoder(encoder_inputs)[2])
vae = keras.models.Model(encoder_inputs, vae_outputs, name='vae')

model=vae
onnx_model, _ = tf2onnx.convert.from_keras(model)
onnx_path = onnx_path = r'C:\Users\Sai krishna\OneDrive\Desktop\dcp\your_model.onnx'

# Specify the path where you want to save the ONNX model
with open(onnx_path, "wb") as f:
    f.write(onnx_model.SerializeToString())


# Define loss function (customize as needed)
reconstruction_loss = keras.losses.mean_squared_error(encoder_inputs, vae_outputs)
reconstruction_loss *= input_shape[0]  # Adjust for sequence length
kl_loss = 1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var)
kl_loss = tf.reduce_mean(kl_loss) * -0.5
vae_loss = reconstruction_loss + kl_loss
vae.add_loss(vae_loss)
def mse_loss(y_true, y_pred):
    return tf.reduce_mean(tf.square(y_true - y_pred))

# In your VAE model, set the loss function to mse_loss:
vae.compile(optimizer='adam', loss=mse_loss)

optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)  # Adjust the learning rate as needed
vae.compile(optimizer='adam', loss=mse_loss)

# Compile the VAE model
vae.compile(optimizer='adam')

# Train the VAE
vae.fit(X_train, epochs=50, batch_size=32)

# Evaluate the model and set a threshold for anomaly detection
reconstructed_X_test = vae.predict(X_test)
reconstruction_errors = np.mean(np.square(X_test - reconstructed_X_test), axis=(1, 2))

# Set a threshold for anomaly detection
# Adjust this threshold as needed to define what you consider as "higher and abnormal"
threshold = 0.5

# Detect anomalies
anomalies = np.where(reconstruction_errors > threshold)[0]
# Sort anomalies by reconstruction errors in descending order
sorted_anomalies = anomalies[np.argsort(reconstruction_errors[anomalies])[::-1]]

# Print anomalies in descending order of reconstruction errors
print("Anomalies ordered by reconstruction errors (descending order):")
for anomaly_index in sorted_anomalies:
    print(f"Anomaly Index: {anomaly_index}, Reconstruction Error: {reconstruction_errors[anomaly_index]}")
    anomaly_data = X_test[anomaly_index]
    print("Anomaly Data:", anomaly_data)

if np.any(reconstruction_errors > threshold):
    print("Anomaly detected.")
    # You can also print the data associated with each anomaly if needed:
    print("Anomaly Data:", X_test[np.argmax(reconstruction_errors)])

# Check for NaN values in input_data
nan_values = np.isnan(input_data).sum()
print("NaN values in input_data:", nan_values)

# Check for infinite values
infinite_values = np.isinf(input_data).sum()
print("Infinite values in input_data:", infinite_values)
print(vae.summary())

if np.any(reconstruction_errors > threshold):
    print("Anomaly detected.")
    # You can also print the data associated with each anomaly if needed:
    print("Anomaly Data:", X_test[np.argmax(reconstruction_errors)])

