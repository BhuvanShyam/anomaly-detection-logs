import pandas as pd
from sklearn.ensemble import IsolationForest
from drain3 import TemplateMiner
import re
from datetime import datetime

# Read logs
with open("system.log", "r") as f:
    raw_logs = f.readlines()

template_miner = TemplateMiner()
parsed_logs = []

for line in raw_logs:
    line = line.strip()
    if not line:
        continue

    # Extract log level
    match_level = re.search(r'\b(INFO|ERROR|WARNING|CRITICAL)\b', line)
    log_level = match_level.group(1) if match_level else "UNKNOWN"

    # Extract timestamp and parse datetime
    match_time = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
    dt = datetime.strptime(match_time.group(1), "%Y-%m-%d %H:%M:%S") if match_time else None

    # Extract hour and day of week
    hour = dt.hour if dt else -1
    day_of_week = dt.weekday() if dt else -1

    # Extract template
    result = template_miner.add_log_message(line)
    if result is None:
        continue

    template = result["template_mined"]

    # Keyword flags
    failed_flag = 1 if re.search(r'failed', line, re.I) else 0
    unauthorized_flag = 1 if re.search(r'unauthorized', line, re.I) else 0
    crash_flag = 1 if re.search(r'crash', line, re.I) else 0

    parsed_logs.append({
        "log": line,
        "template": template,
        "log_level": log_level,
        "hour": hour,
        "day_of_week": day_of_week,
        "failed_flag": failed_flag,
        "unauthorized_flag": unauthorized_flag,
        "crash_flag": crash_flag
    })

df = pd.DataFrame(parsed_logs)

# Encode categorical features
df['template_id'] = pd.factorize(df['template'])[0]
df['log_level_id'] = pd.factorize(df['log_level'])[0]

# Features
features = ['template_id', 'log_level_id', 'hour', 'day_of_week',
            'failed_flag', 'unauthorized_flag', 'crash_flag']
X = df[features]

# Train Isolation Forest
model = IsolationForest(contamination=0.03, random_state=42)
df['model_pred'] = model.fit_predict(X)
df['model_pred'] = df['model_pred'].map({1: 'Normal', -1: 'Anomaly'})

# Apply heuristics on top of model predictions:
def final_label(row):
    if row['log_level'] == 'CRITICAL':
        return 'Anomaly'
    if row['unauthorized_flag'] == 1 or row['failed_flag'] == 1:
        return 'Anomaly'
    return row['model_pred']

df['final_label'] = df.apply(final_label, axis=1)

# Output to file
with open("detection_output.txt", "w") as f_out:
    f_out.write("=== Final Anomaly Detection Results ===\n\n")
    for _, row in df.iterrows():
        f_out.write(f"[{row['final_label']}] {row['log']}\n")
