#B1. Magic bytes: tipul real, nu estensia
def tip_real(cale):
        """Deschide un fisier binar si citeste primii octeti"""
        cap = open(cale, "rb").read(8)
        if cap.startswith(b"%PDF"):
                return "pdf"
        if cap.startswith(b"\x89PNG"):
                return "png"
        if cap.startswith(b"\xff\xd8"):
                return "jpeg"
        if cap.startswith(b"PK\x03\x04"):
                return  "zip/docx"
        return cap.hex()

print(tip_real("probe/foto.jpg"))

#B2. strings: textul citibil dintr-un binar
import re
date = open("probe/ascuns.png", "rb").read()
for m in re.findall(rb"[ -~]{4,}", date):
        print(m.decode())

#B3.Metadate EXIF si GPS din poza
from PIL import Image
from PIL.ExifTags import TAGS
exif = Image.open("probe/foto.jpg")._getexif() or {}
for id, val in exif.items():
	print(TAGS.get(id, id), "=", val)
gps = exif.get(34853, {})
north = gps.get(2)
east = gps.get(4)
lat = (((north[0] *3600) + north[1]*60)+ north[2])/60/60
long = (((east[0] * 3600) + east[1]*60) + east[2])/60/60
print("Latitudine :",float(lat) ,"Longitudine :",float(long))

#B4. File carving: scoți fișierul ascuns
import zipfile
date = open("probe/ascuns.png", "rb").read()
i = date.find(b"PK\x03\x04")
if i != -1:
  with open("gasit.zip", "wb") as f_out:
    f_out.write(date[i:])
  print("Arhiva extrasă de la octetul:", i)

with zipfile.ZipFile("gasit.zip","r") as zf:
	zf.extractall("extras_zip")
	print("COntinutul arhivei:", zf.namelist())

#B5. Ascunzi un mesaj prin LSB
from PIL import Image
img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.getdata())
mesaj = b"FLAG{ascuns_in_pixeli}\00"
biti = "".join(f"{x:08b}" for x in mesaj)
canale = [c for pixel in px for c in pixel]
for i, bit in enumerate(biti):
    canale[i] = (canale[i] & ~1) | int(bit)

px_nou = [tuple(canale[i:i + 3]) for i in range(0, len(canale), 3)]
img.putdata(px_nou)
img.save("stego.png")
print("mesaj ascuns in stego.png:", len(biti), "biti")

#B6. Dezvalui mesajul inapoi
px = list(Image.open("stego.png").convert("RGB").getdata())
biti = ""
for (r, g, b) in px:
    biti += str(r & 1) + str(g & 1) + str(b & 1)

octeti = bytearray()
for i in range(0, len(biti), 8):
	octet = int(biti[i:i + 8], 2)
	if octet == 0:
		break
	octeti.append(octet)

print("mesaj dezvaluit:",octeti.decode("utf-8", errors = "replace"))

