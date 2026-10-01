import time

from datetime import datetime

from collections import deque

import math



CHECK_INTERVAL = 3

DESICCANT_LIFE = 45.0

WINDOW_SIZE = 3



freq_buffer = deque(maxlen=WINDOW_SIZE)

last_rh = None

sim_step = 0



def get_raw_frequency():

    global sim_step

    sim_step += 1

    wave = math.sin(sim_step * 0.3) * 2000.0

    freq = 11000.0 + wave

    return max(8000.0, freq)



def get_temperature():

    temp_wave = math.cos(sim_step * 0.2) * 8.0

    return round(26.0 + temp_wave, 2)



def calc_humidity(freq):

    capacitance = freq * 0.015

    rh = min(max(capacitance * 0.35, 0.0), 100.0)

    return rh



def check_trend(current_rh):

    global last_rh

    

    if last_rh is None:

        trend = "Stable"

    elif current_rh > last_rh + 0.5:

        trend = "Rapidly Rising"

    elif current_rh > last_rh + 0.1:

        trend = "Rising"

    elif current_rh < last_rh - 0.5:

        trend = "Rapidly Falling"

    elif current_rh < last_rh - 0.1:

        trend = "Falling"

    else:

        trend = "Stable"

        

    last_rh = current_rh

    return trend



def get_risk_level(rh, temp, health):

    if rh > 65.0 or temp > 33.0 or health < 50.0:

        return "CRITICAL DANGER"

    elif rh > 55.0 or temp > 28.0 or health < 75.0:

        return "Moderate"

    return "Low"



def give_advice(risk, trend):

    if risk == "CRITICAL DANGER":

        return "🚨 EMERGENCY: Conditions are bad! Move items and change the desiccant pack!"

    elif risk == "Moderate":

        if "Rising" in trend:

            return "⚠️ CAUTION: Humidity is creeping up. Keep an eye on it."

        return "ℹ️ NOTICE: Getting close to threshold limits."

    return "✅ Looking good. Conditions are stable."



def main():

    global DESICCANT_LIFE

    print("--- Starting Up Environmental Monitor ---")

    

    try:

        while True:

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            

            raw_freq = get_raw_frequency()

            temp = get_temperature()

            

            freq_buffer.append(raw_freq)

            smooth_freq = sum(freq_buffer) / len(freq_buffer)

            rh = calc_humidity(smooth_freq)

            

            trend = check_trend(rh)

            storage_status = "Suboptimal" if (rh > 60.0 or temp > 30.0) else "Optimal"

            

            usage = (rh * 0.002) if rh > 60.0 else (rh * 0.0005)

            DESICCANT_LIFE = max(0.0, DESICCANT_LIFE - usage)

            

            rh_pen = max(0.0, rh - 50.0) * 0.8

            temp_pen = max(0.0, temp - 25.0) * 1.0

            health_score = max(0.0, 100.0 - rh_pen - temp_pen + (DESICCANT_LIFE * 0.1))

            

            risk = get_risk_level(rh, temp, health_score)

            advice = give_advice(risk, trend)

            

            print(f"\n[{timestamp}]")

            print(f"  * Humidity:    {rh:.2f} %RH (Trend: {trend})")

            print(f"  * Temp:        {temp:.2f} °C")

            print(f"  * Status:      {storage_status}")

            print(f"  * Risk Level:  👉 {risk} 👈")

            print(f"  * Desiccant:   {DESICCANT_LIFE:.2f} %")

            print(f"  * Advice:      {advice}")

            print("-" * 65)

            

            time.sleep(CHECK_INTERVAL)

            

    except KeyboardInterrupt:

        print("\nStopped by user. Shutting down.")



if __name__ == "__main__":

    main()
