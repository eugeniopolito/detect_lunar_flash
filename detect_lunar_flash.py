import glob
import math
import numpy as np
import cv2

MOON_SIZE = 1860
RADIUS_MOON_KM = 1737.4
IMAGES_PATH_DIR = "/app/images/"

"""
Calcola la scala (km/pixel)
"""
def compute_scale():
    pixel_size = 0
    while True:
        print("Inserisci la dimensione del pixel della camera (µm)")
        print("[ZWO: ASI 224 = 3.75, ASI 178 = 2.4, ASI 120 = 3.75, ASI 290 = 2.9]")
        print("[Player One: Neptune-C II = 2.9]")
        try:
            pixel_size = float(input("-->"))
        except ValueError:
            print(f"Mmm... la dimensione del pixel non sembra essere un numero valido")
            continue
        else:
            break
    while True:
        print("\nInserisci la focale nativa del telescopio (mm)")
        print("[1000, 2000, ...]")
        try:
            focal_length = int(input("-->"))
        except ValueError:
            print(f"Mmm... la focale non sembra essere un numero valido")
        else:
            break
    while True:
        print("\nInserisci il fattore di scala della lente di Barlow")
        print("[1 = Nessuna lente, 0.3, 0.5, 2, ...]")
        try:
            barlow_factor = float(input("-->"))
        except ValueError:
            print(f"Mmm... il fattore di scale non sembra essere un numero valido")
        else:
            break
    scale_km_per_pixel = ((206.265 * pixel_size / (focal_length * barlow_factor)) / MOON_SIZE) * (RADIUS_MOON_KM * 2)
    print(f"\nIl fattore di scala calcolato è [km/pixel]: {scale_km_per_pixel:.2f}\n")
    return scale_km_per_pixel

"""
Esegue i calcoli per cercare l'eventuale flash usando l'algoritmo Canny Edge Detector di OpenCV.
"""
def check_flashes():
    scale_km_per_pixel = compute_scale()

    filenames = [img for img in glob.glob(f"{IMAGES_PATH_DIR}*.png")]

    curr = 1
    for img_file in filenames:
        img = cv2.imread(img_file)
        frame = img.copy()
        hh, ww = img.shape[:2]

        img = img[0:hh, 0:ww - 2]

        # converte in scala di grigi l'immagine
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # filtro mediano
        median = cv2.medianBlur(gray, 3)

        # cerca l'eventuale cerchio
        canny = cv2.Canny(median, 100, 200)

        # prende le coordinate dell'eventuale e se maggiori di 0 abbiamo trovato un eventuale flash
        points = np.argwhere(canny > 0)

        # prende il cerchio più piccolo
        center, radius = cv2.minEnclosingCircle(points)

        # ok, se abbiamo un cerchio ed il raggio è maggiore di 0, abbiamo trovato un flash!!!
        if canny.any() > 0 and radius >=1:
            print(f"\n\n***ATTENZIONE: Probabile flash trovato in '{img_file}'!***\n\n")
            # disegna il cerchio
            result = frame.copy()
            x = int(center[1])
            y = int(center[0])
            rad = 2 * int(radius)
            cv2.circle(result, (x, y), rad, (255, 255, 0), 1)
            cv2.imwrite(f"{IMAGES_PATH_DIR}/flash_{curr}.png", result)
            curr += 1
            image_array = np.array(gray)
            threshold = 40  # Threshold per il contrasto usato per separare la luna dallo sfondo
            moon_mask = image_array > threshold
            coords = np.argwhere(moon_mask)
            center_y, center_x = coords.mean(axis=0)  # approssima il centro della luna

            # calcola le distanze relative (in km)
            dx = (x - center_x) * scale_km_per_pixel  # E-W
            dy = (center_y - y) * scale_km_per_pixel  # N-S

            # Latitudine (gradi)
            latitudine = math.asin(dy / RADIUS_MOON_KM)
            latitudine_deg = math.degrees(latitudine)

            # Longitudine (gradi)
            longitudine = math.atan2(dx, math.sqrt(RADIUS_MOON_KM ** 2 - dx ** 2 - dy ** 2))
            longitudine_deg = math.degrees(longitudine)

            # Stampa i risultati
            print(f"Punto più luminoso (pixel): ({x}, {y})")
            print(f"Centro stimato (pixel): ({center_x:.2f}, {center_y:.2f})")
            print(f"Raggio stimato [km]: {radius * scale_km_per_pixel:.2f}")
            print(f"Latitudine: {latitudine_deg:.2f}°N")
            print(f"Longitudine: {longitudine_deg:.2f}°E")

