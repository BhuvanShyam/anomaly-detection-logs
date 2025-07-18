
# 🚨 System Log Anomaly Detection using Machine Learning & Log Parsing

This project detects anomalies in unstructured system logs using a combination of log template mining (Drain3) and machine learning (Isolation Forest). It mimics real-time log analysis for identifying security breaches, crashes, and system malfunctions.

---

## 📁 Project Structure

```
├── system.log               # Raw input log file (1000 entries)
├── detection_output.txt     # Output file with anomaly detection results
├── anomaly_detection.py     # Main Python script
├── README.md                # Project documentation
└── requirements.txt         # Python dependencies
```

---

## 🔍 Problem Statement

Modern IT systems generate large volumes of unstructured log data, making it challenging to manually detect system failures or breaches. This project aims to:
- Automatically learn normal log patterns.
- Flag deviations as anomalies in real-time.
- Generate alerts for potential threats or performance issues.

---

## 🚀 Features

- ✅ Supports **unstructured logs** in varied formats.
- ✅ Uses **Drain3** for log template extraction.
- ✅ Implements **Isolation Forest** for unsupervised anomaly detection.
- ✅ Adds **heuristics** to enhance precision for keywords like "crash", "unauthorized", "failed".
- ✅ Outputs tagged logs (`Normal` or `Anomaly`) into a result file.

---

## 🛠️ Technologies Used

- `Python 3.8+`
- `Drain3` for log template mining
- `Scikit-learn` for anomaly detection (Isolation Forest)
- `pandas` for log processing
- `re` and `datetime` for parsing logs

---

## 📄 How It Works

1. Parses raw logs from `system.log`.
2. Extracts structured info: timestamp, log level, flags (e.g., failed, unauthorized).
3. Applies Drain3 to extract log templates.
4. Trains an **Isolation Forest** on encoded features.
5. Applies **heuristics** (e.g., if log level is CRITICAL → anomaly).
6. Writes the results to `detection_output.txt`.

---

## 🧪 Sample Log Format

```
2025-07-17 10:01:23 INFO User John logged in from 10.0.0.1
2025-07-17 10:03:12 WARNING Disk usage 90% on /dev/sda1
2025-07-17 10:07:12 CRITICAL System crash on node-03
```

---

## ✅ Output Example

```
[Normal] 2025-07-17 10:01:23 INFO User John logged in from 10.0.0.1
[Anomaly] 2025-07-17 10:07:12 CRITICAL System crash on node-03
```

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/BhuvanShyam/anomaly-detection-logs.git
cd Anomaly-detection

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Run the Detector

```bash
python anomaly_detection_logs
```

Results will be saved in:
- `detection_output.txt`

---

## 📌 Notes

- You can modify or extend heuristics to adapt to specific business cases.
- Adjust the `contamination` parameter in Isolation Forest for tuning sensitivity.

---
