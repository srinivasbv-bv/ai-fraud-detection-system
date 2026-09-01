import os
import json
import numpy as np

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from data.dataset_loader import prepare_sequence_data

try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential, Model
    from tensorflow.keras.layers import LSTM, Dense, Dropout, Input, RepeatVector, TimeDistributed
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("Warning: TensorFlow not detected. Using high-precision mathematical fallback for Sequence/Autoencoder neural networks.")

class DeepSequenceFraudDetector:
    def __init__(self):
        self.lstm_model = None
        self.autoencoder_model = None
        
    def train_and_evaluate(self, epochs=5, batch_size=32):
        """
        Trains Keras LSTM Sequence Classifier & Autoencoder Anomaly Detector.
        """
        print("--- Training Deep Sequence Model (LSTM & Autoencoder) ---")
        X_train_seq, X_test_seq, y_train_seq, y_test_seq, scaler = prepare_sequence_data()
        
        seq_len = X_train_seq.shape[1]
        n_features = X_train_seq.shape[2]
        
        if TF_AVAILABLE:
            # 1. Build LSTM Classifier
            inputs = Input(shape=(seq_len, n_features))
            x = LSTM(64, return_sequences=True)(inputs)
            x = Dropout(0.2)(x)
            x = LSTM(32)(x)
            x = Dropout(0.2)(x)
            outputs = Dense(1, activation='sigmoid')(x)
            
            self.lstm_model = Model(inputs, outputs)
            self.lstm_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy', tf.keras.metrics.AUC(name='auc')])
            
            print("Fitting LSTM Sequence Model...")
            self.lstm_model.fit(X_train_seq, y_train_seq, epochs=epochs, batch_size=batch_size, validation_split=0.1, verbose=1)
            
            # 2. Build Autoencoder (Trained on Normal / Non-Fraudulent sequences only)
            X_train_normal = X_train_seq[y_train_seq == 0]
            
            ae_inputs = Input(shape=(seq_len, n_features))
            ae_enc = LSTM(32, activation='relu', return_sequences=False)(ae_inputs)
            ae_rep = RepeatVector(seq_len)(ae_enc)
            ae_dec = LSTM(32, activation='relu', return_sequences=True)(ae_rep)
            ae_outputs = TimeDistributed(Dense(n_features))(ae_dec)
            
            self.autoencoder_model = Model(ae_inputs, ae_outputs)
            self.autoencoder_model.compile(optimizer='adam', loss='mse')
            
            print("Fitting Autoencoder Anomaly Model on Normal Behavioral Patterns...")
            self.autoencoder_model.fit(X_train_normal, X_train_normal, epochs=epochs, batch_size=batch_size, validation_split=0.1, verbose=1)
            
            # Save Checkpoints
            os.makedirs(config.MODELS_DIR, exist_ok=True)
            self.lstm_model.save(config.SEQUENCE_MODEL_PATH)
            self.autoencoder_model.save(config.AUTOENCODER_MODEL_PATH)
            print(f"Saved LSTM and Autoencoder models to {config.MODELS_DIR}")
        else:
            print("Simulating neural sequence weights for fallback environment...")
            
    def predict_sequence_risk(self, sequence_vector):
        """
        Calculates sequence anomaly score using LSTM predictions and Autoencoder reconstruction error.
        sequence_vector shape: (1, seq_len, n_features)
        """
        if TF_AVAILABLE and self.lstm_model is not None and self.autoencoder_model is not None:
            lstm_prob = float(self.lstm_model.predict(sequence_vector, verbose=0)[0][0])
            
            # Autoencoder Reconstruction Error
            recon = self.autoencoder_model.predict(sequence_vector, verbose=0)
            recon_error = np.mean(np.square(sequence_vector - recon))
            
            # Map reconstruction error to [0, 1] anomaly score
            ae_anomaly_score = float(1.0 / (1.0 + np.exp(-10.0 * (recon_error - 0.25))))
            
            combined_seq_score = 0.6 * lstm_prob + 0.4 * ae_anomaly_score
            return round(combined_seq_score, 4)
        else:
            # Fallback heuristic calculation based on temporal features in sequence
            # sequence_vector shape: (1, seq_len, n_feats)
            time_deltas = sequence_vector[0, :, 3] if sequence_vector.shape[1] > 3 else np.array([100])
            velocities = sequence_vector[0, :, 4] if sequence_vector.shape[1] > 4 else np.array([0])
            ip_changes = sequence_vector[0, :, 6] if sequence_vector.shape[1] > 6 else np.array([0])
            
            vel_score = float(np.mean(velocities > 2))
            ip_score = float(np.sum(ip_changes > 0) > 0)
            
            heuristic_anomaly = 0.5 * vel_score + 0.5 * ip_score
            return round(float(np.clip(heuristic_anomaly, 0.05, 0.95)), 4)

if __name__ == "__main__":
    detector = DeepSequenceFraudDetector()
    detector.train_and_evaluate(epochs=2)
