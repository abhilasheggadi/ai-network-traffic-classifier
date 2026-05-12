"""
NSL-KDD Dataset Downloader
Downloads and prepares the NSL-KDD intrusion detection dataset
"""

import os
import urllib.request
import tarfile
import pandas as pd
from pathlib import Path

# Dataset URLs
DATASET_URL = "https://www.unb.ca/cic/datasets/nsl-kdd/NSL-KDD.zip"
BACKUP_URL = "http://nsl.cs.unb.ca/NSL-KDD/NSL-KDD.zip"

# Column names for NSL-KDD
COLUMNS = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
    'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
    'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
    'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
    'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'same_ctry_rate',
    'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
    'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
    'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
    'dst_host_srv_rerror_rate', 'label'
]

class NSLKDDDownloader:
    """Download and process NSL-KDD dataset"""
    
    def __init__(self, output_dir='./dataset/raw'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def download(self):
        """Download NSL-KDD dataset"""
        print("\n📥 NSL-KDD Dataset Downloader")
        print("="*60)
        
        # Try primary URL first
        urls = [DATASET_URL, BACKUP_URL]
        
        for url in urls:
            try:
                print(f"\n🔗 Downloading from: {url}")
                zip_path = self.output_dir / "NSL-KDD.zip"
                
                # Download with progress
                urllib.request.urlretrieve(url, zip_path)
                print(f"✓ Downloaded: {zip_path}")
                
                # Extract
                print("\n📦 Extracting files...")
                with tarfile.open(zip_path) as tar:
                    tar.extractall(self.output_dir)
                print("✓ Extracted successfully")
                
                return True
                
            except Exception as e:
                print(f"✗ Failed with this URL: {e}")
                continue
        
        print("\n⚠️  Download failed. Please download manually:")
        print(f"1. Visit: {urls[0]}")
        print(f"2. Extract to: {self.output_dir}")
        return False
    
    def prepare_data(self):
        """Find and prepare CSV files"""
        print("\n🔍 Looking for NSL-KDD data files...")
        
        # Look for KDD files
        possible_paths = [
            self.output_dir / "NSL-KDD" / "KDDTrain+.txt",
            self.output_dir / "NSL-KDD" / "KDDTest+.txt",
            self.output_dir / "KDDTrain+.txt",
            self.output_dir / "KDDTest+.txt",
        ]
        
        train_file = None
        test_file = None
        
        for path in possible_paths:
            if path.exists():
                if 'Train' in str(path):
                    train_file = path
                    print(f"✓ Found training data: {path}")
                elif 'Test' in str(path):
                    test_file = path
                    print(f"✓ Found test data: {path}")
        
        if not train_file:
            print("\n⚠️  Training file not found!")
            print(f"Expected one of:")
            for p in possible_paths:
                print(f"  - {p}")
            return None
        
        # Combine train + test into single CSV
        print("\n📊 Processing files...")
        dfs = []
        
        for file_path, name in [(train_file, 'training'), (test_file, 'test')]:
            if file_path and file_path.exists():
                print(f"  Reading {name}...")
                df = pd.read_csv(file_path, header=None, names=COLUMNS)
                dfs.append(df)
                print(f"    Loaded {len(df)} rows")
        
        if not dfs:
            return None
        
        # Combine
        combined_df = pd.concat(dfs, ignore_index=True)
        print(f"\n✓ Combined dataset: {len(combined_df)} total rows")
        
        # Clean label column
        combined_df['label'] = combined_df['label'].str.rstrip('.')
        
        # Save combined dataset
        output_path = self.output_dir / "nsl_kdd_combined.csv"
        combined_df.to_csv(output_path, index=False)
        print(f"✓ Saved combined dataset: {output_path}")
        
        return output_path
    
    def get_dataset_path(self):
        """Get path to cleaned dataset"""
        combined_path = self.output_dir / "nsl_kdd_combined.csv"
        if combined_path.exists():
            return combined_path
        
        # Try to find original files
        for possible_path in [
            self.output_dir / "NSL-KDD" / "KDDTrain+.txt",
            self.output_dir / "KDDTrain+.txt",
        ]:
            if possible_path.exists():
                return self.prepare_data()
        
        return None

def main():
    """Download dataset"""
    downloader = NSLKDDDownloader()
    
    # Try to download
    if downloader.download():
        downloader.prepare_data()
    
    # Check what we have
    dataset_path = downloader.get_dataset_path()
    if dataset_path and dataset_path.exists():
        print(f"\n✅ Dataset ready at: {dataset_path}")
        print(f"📊 Size: {dataset_path.stat().st_size / (1024*1024):.1f} MB")
        df = pd.read_csv(dataset_path)
        print(f"📈 Rows: {len(df)}")
        print(f"📋 Columns: {df.shape[1]}")
        print(f"\n🏷️  Labels: {df['label'].nunique()} classes")
        print(df['label'].value_counts())
    else:
        print("\n❌ Dataset not found. Please download manually.")

if __name__ == "__main__":
    main()
