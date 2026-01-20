import sqlite3
import json
import datetime
import os

DB_PATH = "test_history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS test_runs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  timestamp TEXT, 
                  instruction TEXT, 
                  total_steps INTEGER, 
                  passed INTEGER, 
                  failed INTEGER, 
                  status TEXT,
                  report_json TEXT)''')
    conn.commit()
    conn.close()

def add_test_run(instruction, report):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    summary = report.get("summary", {})
    total = summary.get("total_steps", 0)
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    status = "PASS" if failed == 0 and total > 0 else "FAIL"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute("INSERT INTO test_runs (timestamp, instruction, total_steps, passed, failed, status, report_json) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (timestamp, instruction, total, passed, failed, status, json.dumps(report)))
    conn.commit()
    conn.close()

def get_all_test_runs():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT id, timestamp, instruction, total_steps, passed, failed, status FROM test_runs ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_test_run(run_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM test_runs WHERE id=?", (run_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def clear_history():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM test_runs")
    conn.commit()
    conn.close()
