import sys
import platform

def is_raspberry_pi():
    if platform.system() == "Darwin":
        return False
    try:
        with open("/proc/device-tree/model", "r") as model_file:
            model = model_file.read().lower()
        return "raspberry pi" in model
    except Exception:
        return False

if not is_raspberry_pi():
    import fake_rpi
    sys.modules["RPi"] = fake_rpi.RPi
    sys.modules["RPi.GPIO"] = fake_rpi.RPi.GPIO

