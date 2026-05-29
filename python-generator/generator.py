import pandas as pd
import json
import time
import os
from datetime import datetime

LOG_FILE = "/logs/kpi_network.log"
INTERVAL = 2

def classify_rsrp(val):
    if val > -80: return "good"
    if val > -100: return "moderate"
    return "critical"

def classify_rscp(val):
    if val > -80: return "good"
    if val > -95: return "moderate"
    return "critical"

def load_4g_data():
    df = pd.read_excel("/data/DT1.xlsx")
    df.columns = ["Time","PCI","Band","RSRP","RSRQ","Throughput"]
    df["RSRP"] = pd.to_numeric(df["RSRP"], errors="coerce")
    df["RSRQ"] = pd.to_numeric(df["RSRQ"], errors="coerce")
    return df.dropna(subset=["RSRP"])

def load_3g_data():
    df = pd.read_csv("/data/DT2.csv", sep=";", on_bad_lines="skip")
    df.columns = ["Time","Band","Channel","SC","RSCP","EcNo","RSCP_det","SC_det"]
    df["RSCP"] = pd.to_numeric(df["RSCP"], errors="coerce")
    df["EcNo"] = pd.to_numeric(df["EcNo"], errors="coerce")
    return df.dropna(subset=["RSCP"])

def emit_log(entry):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def main():
    print("[*] Loading datasets...")
    df4g = load_4g_data()
    df3g = load_3g_data()
    print(f"[*] 4G samples: {len(df4g)} | 3G samples: {len(df3g)}")

    idx4g = 0
    idx3g = 0

    while True:
        ts = datetime.utcnow().isoformat() + "Z"

        row4g = df4g.iloc[idx4g % len(df4g)]
        rsrp = float(row4g["RSRP"])
        rsrq = float(row4g["RSRQ"]) if pd.notna(row4g["RSRQ"]) else None
        pci  = int(row4g["PCI"]) if pd.notna(row4g["PCI"]) else 0
        band = str(row4g["Band"]) if pd.notna(row4g["Band"]) else "unknown"

        log4g = {
            "timestamp": ts,
            "technology": "LTE",
            "band": band,
            "pci": pci,
            "rsrp_dbm": round(rsrp, 1),
            "rsrq_db": round(rsrq, 1) if rsrq else None,
            "rsrp_quality": classify_rsrp(rsrp),
            "anomaly": rsrp < -100,
            "alert_level": "CRITICAL" if rsrp < -100 else ("WARNING" if rsrp < -85 else "OK"),
            "data_source": "DT1"
        }
        emit_log(log4g)

        if idx3g % 2 == 0:
            row3g = df3g.iloc[(idx3g // 2) % len(df3g)]
            rscp = float(row3g["RSCP"])
            ecno = float(row3g["EcNo"]) if pd.notna(row3g["EcNo"]) else None

            log3g = {
                "timestamp": ts,
                "technology": "UMTS",
                "band": str(row3g["Band"]),
                "rscp_dbm": round(rscp, 1),
                "ecno_db": round(ecno, 1) if ecno else None,
                "rscp_quality": classify_rscp(rscp),
                "anomaly": rscp < -95,
                "alert_level": "CRITICAL" if rscp < -95 else ("WARNING" if rscp < -80 else "OK"),
                "data_source": "DT2"
            }
            emit_log(log3g)

        idx4g += 1
        idx3g += 1
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
