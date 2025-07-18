import pandas as pd
from sklearn.ensemble import IsolationForest
from drain3 import TemplateMiner
import re

# Sample unstructured log lines (replace these with actual logs)
# Read logs from file
with open("system.log", "r") as f:
    raw_logs = f.readlines()

# Drain3 parser setup
template_miner = TemplateMiner()

parsed_logs = []

for line in raw_logs:
    result = template_miner.add_log_message(line)
    if result is not None:
        parsed_logs.append({
            "log": line,
            "template": result["template_mined"]
        })

# Create DataFrame
df = pd.DataFrame(parsed_logs)


# Encode templates as numeric features
df['template_id'] = pd.factorize(df['template'])[0]

# Isolation Forest expects 2D features
X = df[['template_id']]

# Train Isolation Forest model
model = IsolationForest(contamination=0.2, random_state=42)
df['anomaly'] = model.fit_predict(X)

# Map results
df['anomaly'] = df['anomaly'].map({1: 'Normal', -1: 'Anomaly'})

# Display results
for i, row in df.iterrows():
    print(f"[{row['anomaly']}] {row['log']}")