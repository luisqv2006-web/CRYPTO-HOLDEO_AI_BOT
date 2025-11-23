import json
import os

FILE = "positions.json"

def load_positions():
    if not os.path.exists(FILE):
        return {"positions": []}
    
    with open(FILE, "r") as f:
        return json.load(f)

def save_positions(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_position(symbol, entry_price, amount, tp1, tp2, tp3):
    data = load_positions()

    pos = {
        "symbol": symbol,
        "entry_price": entry_price,
        "amount": amount,
        "tp1": tp1,
        "tp2": tp2,
        "tp3": tp3,
        "status": "open",
        "tp1_hit": False,
        "tp2_hit": False,
        "tp3_hit": False
    }

    data["positions"].append(pos)
    save_positions(data)
    return pos

def get_open_positions():
    data = load_positions()
    return [p for p in data["positions"] if p["status"] == "open"]

def close_position(symbol):
    data = load_positions()
    for p in data["positions"]:
        if p["symbol"] == symbol:
            p["status"] = "closed"
    save_positions(data)

def mark_tp_hit(symbol, target):
    data = load_positions()
    for p in data["positions"]:
        if p["symbol"] == symbol:
            p[target] = True
    save_positions(data)
