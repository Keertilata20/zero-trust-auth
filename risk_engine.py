import numpy as np

def calculate_risk(keystrokes, mouse):

    if not keystrokes or not mouse:
        return "Monitoring..."

    typing_variation = np.std(keystrokes)
    mouse_variation = np.std(mouse)

    score = 100

    score -= typing_variation * 0.5
    score -= mouse_variation * 10

    if score > 70:
        return "Trusted"
    elif score > 40:
        return "Monitor"
    else:
        return "Re-Verify Required"
