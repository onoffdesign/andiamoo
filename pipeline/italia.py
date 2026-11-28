"""Province italiane per l'area "tutta Italia": sigla -> (provincia, capoluogo, regione), nell'ordine di priorita'
della ricerca (ops/espansione.md: prima il Veneto, poi le regioni confinanti, poi Nord, Centro, Sud e isole).
I comuni e i loro centri sono in config/comuni.csv."""
from __future__ import annotations

_RAW = """
TV Treviso|Treviso|Veneto; PD Padova|Padova|Veneto; VR Verona|Verona|Veneto; VI Vicenza|Vicenza|Veneto;
VE Venezia|Venezia|Veneto; RO Rovigo|Rovigo|Veneto; BL Belluno|Belluno|Veneto;
UD Udine|Udine|Friuli-Venezia Giulia; PN Pordenone|Pordenone|Friuli-Venezia Giulia;
TS Trieste|Trieste|Friuli-Venezia Giulia; GO Gorizia|Gorizia|Friuli-Venezia Giulia;
TN Trento|Trento|Trentino-Alto Adige; BZ Bolzano|Bolzano|Trentino-Alto Adige;
MI Milano|Milano|Lombardia; BS Brescia|Brescia|Lombardia; BG Bergamo|Bergamo|Lombardia;
MB Monza e Brianza|Monza|Lombardia; VA Varese|Varese|Lombardia; CO Como|Como|Lombardia; PV Pavia|Pavia|Lombardia;
MN Mantova|Mantova|Lombardia; CR Cremona|Cremona|Lombardia; LC Lecco|Lecco|Lombardia; LO Lodi|Lodi|Lombardia;
SO Sondrio|Sondrio|Lombardia;
BO Bologna|Bologna|Emilia-Romagna; MO Modena|Modena|Emilia-Romagna; RE Reggio Emilia|Reggio nell'Emilia|Emilia-Romagna;
PR Parma|Parma|Emilia-Romagna; FC Forli'-Cesena|Forlì|Emilia-Romagna; RA Ravenna|Ravenna|Emilia-Romagna;
FE Ferrara|Ferrara|Emilia-Romagna; RN Rimini|Rimini|Emilia-Romagna; PC Piacenza|Piacenza|Emilia-Romagna;
TO Torino|Torino|Piemonte; CN Cuneo|Cuneo|Piemonte; NO Novara|Novara|Piemonte; AL Alessandria|Alessandria|Piemonte;
AT Asti|Asti|Piemonte; BI Biella|Biella|Piemonte; VC Vercelli|Vercelli|Piemonte;
VB Verbano-Cusio-Ossola|Verbania|Piemonte;
GE Genova|Genova|Liguria; SV Savona|Savona|Liguria; SP La Spezia|La Spezia|Liguria; IM Imperia|Imperia|Liguria;
AO Aosta|Aosta|Valle d'Aosta;
FI Firenze|Firenze|Toscana; PI Pisa|Pisa|Toscana; LU Lucca|Lucca|Toscana; AR Arezzo|Arezzo|Toscana;
LI Livorno|Livorno|Toscana; SI Siena|Siena|Toscana; PT Pistoia|Pistoia|Toscana; PO Prato|Prato|Toscana;
GR Grosseto|Grosseto|Toscana; MS Massa-Carrara|Massa|Toscana;
AN Ancona|Ancona|Marche; PU Pesaro e Urbino|Pesaro|Marche; MC Macerata|Macerata|Marche;
AP Ascoli Piceno|Ascoli Piceno|Marche; FM Fermo|Fermo|Marche;
PG Perugia|Perugia|Umbria; TR Terni|Terni|Umbria;
RM Roma|Roma|Lazio; LT Latina|Latina|Lazio; FR Frosinone|Frosinone|Lazio; VT Viterbo|Viterbo|Lazio; RI Rieti|Rieti|Lazio;
PE Pescara|Pescara|Abruzzo; CH Chieti|Chieti|Abruzzo; TE Teramo|Teramo|Abruzzo; AQ L'Aquila|L'Aquila|Abruzzo;
CB Campobasso|Campobasso|Molise; IS Isernia|Isernia|Molise;
NA Napoli|Napoli|Campania; SA Salerno|Salerno|Campania; CE Caserta|Caserta|Campania; AV Avellino|Avellino|Campania;
BN Benevento|Benevento|Campania;
BA Bari|Bari|Puglia; LE Lecce|Lecce|Puglia; FG Foggia|Foggia|Puglia; TA Taranto|Taranto|Puglia;
BR Brindisi|Brindisi|Puglia; BT Barletta-Andria-Trani|Barletta|Puglia;
PZ Potenza|Potenza|Basilicata; MT Matera|Matera|Basilicata;
CS Cosenza|Cosenza|Calabria; RC Reggio Calabria|Reggio di Calabria|Calabria; CZ Catanzaro|Catanzaro|Calabria;
KR Crotone|Crotone|Calabria; VV Vibo Valentia|Vibo Valentia|Calabria;
PA Palermo|Palermo|Sicilia; CT Catania|Catania|Sicilia; ME Messina|Messina|Sicilia; AG Agrigento|Agrigento|Sicilia;
TP Trapani|Trapani|Sicilia; SR Siracusa|Siracusa|Sicilia; RG Ragusa|Ragusa|Sicilia;
CL Caltanissetta|Caltanissetta|Sicilia; EN Enna|Enna|Sicilia;
CA Cagliari|Cagliari|Sardegna; SS Sassari|Sassari|Sardegna; NU Nuoro|Nuoro|Sardegna; OR Oristano|Oristano|Sardegna;
SU Sud Sardegna|Carbonia|Sardegna
"""

PROVINCE: dict[str, dict] = {}
for _item in _RAW.replace("\n", " ").split(";"):
    _item = _item.strip()
    if _item:
        _sigla, _rest = _item.split(" ", 1)
        _nome, _capo, _reg = _rest.split("|")
        PROVINCE[_sigla] = {"sigla": _sigla, "provincia": _nome, "capoluogo": _capo, "regione": _reg}

ALL_WORDS = {"tutte", "italia", "tutta italia", "all"}


def all_italy(provinces) -> bool:
    return any(str(p).strip().lower() in ALL_WORDS for p in provinces or [])
