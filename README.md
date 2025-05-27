# Tekstų Santraukų Įrankis
Tai žiniatinklio tipo įrankis, skirtas efektyviai generuoti glaustas santraukas anglų kalbos tekstams. Jis apjungia mašininio mokymosi modelius su patogia vartotojo sąsaja ir siūlo tiek ekstraktyvios, tiek abstraktyvios santraukos režimus.

# Įrankio architektūros aprašymas (praktikos ataskaita)
[Download Project Report (PDF)](Teksto santraukos įrankio architektūros aprašas.pdf)

# Funkcijos
* ✅ Pasirinkite santraukos tipą: ekstraktyvi (svarbiausių sakinių atranka) arba abstraktyvi (perfrazuota santrauka).
* ✅ Įveskite arba įklijuokite savo tekstą.
* ✅ Nustatykite pageidaujamą santraukos ilgį (10–50 % nuo pradinio teksto).
* ✅ Generuokite santrauką vienu mygtuko paspaudimu.
* ✅ Matykite žodžių skaičių palyginimą tarp pradinio ir santraukos teksto.
* ✅ Išsaugokite santraukas CSV formatu.
* ✅ Peržiūrėkite santraukų istoriją.
* ✅ Atsisiųskite ankstesnes santraukas atskirai arba visas kartu.
* ✅ Aiškūs klaidų pranešimai, jei įvyksta nesklandumai (pvz., per ilgas tekstas).

# Techninė informacija
- Backend: Python (Flask), MVC architektūra.
- Frontend: HTML, CSS, JavaScript.
- Duomenų bazė: SQLite (saugo santraukų istoriją, naudotojas yra nustatomas pagal cookies).
- Ekstraktyvi santrauka: vykdoma lokaliai.
- Abstraktyvi santrauka: prisijungiama prie HPC (aukšto našumo kompiuterių) klasterio per SSH ir naudojamas ProphetNet modelis. Šios santraukos sudarymas trunka iki minutės.

# Reikiami paketai
pip install -r requirements.txt

# Naudojimas
1. Atidarykite žiniatinklio sąsają.
2. Pasirinkite santraukos tipą (ekstraktyvi arba abstraktyvi).
3. Įveskite tekstą ir pasirinkite santraukos ilgį.
4. Paspauskite Sutrumpinti.
5. Peržiūrėkite sugeneruotą santrauką. Ją galima atsisiųsti.
6. Skiltyje Istorija peržiūrėkite ar atsisiųskite ankstesnes santraukas ar visą istoriją.
