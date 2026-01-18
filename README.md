# LogLens – AI-Powered System Log Analysis

LogLens is an automated system log analysis tool that collects, cleans, and analyzes Windows Event Logs using Python and Retrieval-Augmented Generation (RAG). It enables interactive log querying, AI-generated summaries, and actionable recommendations using a locally hosted Large Language Model (LLaMA via Ollama).

---

## Features
- Automated Windows Event Log collection and CSV generation
- Severity-based filtering (Error, Warning, Critical)
- Duplicate log removal and rule-based preprocessing
- Retrieval of relevant log patterns using TF-IDF and cosine similarity
- AI-powered log summarization and interactive chat-based analysis
- Local LLM execution using Ollama (no cloud dependency)

---

## Technology Stack
- Python
- Pandas, NumPy
- Scikit-learn (TF-IDF, cosine similarity)
- Ollama (LLaMA 3.2)
- Tkinter (GUI)
- PowerShell (setup & automation)

---

## How It Works
1. Fetch system logs from Windows Event Viewer
2. Preprocess and clean logs
3. Retrieve relevant log patterns using classical NLP
4. Generate insights and explanations using an LLM
5. Enable interactive querying via chat interface

---

## Use Cases
- System monitoring and troubleshooting
- DevOps and SRE log analysis
- Root cause investigation
- Learning and experimentation with RAG-based systems

---

## Note
This project focuses on log understanding and explanation rather than traditional anomaly detection or classification models.

