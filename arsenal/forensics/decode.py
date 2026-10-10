#A1 Text si octeti: incalzirea
s = "Salut"
b = s.encode()
print(b, b[0])

print(b.hex())
print(bytes.fromhex(b.hex()))

#A2 Recunosti stratul dupa forma
import re
def ghici_strat(s):
	"""Ghiceste codarea unui sir dupa caracterele sale si le clasifica"""
	if "%" in s:
		return "url"
	if re.fullmatch(r"[0-9a-f]+", s) and len(s) % 2 ==0:
		return "hex"
	if re.fullmatch(r"[A-Za-z0-9+/=]+",s):
		return "base64"
	return "necunoscut"

#A3. Desfaci stratul recunoscut
import base64
from urllib.parse import unquote
def desfa(s):
	"""Decodeaza un sir dupa caracterele sale"""
	strat = ghici_strat(s)
	if strat == "base64":
		return strat, base64.b64decode(s)
	if strat == "hex":
		return strat, bytes.fromhex(s) 
	if strat == "url":
		return strat, unquote(s).encode()
	return strat, s.encode()

#A4. Straturi multiple, intr-o bucla
def citibil(b):
	"""True daca toti octetii sunt caracere imprimabile (32...126)"""
	return all(32 <= c < 127 for c in b)

val = "NTM1OTU3NTk="
for _ in range(8):
	strat, b = desfa(val)
	print(strat, b)
	if citibil(b):
		print("citibil:", b.decode())
		break
	try:
		val = b.decode()
	except UnicodeDecodeError:
		print("octeti care nu ssunt text:", b)
		break

#A5. Spargi un XOR cu cheie de un octet
date = open("probe/xor.bin", "rb").read()
for k in range(256):
	clar = bytes(b^k for b in date)
	if citibil(clar) and b"FLAG{" in clar:
		print("cheie:", k, clar.decode())

#A6. Spargi un hash prin dictionar
import hashlib
tinta =open("probe/hashuri.txt").readline().strip()
print(len(tinta))
for cuv in open("probe/wordlist.txt", encoding="latin1"):
	cuv = cuv.strip()
	if hashlib.md5(cuv.encode()).hexdigest() == tinta:
		print("gasit:", cuv)
		break

#A7. argparse, fisa JSON si test
import argparse, json
if __name__ == "__main__":
	p = argparse.ArgumentParser()
	p.add_argument("intrare")
	p.add_argument("--fisier", action = "store_true")
	a = p.parse_args()

	if a.fisier:
		val = open(a.intrare, "rb").read().decode().strip()
	else:
		val = a.intrare

	strat, rezultat = desfa(val)
	fisa = {"strat": strat, "rezultat": rezultat.decode(errors ="replace")}
	with open("arsenal/forensics/fisa.json", "w", encoding = "utf-8") as f:
		json.dump(fisa, f, indent = 2, ensure_ascii= False)
	print(fisa)



