"""
Synthetic Network Traffic Dataset Generator
Creates realistic sample data for testing the classifier pipeline
"""

import pandas as pd
import numpy as np
from pathlib import Path

class SyntheticDataGenerator:
    """Generate synthetic network traffic data"""
    
    def __init__(self, n_samples=5000, random_state=42):
        self.n_samples = n_samples
        np.random.seed(random_state)
        
    def generate_normal_traffic(self, n):
        """Generate normal (benign) traffic samples"""
        return {
            'duration': np.random.exponential(scale=200, size=n),
            'protocol_type': np.random.choice(['tcp', 'udp'], n),
            'service': np.random.choice(['http', 'https', 'dns', 'ftp'], n),
            'flag': np.random.choice(['S0', 'S1', 'S2', 'S3'], n),
            'src_bytes': np.random.lognormal(mean=7, sigma=2, size=n),
            'dst_bytes': np.random.lognormal(mean=7, sigma=2, size=n),
            'land': np.zeros(n, dtype=int),
            'wrong_fragment': np.zeros(n, dtype=int),
            'urgent': np.zeros(n, dtype=int),
            'hot': np.zeros(n, dtype=int),
            'num_failed_logins': np.zeros(n, dtype=int),
            'logged_in': np.ones(n, dtype=int),
            'num_compromised': np.zeros(n, dtype=int),
            'root_shell': np.zeros(n, dtype=int),
            'su_attempted': np.zeros(n, dtype=int),
            'num_root': np.zeros(n, dtype=int),
            'num_file_creations': np.random.poisson(lam=0.5, size=n),
            'num_shells': np.zeros(n, dtype=int),
            'num_access_files': np.random.poisson(lam=0.5, size=n),
            'num_outbound_cmds': np.zeros(n, dtype=int),
            'is_host_login': np.zeros(n, dtype=int),
            'is_guest_login': np.zeros(n, dtype=int),
            'count': np.random.poisson(lam=5, size=n),
            'srv_count': np.random.poisson(lam=4, size=n),
            'serror_rate': np.random.uniform(0, 0.05, size=n),
            'srv_serror_rate': np.random.uniform(0, 0.05, size=n),
            'rerror_rate': np.random.uniform(0, 0.05, size=n),
            'srv_rerror_rate': np.random.uniform(0, 0.05, size=n),
            'same_srv_rate': np.random.uniform(0.8, 1.0, size=n),
            'same_ctry_rate': np.random.uniform(0.8, 1.0, size=n),
            'dst_host_count': np.random.poisson(lam=10, size=n),
            'dst_host_srv_count': np.random.poisson(lam=8, size=n),
            'dst_host_same_srv_rate': np.random.uniform(0.7, 1.0, size=n),
            'dst_host_diff_srv_rate': np.random.uniform(0, 0.3, size=n),
            'dst_host_same_src_port_rate': np.random.uniform(0.8, 1.0, size=n),
            'dst_host_srv_diff_host_rate': np.random.uniform(0, 0.1, size=n),
            'dst_host_serror_rate': np.random.uniform(0, 0.05, size=n),
            'dst_host_srv_serror_rate': np.random.uniform(0, 0.05, size=n),
            'dst_host_rerror_rate': np.random.uniform(0, 0.05, size=n),
            'dst_host_srv_rerror_rate': np.random.uniform(0, 0.05, size=n),
            'label': np.full(n, 'normal')
        }
    
    def generate_dos_traffic(self, n):
        """Generate DoS attack traffic"""
        return {
            'duration': np.random.exponential(scale=50, size=n),
            'protocol_type': np.full(n, 'tcp'),
            'service': np.random.choice(['http', 'https'], n),
            'flag': np.random.choice(['S0', 'S1'], n),
            'src_bytes': np.random.lognormal(mean=5, sigma=1, size=n),
            'dst_bytes': np.random.lognormal(mean=6, sigma=1, size=n),
            'land': np.zeros(n, dtype=int),
            'wrong_fragment': np.random.poisson(lam=0.3, size=n),
            'urgent': np.zeros(n, dtype=int),
            'hot': np.zeros(n, dtype=int),
            'num_failed_logins': np.zeros(n, dtype=int),
            'logged_in': np.zeros(n, dtype=int),
            'num_compromised': np.zeros(n, dtype=int),
            'root_shell': np.zeros(n, dtype=int),
            'su_attempted': np.zeros(n, dtype=int),
            'num_root': np.zeros(n, dtype=int),
            'num_file_creations': np.zeros(n, dtype=int),
            'num_shells': np.zeros(n, dtype=int),
            'num_access_files': np.zeros(n, dtype=int),
            'num_outbound_cmds': np.zeros(n, dtype=int),
            'is_host_login': np.zeros(n, dtype=int),
            'is_guest_login': np.zeros(n, dtype=int),
            'count': np.random.poisson(lam=50, size=n),  # Very high
            'srv_count': np.random.poisson(lam=40, size=n),
            'serror_rate': np.random.uniform(0.3, 0.8, size=n),
            'srv_serror_rate': np.random.uniform(0.3, 0.8, size=n),
            'rerror_rate': np.random.uniform(0.2, 0.6, size=n),
            'srv_rerror_rate': np.random.uniform(0.2, 0.6, size=n),
            'same_srv_rate': np.random.uniform(0.9, 1.0, size=n),
            'same_ctry_rate': np.random.uniform(0.8, 1.0, size=n),
            'dst_host_count': np.random.poisson(lam=100, size=n),  # Very high
            'dst_host_srv_count': np.random.poisson(lam=80, size=n),
            'dst_host_same_srv_rate': np.random.uniform(0.9, 1.0, size=n),
            'dst_host_diff_srv_rate': np.random.uniform(0, 0.1, size=n),
            'dst_host_same_src_port_rate': np.random.uniform(0.9, 1.0, size=n),
            'dst_host_srv_diff_host_rate': np.random.uniform(0, 0.05, size=n),
            'dst_host_serror_rate': np.random.uniform(0.3, 0.8, size=n),
            'dst_host_srv_serror_rate': np.random.uniform(0.3, 0.8, size=n),
            'dst_host_rerror_rate': np.random.uniform(0.2, 0.6, size=n),
            'dst_host_srv_rerror_rate': np.random.uniform(0.2, 0.6, size=n),
            'label': np.full(n, 'dos')
        }
    
    def generate_probe_traffic(self, n):
        """Generate Port Scan/Probe traffic"""
        return {
            'duration': np.random.exponential(scale=100, size=n),
            'protocol_type': np.random.choice(['tcp', 'udp'], n),
            'service': np.random.choice(['telnet', 'ssh', 'ftp'], n),
            'flag': np.random.choice(['S0', 'REJ'], n),
            'src_bytes': np.zeros(n, dtype=int),
            'dst_bytes': np.zeros(n, dtype=int),
            'land': np.zeros(n, dtype=int),
            'wrong_fragment': np.zeros(n, dtype=int),
            'urgent': np.zeros(n, dtype=int),
            'hot': np.zeros(n, dtype=int),
            'num_failed_logins': np.zeros(n, dtype=int),
            'logged_in': np.zeros(n, dtype=int),
            'num_compromised': np.zeros(n, dtype=int),
            'root_shell': np.zeros(n, dtype=int),
            'su_attempted': np.zeros(n, dtype=int),
            'num_root': np.zeros(n, dtype=int),
            'num_file_creations': np.zeros(n, dtype=int),
            'num_shells': np.zeros(n, dtype=int),
            'num_access_files': np.zeros(n, dtype=int),
            'num_outbound_cmds': np.zeros(n, dtype=int),
            'is_host_login': np.zeros(n, dtype=int),
            'is_guest_login': np.zeros(n, dtype=int),
            'count': np.random.poisson(lam=3, size=n),
            'srv_count': np.random.poisson(lam=2, size=n),
            'serror_rate': np.random.uniform(0.7, 1.0, size=n),  # High error rate
            'srv_serror_rate': np.random.uniform(0.7, 1.0, size=n),
            'rerror_rate': np.random.uniform(0.5, 0.9, size=n),
            'srv_rerror_rate': np.random.uniform(0.5, 0.9, size=n),
            'same_srv_rate': np.random.uniform(0, 0.5, size=n),
            'same_ctry_rate': np.random.uniform(0.5, 1.0, size=n),
            'dst_host_count': np.random.poisson(lam=20, size=n),
            'dst_host_srv_count': np.random.poisson(lam=15, size=n),
            'dst_host_same_srv_rate': np.random.uniform(0.3, 0.7, size=n),
            'dst_host_diff_srv_rate': np.random.uniform(0.3, 0.7, size=n),
            'dst_host_same_src_port_rate': np.random.uniform(0, 0.3, size=n),
            'dst_host_srv_diff_host_rate': np.random.uniform(0.5, 1.0, size=n),
            'dst_host_serror_rate': np.random.uniform(0.7, 1.0, size=n),
            'dst_host_srv_serror_rate': np.random.uniform(0.7, 1.0, size=n),
            'dst_host_rerror_rate': np.random.uniform(0.5, 0.9, size=n),
            'dst_host_srv_rerror_rate': np.random.uniform(0.5, 0.9, size=n),
            'label': np.full(n, 'probe')
        }
    
    def generate_r2l_traffic(self, n):
        """Generate Remote to Local (Brute Force) traffic"""
        return {
            'duration': np.random.exponential(scale=150, size=n),
            'protocol_type': np.full(n, 'tcp'),
            'service': np.random.choice(['telnet', 'ssh', 'ftp'], n),
            'flag': np.random.choice(['S0', 'S1', 'S2'], n),
            'src_bytes': np.random.lognormal(mean=6, sigma=1, size=n),
            'dst_bytes': np.random.lognormal(mean=5, sigma=1, size=n),
            'land': np.zeros(n, dtype=int),
            'wrong_fragment': np.zeros(n, dtype=int),
            'urgent': np.zeros(n, dtype=int),
            'hot': np.zeros(n, dtype=int),
            'num_failed_logins': np.random.poisson(lam=10, size=n),  # Many failed logins
            'logged_in': np.zeros(n, dtype=int),
            'num_compromised': np.zeros(n, dtype=int),
            'root_shell': np.zeros(n, dtype=int),
            'su_attempted': np.random.poisson(lam=2, size=n),
            'num_root': np.zeros(n, dtype=int),
            'num_file_creations': np.zeros(n, dtype=int),
            'num_shells': np.zeros(n, dtype=int),
            'num_access_files': np.zeros(n, dtype=int),
            'num_outbound_cmds': np.zeros(n, dtype=int),
            'is_host_login': np.zeros(n, dtype=int),
            'is_guest_login': np.zeros(n, dtype=int),
            'count': np.random.poisson(lam=8, size=n),
            'srv_count': np.random.poisson(lam=6, size=n),
            'serror_rate': np.random.uniform(0.1, 0.4, size=n),
            'srv_serror_rate': np.random.uniform(0.1, 0.4, size=n),
            'rerror_rate': np.random.uniform(0.05, 0.2, size=n),
            'srv_rerror_rate': np.random.uniform(0.05, 0.2, size=n),
            'same_srv_rate': np.random.uniform(0.6, 0.9, size=n),
            'same_ctry_rate': np.random.uniform(0.8, 1.0, size=n),
            'dst_host_count': np.random.poisson(lam=15, size=n),
            'dst_host_srv_count': np.random.poisson(lam=12, size=n),
            'dst_host_same_srv_rate': np.random.uniform(0.6, 0.9, size=n),
            'dst_host_diff_srv_rate': np.random.uniform(0.1, 0.4, size=n),
            'dst_host_same_src_port_rate': np.random.uniform(0.6, 0.9, size=n),
            'dst_host_srv_diff_host_rate': np.random.uniform(0.1, 0.3, size=n),
            'dst_host_serror_rate': np.random.uniform(0.05, 0.3, size=n),
            'dst_host_srv_serror_rate': np.random.uniform(0.05, 0.3, size=n),
            'dst_host_rerror_rate': np.random.uniform(0.05, 0.2, size=n),
            'dst_host_srv_rerror_rate': np.random.uniform(0.05, 0.2, size=n),
            'label': np.full(n, 'r2l')
        }
    
    def generate_u2r_traffic(self, n):
        """Generate User to Root (Privilege Escalation) traffic"""
        return {
            'duration': np.random.exponential(scale=80, size=n),
            'protocol_type': np.full(n, 'tcp'),
            'service': np.random.choice(['telnet', 'ssh'], n),
            'flag': np.random.choice(['S0', 'S1', 'S2', 'S3'], n),
            'src_bytes': np.random.lognormal(mean=6, sigma=1, size=n),
            'dst_bytes': np.random.lognormal(mean=5, sigma=1, size=n),
            'land': np.zeros(n, dtype=int),
            'wrong_fragment': np.zeros(n, dtype=int),
            'urgent': np.zeros(n, dtype=int),
            'hot': np.zeros(n, dtype=int),
            'num_failed_logins': np.random.poisson(lam=2, size=n),
            'logged_in': np.ones(n, dtype=int),
            'num_compromised': np.ones(n, dtype=int),  # Compromised
            'root_shell': np.ones(n, dtype=int),  # Root shell obtained
            'su_attempted': np.ones(n, dtype=int),
            'num_root': np.random.poisson(lam=5, size=n),
            'num_file_creations': np.random.poisson(lam=2, size=n),
            'num_shells': np.ones(n, dtype=int),
            'num_access_files': np.random.poisson(lam=3, size=n),
            'num_outbound_cmds': np.random.poisson(lam=2, size=n),
            'is_host_login': np.zeros(n, dtype=int),
            'is_guest_login': np.zeros(n, dtype=int),
            'count': np.random.poisson(lam=5, size=n),
            'srv_count': np.random.poisson(lam=4, size=n),
            'serror_rate': np.random.uniform(0, 0.1, size=n),
            'srv_serror_rate': np.random.uniform(0, 0.1, size=n),
            'rerror_rate': np.random.uniform(0, 0.05, size=n),
            'srv_rerror_rate': np.random.uniform(0, 0.05, size=n),
            'same_srv_rate': np.random.uniform(0.8, 1.0, size=n),
            'same_ctry_rate': np.random.uniform(0.8, 1.0, size=n),
            'dst_host_count': np.random.poisson(lam=8, size=n),
            'dst_host_srv_count': np.random.poisson(lam=6, size=n),
            'dst_host_same_srv_rate': np.random.uniform(0.8, 1.0, size=n),
            'dst_host_diff_srv_rate': np.random.uniform(0, 0.2, size=n),
            'dst_host_same_src_port_rate': np.random.uniform(0.8, 1.0, size=n),
            'dst_host_srv_diff_host_rate': np.random.uniform(0, 0.1, size=n),
            'dst_host_serror_rate': np.random.uniform(0, 0.1, size=n),
            'dst_host_srv_serror_rate': np.random.uniform(0, 0.1, size=n),
            'dst_host_rerror_rate': np.random.uniform(0, 0.05, size=n),
            'dst_host_srv_rerror_rate': np.random.uniform(0, 0.05, size=n),
            'label': np.full(n, 'u2r')
        }
    
    def generate_dataset(self):
        """Generate complete synthetic dataset"""
        print("\n🔧 Generating synthetic network traffic dataset...")
        
        # Generate different attack types
        samples_per_class = self.n_samples // 5
        
        print(f"  • Normal traffic: {samples_per_class}")
        normal = self.generate_normal_traffic(samples_per_class)
        
        print(f"  • DoS attacks: {samples_per_class}")
        dos = self.generate_dos_traffic(samples_per_class)
        
        print(f"  • Port Scans: {samples_per_class}")
        probe = self.generate_probe_traffic(samples_per_class)
        
        print(f"  • Brute Force (R2L): {samples_per_class}")
        r2l = self.generate_r2l_traffic(samples_per_class)
        
        print(f"  • Privilege Escalation (U2R): {samples_per_class}")
        u2r = self.generate_u2r_traffic(samples_per_class)
        
        # Combine all
        data = {}
        for key in normal.keys():
            data[key] = np.concatenate([
                normal[key], dos[key], probe[key], r2l[key], u2r[key]
            ])
        
        df = pd.DataFrame(data)
        
        # Shuffle
        df = df.sample(frac=1).reset_index(drop=True)
        
        print(f"\n✓ Generated {len(df)} samples")
        print(f"  Classes: {df['label'].value_counts().to_dict()}")
        
        return df
    
    def save_dataset(self, df, output_path='./dataset/raw/nsl_kdd_combined.csv'):
        """Save dataset to CSV"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"✓ Saved to: {output_path}")
        return output_path

def main():
    """Generate and save synthetic dataset"""
    print("\n" + "="*60)
    print("SYNTHETIC NETWORK TRAFFIC DATASET GENERATOR")
    print("="*60)
    
    generator = SyntheticDataGenerator(n_samples=5000)
    df = generator.generate_dataset()
    generator.save_dataset(df)
    
    print("\n✅ Dataset ready for training!")
    print("📊 Next: python model/train.py")

if __name__ == "__main__":
    main()
