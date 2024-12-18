import os
import joblib

# Load the trained model and scaler
model = joblib.load('batch_file_detector_model.pkl')
scaler = joblib.load('scaler.pkl')

# Directory to scan (modify this path to your desired directory)
directory_to_scan = 'C:/'

def scan_batch_files(directory):
    # Walk through all directories and files within the specified path
    for root, dirs, files in os.walk(directory):
        try:
            for file in files:
                if file.endswith('.bat'):  # Only process .bat files
                    file_path = os.path.join(root, file)
                    print(f"Scanning: {file_path}")
                    
                    # Open file with 'ignore' to handle encoding errors
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        script_content = f.read()
                        
                        # Extract features from the batch script
                        features = extract_features(script_content)
                        features_scaled = scaler.transform([features])
                        
                        # Predict whether the script is malicious or not
                        prediction = model.predict(features_scaled)
                        if prediction == 1:
                            print(f"Malicious file detected: {file_path}")
                        else:
                            print(f"Safe file: {file_path}")
        except PermissionError:
            # Skip folders that cannot be accessed
            print(f"Permission denied for folder: {root}")
            continue

def extract_features(script_content):
    # Extract the relevant features from the script content
    features = {
        'del': script_content.count('del'),
        'shutdown': script_content.count('shutdown'),
        'rd': script_content.count('rd'),
        'format': script_content.count('format'),
        'attrib': script_content.count('attrib'),
        'total_commands': len(script_content.splitlines()),
        'script_length': len(script_content),
        'has_critical_path': 1 if 'C:\\' in script_content else 0
    }
    return list(features.values())

# Scan the specified directory
scan_batch_files(directory_to_scan)
