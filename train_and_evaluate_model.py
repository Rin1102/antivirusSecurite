import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Load the dataset
dataset = pd.read_csv('feature_enhanced_bat_dataset.csv')

# Prepare the dataset (features and target)
X = dataset.drop(columns=['label'])
y = dataset['label']

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model using RandomForestClassifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train_scaled, y_train)

# Make predictions and evaluate the model
y_pred = model.predict(X_test_scaled)
print(classification_report(y_test, y_pred))

# Save the trained model and scaler
joblib.dump(model, 'batch_file_detector_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
