from config import CAPITAL_MAX

active_farm = None
rewards = 0.0

def enter_farm(farm):
    global active_farm
    active_farm = farm
    return f"✅ Entrando al farm {farm['pair']} con {CAPITAL_MAX} USD"

def farm_status():
    global rewards
    rewards += 0.12  # simulación de rewards
    return active_farm, rewards

def exit_farm():
    global active_farm, rewards
    active_farm = None
    rewards = 0
    return "🚨 Posición cerrada y fondos seguros en la wallet"
