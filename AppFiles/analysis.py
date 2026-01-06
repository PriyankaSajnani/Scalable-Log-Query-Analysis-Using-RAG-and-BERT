# import csv
# import json
# import random
# import subprocess
# from tkinter import Tk, filedialog

 
# Tk().withdraw()
# file_path = filedialog.askopenfilename(
#     title="Select Log CSV File", filetypes=[("CSV Files", "*.csv")]
# )

# if not file_path:
#     print(" No file selected. Exiting.")
#     exit()
 
# logs_by_severity = {"Warning": [], "Error": [], "Critical": []}

# with open(file_path, newline='', encoding='utf-8') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         level = row.get("Level")
#         message = row.get("Message")
#         if level in logs_by_severity and message:
#             logs_by_severity[level].append({"Level": level, "Message": message})
 
# sampled_logs = {
#     level: random.sample(logs, min(2, len(logs)))
#     for level, logs in logs_by_severity.items()
# }
 
# print("\n===== SELECTED LOG ENTRIES (Level + Message) =====\n")
# for level, logs in sampled_logs.items():
#     print(f"\n--- {level.upper()} LOGS ---")
#     for i, log in enumerate(logs, 1):
#         print(f"{i}. {log['Message']}")

 
# def summarize_logs(level, logs):
#     prompt = f"""
# You are a system log analyst. Below are logs labeled as '{level}'.

# Please provide:
# 1. Detailed Analysis
# 2. Future Steps
# 3. Further Recommendations
# 4. Preventive Measures

# Logs:
# {json.dumps(logs, indent=2)}
# """
#     result = subprocess.run(
#         ["ollama", "run", "llama3.2"],
#         input=prompt,
#         text=True,
#         capture_output=True
#     )
#     return result.stdout.strip()

# print("\n===== SUMMARY REPORTS =====\n")
# for level, logs in sampled_logs.items():
#     if logs:
#         print(f"\n{level.upper()} SUMMARY:\n")
#         summary = summarize_logs(level, logs)
#         print(summary)
#     else:
#         print(f"\nNo logs available for {level}.")

 
# combined_logs = [log for logs in sampled_logs.values() for log in logs]

# if combined_logs:
#     input("\n✅ Summaries complete. Press Enter to launch interactive chat...\n")

#     intro_prompt = f"""
# 🔍 COPY-PASTE THIS INTO LLaMA CHAT ONCE IT OPENS 👇

# You are an AI assistant analyzing system logs.

# Here are recent logs:
# {json.dumps(combined_logs, indent=2)}

# Now begin an interactive chat. Wait for the user to ask questions. If the user types '/bye', end the session politely.
# """

# print("\nOpening LLaMA 3.2 Interactive Session...\n")
# print(intro_prompt)

# # Launch llama in interactive mode
# subprocess.Popen(["ollama", "run", "llama3.2"])

# print("\nPaste the above context into the chat to begin. Type /bye when you're done.")
# print("To stop the model manually later, use: `ollama stop llama3.2`")
# print("\n **To stop the model manually, run: `ollama stop llama3.2**" )
# print("\n **To free memory and space use this command :ollama stop all && taskkill /IM ollama.exe /F**" )

import csv
import json
import random
import subprocess
from tkinter import Tk, filedialog
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

corpus_logs = [
    "The Windows Update service entered the stopped state.",
    "Audit Failure: An account failed to log on. Subject: Security ID: NULL SID, Logon Type: 3.",
    "The system has rebooted without cleanly shutting down first. This error could be caused if the system stopped responding, crashed, or lost power unexpectedly.",
    "The Application Host Helper Service service terminated unexpectedly. It has done this 1 time(s).",
    "The driver \\\\Driver\\\\WudfRd failed to load for the device ACPI\\PNP0A0A\\2&daba3ff&0.",
    "The Windows Defender Antivirus Service terminated unexpectedly. It has done this 2 time(s).",
    "Process winlogon.exe attempted to access a token which it does not have permission to use.",
    "Event 4625: An account failed to log on. Failure Reason: Unknown user name or bad password.",
    "The server {1B1F472E-3221-4826-97DB-2C2324D389AE} did not register with DCOM within the required timeout.",
    "The system detected a possible attempt to compromise security. Please ensure that you can contact the server that authenticated you.",
    "An unexpected shutdown occurred at 9:47 PM due to a power failure.",
    "Windows failed to start due to a recent hardware or software change.",
    "The Group Policy Client service failed the logon. Access is denied.",
    "The application svchost.exe generated an application error: The memory could not be read.",
    "Volume Shadow Copy Service error: The process cannot access the file because it is being used by another process.",
    "The Software Protection service has stopped. It was prevented from communicating with Microsoft servers.",
    "The Kerberos client received a KRB_AP_ERR_MODIFIED error from the server.",
    "A time difference between the client and server prevented logon.",
    "The computer has rebooted from a bugcheck. The bugcheck was: 0x0000007E.",
    "The DNS Client service has detected changes in the network configuration."
]
 
