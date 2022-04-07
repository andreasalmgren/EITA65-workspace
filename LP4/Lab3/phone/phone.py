from datetime import datetime
import qrcode


# HÄMTA TIDEN
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

#GENERERA QR-KOD

img = qrcode.make(current_time)

img.save("sample.png")