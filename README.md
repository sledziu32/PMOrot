# PMOrot - Biznesowy Tarot dla Zespołów Projektowych

Parodia wróżb tarota w ujęciu biznesowym, stworzona jako żart na 1 kwietnia dla zespołów PMO (Project Management Office).

## Opis

PMOrot to aplikacja Streamlit, która humorystycznie odwołuje się do tradycji wróżenia z kart tarota, ale w kontekście biznesowym i projektowym. Użytkownik zadaje pytanie dotyczące projektu, zespołu lub zasobów, a aplikacja losuje trzy karty z własnej talii biznesowej, udzielając "wróżby" dotyczącej:
- **TimeLine (Terminy)** - co mówi karta o harmonogramie i deadline'ach
- **Resources (Zasoby)** - co mówi karta o budżecie i zasobach finansowych
- **People (Zespół)** - co mówi karta o zespole i relacjach interpersonalnych

Każda karta ma dwie interpretacje: prostą i odwróconą, które są losowo wybierane.

## Charakterystyka

- **Wyłącznie na żart** - nie należy traktować wyników poważnie jako rzeczywistych wróżb
- **Humor sytuacyjny** - odnosi się do typowych sytuacji w zespołach projektowych
- **Biznesowa tali** - karty oparte są na klasycznej talii tarota, ale z opisami dostosowanymi do kontekstu korporacyjnego i projektowego
- **Trzy kategorie** - każda losowana karta odpowiada jednej z trzech kluczowych obszarów projektu

## Technologie

- [Streamlit](https://streamlit.io/) - framework do tworzenia aplikacji webowych w Pythonie
- [Pandas](https://pandas.pydata.org/) - biblioteka do analizy danych (do wczytania talii kart z CSV)

4. Aplikacja będzie dostępna pod adresem: [https://pmorot.streamlit.app/](https://pmorot.streamlit.app/)

## Struktura plików

- `app.py` - główna aplikacja Streamlit
- `pmorot.csv` - talii kart biznesowych z opisami
- `requirements.txt` - zależności Pythonowe
- `README.md` - ten plik

## O talii kart

Talia zawiera 78 kart podzielonych na:
- **Wielkie Arkana** (22 karty) - ważne życiowe lekcje i wydarzenia
- **Buławy (Ogień)** (16 kart) - energia, inicjatywa, rozwój kariery
- **Kielichy (Woda)** (16 kart) - emocje, relacje, intuicja
- **Miecze (Powietrze)** (16 kart) - intelekt, konflikt, komunikacja
- **Monety (Ziemia)** (16 kart) - materialność, finanse, praktyczność

Każda karta ma:
- Nazwę po polsku i angielsku
- Opis dla aspektu "prostej" pozycji
- Opis dla aspektu "odwróconej" pozycji
- Trzy rodzaje opisów:
  * Dotyczące terminów (Deadline)
  * Dotyczące budżetu/zasobów (Budget)
  * Dotyczące zespołu/relacji (Team)

## Oświadczenie

⚠️ **WAŻNE**: Ta aplikacja została stworzona wyłącznie w celach rozrywkowych. Nie należy jej używać jako podstawy do podejmowania rzeczywistych decyzji biznesowych. Wyniki są losowe i nie mają żadnej wartości_predykcyjnej.

---

*PMOrot - nawet najpoważniejsze projekty potrzebują odrobinę humoru.*