vectorizer = TfidfVectorizer()
corpus_vectors = vectorizer.fit_transform(corpus_logs)

def get_top_chunks(query, top_n=3):
    try:
        query_vec = vectorizer.transform([query])
        sim_scores = cosine_similarity(query_vec, corpus_vectors).flatten()
        top_indices = np.argsort(sim_scores)[-top_n:][::-1]
        return [corpus_logs[i] for i in top_indices]
    except Exception as e:
        print(f"[!] Chunking Error: {e}")
        return []
 
chunk_map = {}
for idx, line in enumerate(corpus_logs):
    if "error" in line.lower() or "failure" in line.lower():
        chunk_map[f"chunk_{idx}"] = {"log": line, "severity": "High"}
    elif "warning" in line.lower():
        chunk_map[f"chunk_{idx}"] = {"log": line, "severity": "Medium"}
    else:
        chunk_map[f"chunk_{idx}"] = {"log": line, "severity": "Low"}

Tk().withdraw()
file_path = filedialog.askopenfilename(
    title="Select Log CSV File", filetypes=[("CSV Files", "*.csv")]
)

if not file_path:
    print(" No file selected. Exiting.")
    exit()

logs_by_severity = {"Warning": [], "Error": [], "Critical": []}

with open(file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        level = row.get("Level")
        message = row.get("Message")
        if level in logs_by_severity and message:
            logs_by_severity[level].append({"Level": level, "Message": message})

sampled_logs = {
    level: random.sample(logs, min(2, len(logs)))
    for level, logs in logs_by_severity.items()
}

print("\n===== SELECTED LOG ENTRIES =====\n")
for level, logs in sampled_logs.items():
    print(f"\n--- {level.upper()} LOGS ---")
    for i, log in enumerate(logs, 1):
        print(f"{i}. {log['Message']}")

def summarize_logs(level, logs):
    prompt = f"""
You are a system log analyst. Below are logs labeled as '{level}'.

Please provide:
1. Detailed Analysis
2. Future Steps
3. Further Recommendations
4. Preventive Measures

Logs:
{json.dumps(logs, indent=2)}
"""
    result = subprocess.run(
        ["ollama", "run", "llama3.2"],
        input=prompt,
        text=True,
        capture_output=True
    )
    return result.stdout.strip()

print("\n===== SUMMARY REPORTS =====\n")
for level, logs in sampled_logs.items():
    if logs:
        print(f"\n{level.upper()} SUMMARY:\n")
        summary = summarize_logs(level, logs)
        print(summary)
    else:
        print(f"\nNo logs available for {level}.")

combined_logs = [log for logs in sampled_logs.values() for log in logs]

if combined_logs:
    input("\nSummaries complete. Press Enter to launch interactive chat...\n")

    intro_prompt = f"""
 COPY-PASTE THIS INTO LLaMA CHAT ONCE IT OPENS 

You are an AI assistant analyzing system logs.

Here are recent logs:
{json.dumps(combined_logs, indent=2)}

Now begin an interactive chat. Wait for the user to ask questions. If the user types '/bye', end the session politely.
"""

print("\nOpening LLaMA 3.2 Interactive Session...\n")
print(intro_prompt)

subprocess.Popen(["ollama", "run", "llama3.2"])

print("\nPaste the above context into the chat to begin. Type /bye when you're done.")
print("To stop the model manually later, use: `ollama stop llama3.2`")
print("\n **To stop the model manually, run: `ollama stop llama3.2**" )
print("\n **To free memory and space use this command :ollama stop all && taskkill /IM ollama.exe /F**" )
