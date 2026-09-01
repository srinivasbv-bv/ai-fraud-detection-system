import os
import json
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.metrics import (
    precision_score, recall_score, f1_score, roc_auc_score,
    average_precision_score, confusion_matrix, precision_recall_curve, roc_curve
)

try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("Notice: XGBoost library not installed in current environment. Using sklearn HistGradientBoostingClassifier as high-performance ensemble model.")

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from data.dataset_loader import load_and_preprocess_tabular

class SupervisedFraudClassifier:
    def __init__(self):
        self.model = None
        self.rf_model = None
        self.xgb_model = None
        
    def train_and_evaluate(self):
        """
        Trains Random Forest & Gradient Boosting classifiers with SMOTE balanced data,
        evaluates metrics (Precision, Recall, F1, AUC-PR), and saves the best model.
        """
        print("--- Training Supervised Models (Random Forest & Gradient Boosting) ---")
        X_train_res, X_test, y_train_res, y_test, df_full = load_and_preprocess_tabular(apply_smote=True)
        
        # 1. Random Forest Classifier
        print("Training Random Forest Classifier...")
        self.rf_model = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
        self.rf_model.fit(X_train_res, y_train_res)
        rf_preds_prob = self.rf_model.predict_proba(X_test)[:, 1]
        
        # 2. XGBoost or HistGradientBoosting Classifier
        if XGBOOST_AVAILABLE:
            print("Training XGBoost Classifier...")
            self.xgb_model = XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.08, random_state=42, eval_metric='logloss')
        else:
            print("Training HistGradientBoosting Classifier...")
            self.xgb_model = HistGradientBoostingClassifier(max_iter=100, max_depth=8, learning_rate=0.08, random_state=42)
            
        self.xgb_model.fit(X_train_res, y_train_res)
        xgb_preds_prob = self.xgb_model.predict_proba(X_test)[:, 1]
        
        # Evaluate Gradient Boosting
        xgb_preds_binary = (xgb_preds_prob >= 0.5).astype(int)
        model_label = "XGBoost" if XGBOOST_AVAILABLE else "HistGradientBoosting"
        metrics_xgb = self._calculate_metrics(model_label, y_test, xgb_preds_prob, xgb_preds_binary)
        
        # Evaluate Random Forest
        rf_preds_binary = (rf_preds_prob >= 0.5).astype(int)
        metrics_rf = self._calculate_metrics("Random Forest", y_test, rf_preds_prob, rf_preds_binary)
        
        # Pick the best model based on F1-Score / AUC-PR
        if metrics_xgb['auc_pr'] >= metrics_rf['auc_pr']:
            print(f"Selected {model_label} as primary Supervised Classifier.")
            self.model = self.xgb_model
            best_metrics = metrics_xgb
        else:
            print("Selected Random Forest as primary Supervised Classifier.")
            self.model = self.rf_model
            best_metrics = metrics_rf
            
        # Save Model Checkpoint
        os.makedirs(config.MODELS_DIR, exist_ok=True)
        joblib.dump(self.model, config.SUPERVISED_MODEL_PATH)
        print(f"Saved Supervised Model to {config.SUPERVISED_MODEL_PATH}")
        
        # Save Evaluation Metrics JSON
        evaluation_results = {
            "primary_model": best_metrics['model_name'],
            "gradient_boosting": metrics_xgb,
            "random_forest": metrics_rf
        }
        with open(config.METRICS_PATH, 'w') as f:
            json.dump(evaluation_results, f, indent=4)
        print(f"Saved evaluation metrics to {config.METRICS_PATH}")
        
        return evaluation_results

    def _calculate_metrics(self, model_name, y_true, y_prob, y_pred):
        cm = confusion_matrix(y_true, y_pred).tolist()
        precision = float(precision_score(y_true, y_pred, zero_division=0))
        recall = float(recall_score(y_true, y_pred, zero_division=0))
        f1 = float(f1_score(y_true, y_pred, zero_division=0))
        roc_auc = float(roc_auc_score(y_true, y_prob))
        auc_pr = float(average_precision_score(y_true, y_prob))
        
        precisions, recalls, _ = precision_recall_curve(y_true, y_prob)
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        
        return {
            "model_name": model_name,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(roc_auc, 4),
            "auc_pr": round(auc_pr, 4),
            "confusion_matrix": cm,
            "pr_curve": {"precision": precisions[::20].tolist(), "recall": recalls[::20].tolist()},
            "roc_curve": {"fpr": fpr[::20].tolist(), "tpr": tpr[::20].tolist()}
        }

    def predict_risk(self, feature_vector):
        """
        Predicts raw fraud probability score [0.0, 1.0] for a feature vector.
        """
        if self.model is None:
            if os.path.exists(config.SUPERVISED_MODEL_PATH):
                self.model = joblib.load(config.SUPERVISED_MODEL_PATH)
            else:
                self.train_and_evaluate()
                
        prob = self.model.predict_proba(feature_vector)[:, 1]
        return float(prob[0])

if __name__ == "__main__":
    clf = SupervisedFraudClassifier()
    clf.train_and_evaluate()
