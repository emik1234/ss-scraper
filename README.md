# Automašīnu meklētājs

Mums kā studentiem ir nepieciešams atrasts lētas un lietotas automašīnas personīgai iegādei, tāpēc ir izveidots projekts par automašīnu meklētāju.

# Projekta uzdevums

Projekta uzdevums ir, balstoties uz lietotāja ievadītiem filtriem, vietnē www.ss.lv atrast atbilstošas mašīnas un apkopot tās Excel failā vieglai pārskatīšanai. Priekšrocība ir tāda, ka katru dienu var izmantot programmu un iegūt nepieciešamo informāciju, tādā veidā izvairoties no vairāku stundu pavadīšanas, manuāli meklējot.

# Izmantotās bibliotēkas
Programmā ir izmantotas bibliotēkas:

- Selenium web-scrapping nolūkos;
- Regex string tipa vērtību modificēšanai;
- Openpyxl darbībai ar Excel.

# Izmantotā datu struktūra

Projektā tiek izmantotas paštaisītas MaxHeap un MinHeap datu struktūras (un paštaisīta Car klase). Datu struktūras tiek izmantotas, lai uzglabātu no web-scrapping iegūto informāciju jau sakārtotā veidā (priority queue). Ja tiek izvēlēts gads vai motora tilpums kā galvenais parametrs savstarpēju Car objektu salīdzināšanai Heap struktūrā, tad
tiek veidota MaxHeap struktūra, kura pēc tam Excelī attiecīgi rāda jau ''filtrētu'' dilstošā secībā mašīnu atlasi (filtrēta pēc gada vai motora tilpuma). Ja izvēlēts nobraukums vai cena, tad veidojas MinHeap ar tādu pašu principu. 

# Programmatūras darbība

- Lietotājs uzsāk programmu, tam konsolē tiek pieprasīti dažādi secīgi filtri, kurus tas ievada, tajā skaitā parametrs, pēc kura tiek veidota Heap datu struktūra;
- Programma uzsāk web-scrapping, katru atrasto mašīnu saglabā kā klases Car instanci iekšā pēc filtriem izveidotājā MaxHeap vai MinHeap datu struktūrā;
- Programma beidz web-scrapping un uzsāk informācijas ievietošanu Excel failā, katru klases Car instanci izņemot no Heap struktūras ar .remove() metodi;
- Programma formatē Excel failu un visus datus tajā saglabā, tiek atgriezts .xlsx fails ar nosaukumu 'auto_dati.xlsx'

