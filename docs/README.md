## 1. Instalacija Python-a i Pip-a

Prvo, provjerite imate li instaliran **Python** i **Pip** (Python Package Installer), jer će vam biti potrebni za instalaciju Pipenv-a.

1. Otvorite **Command Prompt** (CMD) ili **PowerShell**.
2. Unesite sljedeće naredbe da provjerite verziju Pythona i pip-a:

   ```bash
   python --version
   pip --version
- Ako dobijete odgovore koji pokazuju verziju, Python i Pip su već instalirani na vašem računalu. Ako nije, preuzmite i instalirajte Python sa službene stranice: https://www.python.org/downloads/.
- Nakon što ste osigurali da je Python instaliran, možete instalirati Pipenv pomoću sljedeće naredbe:
  ```bash
  pip install pipenv

- Nakon što se instalacija završi, provjerite je li Pipenv uspješno instaliran pokretanjem:
  ```bash
  pipenv --version


## 2. Kloniranje projekta
Prvo, potrebno je klonirati repozitorij na svoje računalo. Ako koristite PyCharm, slijedite ove korake:


- Otvorite PyCharm
- Na početnom ekranu, kliknite na Get from Version Control.
- U URL polje unesite sljedeći URL: https://github.com/N0ksa/python_projekt.git
- Kliknite na Clone i čekajte da se projekt preuzme na vaše računalo.

Napomena:

Ako na svom kompjuteru nemate instaliran Git, nećete moći klonirati repozitorij i dobit ćete poruku o pogrešci prilikom pokušaja kloniranja.

Kako instalirati Git:

    Preuzmite i instalirajte Git sa službene stranice: https://git-scm.com/downloads.
    Slijedite upute za instalaciju, a nakon završetka, ponovno pokušajte klonirati repozitorij u PyCharm.


## 3. Postavljanje Python interpretatora u PyCharmu

-Otvorite PyCharm i učitajte klonirani projekt.
1. U Settings (ikona zubčanika u gornjem desnom kutu), idite na Project: [naziv vašeg projekta] > Python Interpreter.
2. Kliknite na Add Interpreter.
3. Odaberite Add Local Interpreter.
4. U Environment odaberite Pipenv.
5. Za Base Interpreter odaberite instalirani sustavni Python.
6. Kliknite na Install Packages from Pipfile i pričekajte da se svi paketi instaliraju. Ako instalacija ne uspije prvi put, pokušajte ponovno.

## 4. Instalacija Tesseract OCR

Za početak, potrebno je instalirati Tesseract OCR na svoj sustav.

- Preuzmite instalacijski paket za Tesseract OCR s [službene stranice](https://tesseract-ocr.github.io/tessdoc/Installation.html).
- Slijedite upute za instalaciju ovisno o operativnom sustavu koji koristite.

Ako prilikom instalacije ne odaberete zadani put za instalaciju, bit će potrebno ručno navesti put do `tesseract.exe` datoteke u konfiguracijskoj datoteci aplikacije.

## 5. Postavljanje putanje do Tesseract-a u `config.py`

* Ako niste koristili zadanu putanju za instalaciju Tesseract OCR-a, trebate specificirati ispravan put u konfiguracijskoj datoteci `config.py`.

* Trenutno je postavljena putanja na:  
`C:\Program Files\Tesseract-OCR\tesseract.exe`

* Ako je Tesseract instaliran na drugačijoj lokaciji, otvorite `config.py` i promijenite putanju do odgovarajuće lokacije

## 6. Skidanje trening podataka za jezike
* Zatim je potrebo skinuti trening podatke za one jezike koji su specificirani u projektu sa stranice https://tesseract-ocr.github.io/tessdoc/Data-Files i dodati ih u `C:\Program Files\Tesseract-OCR\tessdata`


## 7. Instalacija i postavljanje Poppler-a na Windows
Za pravilno korištenje aplikacije koja obrađuje PDF datoteke, potrebno je instalirati Poppler na svoj sustav.

* Preuzmite Poppler sa [službene GitHub stranice](https://github.com/oschwartz10612/poppler-windows/releases/tag/v24.08.0-0), raspakirajte ga i postavite u direktorij koji želite (npr. `C:\poppler-24.08.0`).
* Zatim dodajte taj direktorij u PATH:
  1. Desnim klikom na **This PC** ili **Computer** na desktopu ili u File Exploreru, odaberite **Properties**.
  2. Kliknite na **Advanced system settings** na lijevoj strani.
  3. U prozoru **System Properties**, kliknite na **Environment Variables**.
  4. U prozoru **Environment Variables**, pod "System variables", pronađite varijablu **Path** i kliknite **Edit**.
  5. Kliknite **New** i unesite putanju do `bin` mape unutar Poppler direktorija. Ako ste raspakirali Poppler u `C:\poppler-24.08.0`, unesite:
     ```
     C:\poppler-24.08.0\Library\bin
     ```
  6. Kliknite **OK** za spremanje svih promjena.