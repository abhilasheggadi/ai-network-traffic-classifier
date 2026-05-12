"""
Model Training Pipeline - NSL-KDD Dataset
Trains Random Forest classifier on network traffic data
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import joblib
import json
from datetime import datetime

class TrafficClassifier:
    """Train and evaluate traffic classifier"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.feature_names = None
        self.metrics = {}
        
    def load_dataset(self, csv_path):
        """Load dataset from CSV"""
        print(f"\n📂 Loading dataset: {csv_path}")
        
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Dataset not found: {csv_path}")
        
        df = pd.read_csv(csv_path)
        print(f"✓ Loaded {len(df)} rows, {df.shape[1]} columns")
        
        return df
    
    def prepare_features(self, df):
        """
        Prepare features for ML model
        Select relevant numeric features from NSL-KDD
        """
        print("\n🔧 Preparing features...")
        
        # Features to use (numeric columns from NSL-KDD)
        feature_cols = [
            'duration', 'src_bytes', 'dst_bytes', 'count', 'srv_count',
            'serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
            'same_srv_rate', 'dst_host_count', 'dst_host_srv_count'
        ]
        
        # Filter available columns
        available_features = [col for col in feature_cols if col in df.columns]
        print(f"✓ Using {len(available_features)} features: {', '.join(available_features)}")
        
        X = df[available_features].copy()
        
        # Handle missing values
        X = X.fillna(0)
        X = X.replace([np.inf, -np.inf], 0)
        
        # Get labels
        y = df['label']
        
        # Handle label encoding
        print(f"✓ Found {y.nunique()} traffic classes")
        print(f"  Classes: {y.unique()[:10]}")  # Show first 10
        
        self.feature_names = available_features
        return X, y
    
    def train(self, X, y, test_size=0.2, random_state=42):
        """Train Random Forest classifier"""
        print("\n🧠 Training model...")
        
        # Encode labels
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        
        print(f"✓ Encoded {len(self.label_encoder.classes_)} classes")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=test_size, random_state=random_state, stratify=y_encoded
        )
        
        print(f"✓ Train: {len(X_train)}, Test: {len(X_test)}")
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Random Forest
        print("⏳ Fitting Random Forest (this may take a minute)...")
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=30,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=random_state,
            n_jobs=-1,
            verbose=0
        )
        
        self.model.fit(X_train_scaled, y_train)
        print("✓ Model training completed")
        
        return X_test_scaled, y_test
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        print("\n📊 Evaluating model...")
        
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        self.metrics = {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'timestamp': datetime.now().isoformat(),
            'classes': list(self.label_encoder.classes_)
        }
        
        # Print results
        print(f"\n{'='*50}")
        print(f"{'MODEL PERFORMANCE':^50}")
        print(f"{'='*50}")
        print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1 Score:  {f1:.4f}")
        print(f"{'='*50}\n")
        
        # Classification report
        print("Detailed Classification Report:")
        print(classification_report(
            y_test, y_pred,
            target_names=self.label_encoder.classes_,
            zero_division=0
        ))
        
        return self.metrics
    
    def save_model(self, output_dir='./model/saved_models'):
        """Save trained model and preprocessing objects"""
        print(f"\n💾 Saving model...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Save model
        model_path = os.path.join(output_dir, 'traffic_classifier.pkl')
        joblib.dump(self.model, model_path)
        print(f"✓ Model: {model_path}")
        
        # Save scaler
        scaler_path = os.path.join(output_dir, 'scaler.pkl')
        joblib.dump(self.scaler, scaler_path)
        print(f"✓ Scaler: {scaler_path}")
        
        # Save label encoder
        encoder_path = os.path.join(output_dir, 'label_encoder.pkl')
        joblib.dump(self.label_encoder, encoder_path)
        print(f"✓ Label Encoder: {encoder_path}")
        
        # Save metadata
        metadata = {
            'features': self.feature_names,
            'classes': list(self.label_encoder.classes_),
            'metrics': self.metrics,
            'training_date': datetime.now().isoformat()
        }
        
        metadata_path = os.path.join(output_dir, 'metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✓ Metadata: {metadata_path}")
        
        print(f"\n✅ All files saved to: {output_dir}")

def main():
    """Main training pipeline"""
    print("\n" + "="*60)
    print("NSL-KDD TRAFFIC CLASSIFIER - TRAINING PIPELINE")
    print("="*60)
    
    # Dataset path
    dataset_path = './dataset/raw/nsl_kdd_combined.csv'
    
    # Check if dataset exists
    if not os.path.exists(dataset_path):
        print(f"\n❌ Dataset not found: {dataset_path}")
        print("\n📥 Download the dataset first:")
        print("   python dataset/download_nsl_kdd.py")
        sys.exit(1)
    
    # Initialize classifier
    classifier = TrafficClassifier()
    
    # Load dataset
    df = classifier.load_dataset(dataset_path)
    
    # Prepare features
    X, y = classifier.prepare_features(df)
    
    # Train model
    X_test_scaled, y_test = classifier.train(X, y)
    
    # Evaluate
    metrics = classifier.evaluate(X_test_scaled, y_test)
    
    # Save
    classifier.save_model()
    
    print("\n" + "="*60)
    print("✅ TRAINING COMPLETED SUCCESSFULLY")
    print("="*60)
    print(f"\n📈 Model Accuracy: {metrics['accuracy']*100:.2f}%")
    print(f"📊 Ready for API deployment")
    print(f"\n🚀 Next step: Create FastAPI backend")

if __name__ == "__main__":
    main()
