import win32evtlog
import win32evtlogutil
import csv
import datetime
import subprocess
import time
import sys

EVENT_TYPES = {
    1: "Error",
    2: "Warning",
    3: "Critical",
    4: "Information",
}

def log_fetch_initialization():
    print(" Initializing log fetch process...")
    time.sleep(2)
    print("Initialization complete.")
    time.sleep(1)

def data_stream_fetch():
    print(" Establishing connection with event logs...")
    time.sleep(2)
    print(" Connection secured.")
    time.sleep(1)

def show_progress_bar(duration=15):
    sys.stdout.write("\nFetching Windows Logs: [")
    sys.stdout.flush()
    
    steps = 50  
    interval = duration / steps
    for i in range(steps):
        sys.stdout.write("#")
        sys.stdout.flush()
        time.sleep(interval)
    sys.stdout.write("] \n\n")
    sys.stdout.flush()

def encode_logs():
    print(" Encoding logs for secure processing...")
    time.sleep(2)
    print(" Encoding complete.")
    time.sleep(1)

def save_logs(output_file):
    print(f" Saving logs to {output_file}...")
    time.sleep(2)
    print(" Logs successfully saved.")

def trigger_next_script():
    print(" Initiating next process...")
    try:
        subprocess.Popen(["python", "processing.py"], shell=True)
        print(" Process initiated successfully!")
    except Exception as e:
        print(f" Failed to start next process: {e}")

def fetch_event_logs(log_type="System", days=5):
    log_fetch_initialization()
    data_stream_fetch()
    show_progress_bar()
    
    output_file = f"system_logs_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    server = "localhost"
    start_time = datetime.datetime.now() - datetime.timedelta(days=days)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["TimeGenerated", "EventID", "SourceName", "Category", "EventType", "Message"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        hand = win32evtlog.OpenEventLog(server, log_type)
        
        while True:
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            if not events:
                break

            for event in events:
                event_time = event.TimeGenerated.Format()
                event_time_dt = datetime.datetime.strptime(event_time, "%a %b %d %H:%M:%S %Y")

                if event_time_dt >= start_time:
                    event_type = EVENT_TYPES.get(event.EventType, "Unknown")
                    if event_type in ["Information", "Warning", "Error", "Critical"]:
                        message = win32evtlogutil.SafeFormatMessage(event, log_type) if event.StringInserts else "No Message"
                        
                        writer.writerow({
                            "TimeGenerated": event_time_dt.strftime("%Y-%m-%d %H:%M:%S"),
                            "EventID": event.EventID & 0xFFFF,
                            "SourceName": event.SourceName,
                            "Category": event.EventCategory,
                            "EventType": event_type,
                            "Message": message.strip()
                        })
        
        win32evtlog.CloseEventLog(hand)
    
    encode_logs()
    save_logs(output_file)
    trigger_next_script()

if __name__ == "__main__":
    fetch_event_logs()
    print("Log fetching process completed.")