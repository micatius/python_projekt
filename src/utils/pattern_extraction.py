import re

# Funkcija za pronalaženje imena, prezimena i datuma pregleda iz teksta
def find_name_surname_date(text):
    try:

        # Existing name and surname patterns
        name_surname_pattern_1 = re.compile(r'Prezime i ime:\s*([A-ZČĆŽŠĐ]+)\s*([A-ZČĆŽŠĐa-zčćžšđ]+)', re.IGNORECASE)
        name_surname_pattern_2 = re.compile(r'Prezime i ime, ime oca-majke:\s*(.*?)(,|\n|$)', re.IGNORECASE)
        name_surname_pattern_3 = re.compile(r'ime oca/majke:\s*(.*?)(,|\n|$)', re.IGNORECASE)  # Updated pattern
        name_surname_pattern_4 = re.compile(
            r'UVJERENJE O ZDRAVSTVENOJ SPOSOBNOSTI\s*ZA OBRAZOVANJE\s*\n\s*\n\s*([A-ZČĆŽŠĐ]+ [A-ZČĆŽŠĐa-zčćžšđ]+)',
            re.IGNORECASE)  # Existing pattern
        name_surname_pattern_5 = re.compile(r'LIJEČNIČKA SVJEDODŽBA\s*\n\s*(.*?)\n', re.IGNORECASE | re.DOTALL)
        # New pattern for name and surname after "IZVJEŠĆE O ZDRAVSTVENOM PREGLEDU"
        name_surname_pattern_6 = re.compile(r'IZVJEŠĆE O ZDRAVSTVENOM PREGLEDU\s*\n\s*(.*?)(,|\n)', re.IGNORECASE)

        # Existing date pattern
        date_pattern_1 = re.compile(r'ZAGREB,\s*([0-9]{2}\.[0-9]{2}\.[0-9]{4})', re.IGNORECASE)
        # New date pattern
        date_pattern_2 = re.compile(r'Datum pregleda:\s*([0-9]{2}\.[0-9]{2}\.[0-9]{4})', re.IGNORECASE)

        # Find name and surnamepip install Pillow
        name_surname_match_1 = name_surname_pattern_1.search(text)
        name_surname_match_2 = name_surname_pattern_2.search(text)
        name_surname_match_3 = name_surname_pattern_3.search(text)
        name_surname_match_4 = name_surname_pattern_4.search(text)
        name_surname_match_5 = name_surname_pattern_5.search(text)
        name_surname_match_6 = name_surname_pattern_6.search(text)

        # Find date
        date_match_1 = date_pattern_1.search(text)
        date_match_2 = date_pattern_2.search(text)

        if name_surname_match_1 and (date_match_1 or date_match_2):
            name = name_surname_match_1.group(2)
            surname = name_surname_match_1.group(1)
            date = date_match_1.group(1) if date_match_1 else date_match_2.group(1)
            return f"{surname} {name}", date
        elif name_surname_match_2 and (date_match_1 or date_match_2):
            name_surname = name_surname_match_2.group(1).strip()
            date = date_match_1.group(1) if date_match_1 else date_match_2.group(1)
            return name_surname, date
        elif name_surname_match_3 and (date_match_1 or date_match_2):
            name_surname = name_surname_match_3.group(1).strip()
            date = date_match_1.group(1) if date_match_1 else date_match_2.group(1)
            return name_surname, date
        elif name_surname_match_4 and (date_match_1 or date_match_2):
            name_surname = name_surname_match_4.group(1).strip()
            date = date_match_1.group(1) if date_match_1 else date_match_2.group(1)
            return name_surname, date
        elif name_surname_match_5 and (date_match_1 or date_match_2):
            name_surname = name_surname_match_5.group(1).strip()
            date = date_match_1.group(1) if date_match_1 else date_match_2.group(1)
            return name_surname, date
        elif name_surname_match_6 and (date_match_1 or date_match_2):
            name_surname = name_surname_match_6.group(1).strip()
            date = date_match_1.group(1) if date_match_1 else date_match_2.group(1)
            return name_surname, date
        else:
            return None, None
    except Exception as e:
        print(f"Error in find_name_surname_date: {e}")
        return None, None