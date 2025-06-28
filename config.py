ZONES = ["zone_1", "zone_2", "zone_3", "zone_4"]
WATER_USAGE = {zone: 0 for zone in ZONES}
MODE = "ia"  # ou "manuel"
OLIVE_AGES = {zone: 5 for zone in ZONES}  # Âge par défaut

def set_mode(new_mode):
    global MODE
    MODE = new_mode

def set_age(zone, age):
    OLIVE_AGES[zone] = age
