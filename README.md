# Aplikacija za automatsku obradu i organizaciju PDF dokumenata

Ova aplikacija omogućava automatsko skeniranje, organizaciju i preimenovanje PDF dokumenata temeljenih na prepoznatom tekstu unutar dokumenata.

## Glavne funkcionalnosti

### 1. **Automatsko preimenovanje PDF dokumenata**
- Aplikacija skenira tekst u PDF dokumentu i prepoznaje fraze poput "LIJEČNIČKA SVJEDODŽBA".
- Na temelju prepoznatog teksta, PDF dokument se automatski preimenuje u oblik: LIJEČNIČKA_SVJEDOŽBA - Ime_Prezime

### 2. **Organizacija dokumenata u direktorije**
- Na temelju prepoznatog tipa dokumenta, PDF dokument se automatski premješta u odgovarajući direktorij i poddirektorij.
Na primjer: Liječničke_svjedodžbe/Prezime/LIJEČNIČKA_SVJEDOŽBA - Ime_Prezime


### 3. **Prepoznavanje i ekstrakcija teksta iz slika ili PDF datoteka**
- Prepoznaje tekst sa slika ili PDF datoteka  i izdvaja ga za daljnju obradu u novu .txt datoteku.

### 4. **Pretvorba slika u skenirane PDF dokumente**
- Aplikacija omogućava pretvorbu slika (slike s dokumentima u sebi) u PDF format.
- Automatski prepoznaje dokument unutar slike, prilagođava perspektivu (ako je potrebno) i sprema rezultat u PDF format.

### 5. **Generiranje sažetka teksta iz tekstualne dadoteke**
- Aplikacija generira sažetak teksta na osnovnu tekstualne datoteke, i sprema ga u novu .txt datoteku.

## Tehnologije
Aplikacija koristi sljedeće biblioteke i alate:
- **Tkinter** – za izradu grafičkog sučelja.
- **Pytesseract** – za ekstrakciju teksta iz PDF-ova i slika (OCR).
- **Pillow** – za manipulaciju slikama.
- **OpenCV** – za prepoznavanje i prilagodbu perspektive slika te obradu vizualnih elemenata.
- **NumPy** – za efikasno rukovanje matricama i obavljanje matematičkih operacija potrebnih za obradu slika.
- **math** – za izvođenje matematičkih izračuna potrebnih pri transformacijama i prilagodbama slika.
- **pdf2image** – za konverziju PDF dokumenata u slike kako bi se omogućila obrada njihovog sadržaja.
- **Regularni izrazi** – za identifikaciju i prepoznavanje tipa dokumenta temeljenog na tekstu.
- **Hugging Face - Transformers** - služi kao high level API za korištenje modela poput BART.
- **PyTorch** - pruža brzu implementaciju za velik broj operacija poput množenja matrica koje zahtjeva model.
- **BART** - Facebookov transformer model koji služi za različite NLP zadatke poput prevođenja i kreiranja sažetka teksta

