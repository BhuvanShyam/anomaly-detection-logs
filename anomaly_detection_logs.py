import pandas as pd
from sklearn.ensemble import IsolationForest
from drain3 import TemplateMiner
import re

# Sample unstructured log lines (replace these with actual logs)
raw_logs = [
    "2025-07-17 10:01:23 INFO User John logged in from 10.0.0.1",
    "2025-07-17 10:02:45 INFO User Jane logged in from 10.0.0.2",
    "2025-07-17 10:03:12 WARNING Disk usage 90% on /dev/sda1",
    "2025-07-17 10:03:50 INFO User John logged out",
    "2025-07-17 10:04:21 ERROR Unauthorized login attempt from 192.168.1.22",
    "2025-07-17 10:05:12 INFO User Jane logged out",
    "2025-07-17 10:05:33 INFO User Mike logged in from 10.0.0.3",
    "2025-07-17 10:06:10 WARNING High memory usage detected",
    "2025-07-17 10:06:35 ERROR User John failed password attempt",
    "2025-07-17 10:07:12 CRITICAL System crash on node-03"
]

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