import json
import os
from datetime import datetime
from src.logger_config import setup_logger

logger = setup_logger("Stats")

DATA_FILE = os.path.join("data", "speed_runs.json")

def load_stats():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        logger.error("Failed to decode stats file. Returning empty list.")
        return []

def save_run(start_url, end_url, path, time_taken):
    stats = load_stats()
    
    run_data = {
        "date": datetime.now().isoformat(),
        "start_url": start_url,
        "end_url": end_url,
        "path": path,
        "steps": len(path),
        "time_taken_seconds": time_taken
    }
    
    stats.append(run_data)
    
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(stats, f, indent=4)
        logger.info("Run saved successfully.")
    except Exception as e:
        logger.error(f"Failed to save run: {e}")

def get_average_time():
    stats = load_stats()
    if not stats:
        return 0.0
    
    total_time = sum(run.get("time_taken_seconds", 0) for run in stats)
    return total_time / len(stats)
