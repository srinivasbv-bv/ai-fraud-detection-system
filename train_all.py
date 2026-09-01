import os
import sys

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from data.generator import generate_synthetic_data
from models.supervised_model import SupervisedFraudClassifier
from models.sequence_model import DeepSequenceFraudDetector

def run_training_pipeline():
    print("=================================================================")
    print(" AI-POWERED FRAUD DETECTION SYSTEM: FULL MODEL TRAINING PIPELINE")
    print("=================================================================\n")
    
    # 1. Dataset Generation
    print("[STEP 1/3] Generating synthetic benchmark datasets (ULB & IEEE-CIS style)...")
    df = generate_synthetic_data(num_samples=15000)
    print(f"Dataset generated with {len(df)} transactions.\n")
    
    # 2. Supervised Classifier Training
    print("[STEP 2/3] Training Supervised Classifiers (Random Forest & XGBoost with SMOTE)...")
    supervised_clf = SupervisedFraudClassifier()
    eval_results = supervised_clf.train_and_evaluate()
    print(f"Supervised model training complete. Selected Model: {eval_results['primary_model']}\n")
    
    # 3. Deep Sequence Model Training
    print("[STEP 3/3] Training Deep Sequence Detector (LSTM & Autoencoder)...")
    seq_detector = DeepSequenceFraudDetector()
    seq_detector.train_and_evaluate(epochs=3)
    print("Deep sequence model training complete.\n")
    
    print("=================================================================")
    print(" TRAINING COMPLETE! All model checkpoints and metrics saved.")
    print("=================================================================")

if __name__ == "__main__":
    run_training_pipeline()
