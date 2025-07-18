import pandas as pd
from sklearn.ensemble import IsolationForest
from drain3 import TemplateMiner
import re

# Read logs from file
with open("system.log", "r") as f:
    raw_logs = f.readlines()

# Initialize Drain3 template miner
template_miner = TemplateMiner()

parsed_logs = []

# Parse each log line using Drain3 and extract log level
for line in raw_logs:
    line = line.strip()  # Remove trailing newlines/spaces
    if not line:
        continue  # Skip empty lines

    # Extract log level (INFO, ERROR, WARNING, CRITICAL)
    match = re.search(r'\b(INFO|ERROR|WARNING|CRITICAL)\b', line)
    log_level = match.group(1) if match else "UNKNOWN"

    # Parse template using Drain3
    result = template_miner.add_log_message(line)
    if result is not None:
        parsed_logs.append({
            "log": line,
            "template": result["template_mined"],
            "log_level": log_level
        })

# Create DataFrame from parsed logs
df = pd.DataFrame(parsed_logs)

# Encode templates and log levels as numerical features
df['template_id'] = pd.factorize(df['template'])[0]
df['log_level_id'] = pd.factorize(df['log_level'])[0]

# Prepare input features for the model
X = df[['template_id', 'log_level_id']]

# Train Isolation Forest model with lower contamination to reduce false positives
model = IsolationForest(contamination=0.1, random_state=42)
df['anomaly'] = model.fit_predict(X)

# Map results to readable labels
df['anomaly'] = df['anomaly'].map({1: 'Normal', -1: 'Anomaly'})

# Display results
print("\n=== Anomaly Detection Results ===\n")
for i, row in df.iterrows():
    print(f"[{row['anomaly']}] {row['log']}")
