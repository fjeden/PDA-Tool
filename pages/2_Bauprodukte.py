import streamlit as st
from Data.backend import DIN276klassifizierung
import Data.backend

def get_demontierbarkeit(verbindungsart: str) -> str:
            """
            Wandelt die Verbindungsart automatisch in die zugehörige Demontierbarkeit um,
            anhand der verschachtelten Logik aus der Excel-Formel.
            """
            mapping = {
                "Bitte wählen Sie einen Wert aus ..." :"",
                "Lose / Klickverbindung": "Optimiert",
                "Gesteckt / Geschraubt": "Verbessert",
                "Festverbaut (Rückbauaufwand: mittel; Schadensart: überwiegend zerstörungsfrei lösbar)": "Standard",
                "Festverbaut (Rückbauaufwand: hoch; Schadensart: reparable Schäden)": "Eingeschränkt",
                "Festverbaut (Rückbauaufwand: extrem aufwändig; Schadensart: irreparable Schäden)": "Problematisch",
                "Nicht bewertbar bzw. nicht demontagefähig": "Nicht bewertbar bzw. nicht demontagefähig"
            }
            # Wenn der gegebene Wert nicht in der Map liegt, liefern wir einen leeren String:
            return mapping.get(verbindungsart, "")
        

def dynamic_selectbox(
    label: str,
    official_list: list,
    current_value: str,
    key: str = None,
    help_text: str = "",
    accept_new_options: bool = True,
    toast_message: str = None
):
    """
    Zeigt eine Selectbox an, die folgende Speziallogik abbildet:

    1) Offizielle Liste (official_list) wird kopiert => local_list.
    2) Falls current_value nicht in official_list und nicht leer, wird er 
       an Index 0 eingefügt und Index=0 vorbelegt. Gleichzeitig optional ein Toast.
    3) Falls der Wert drinsteht, berechnen wir den Index mittels .index(...).
    4) Falls kein passender Wert gefunden wird, setzen wir Index=0.
    5) Wir geben das ausgewählte Element per st.selectbox zurück.

    Parameter:
    - label:       Label der Selectbox.
    - official_list:    Die ursprüngliche Referenzliste (z. B. Data.backend.Verbindungart_grob).
    - current_value:     Der bereits gespeicherte Wert, der angezeigt werden soll.
    - key:         Optionale Key für das Widget (z. B. "edit_verbindungsartgrob").
    - help_text:   Optionaler Hilfe-Text.
    - accept_new_options:  True/False, ob Freitexteingabe via Selectbox erlaubt ist.
    - toast_message:   String, der im st.toast ausgegeben wird, wenn wir einen
                       unbekannten Wert einfügen (kann auch None sein).

    Rückgabe:
    - Der von der Selectbox gewählte/neue Wert (String).
    """

    # Lokale Kopie anlegen
    local_list = official_list.copy()
    
    if current_value not in official_list and current_value != "":
        # Unbekannter Wert => vorne einfügen
        local_list.insert(0, current_value)
        idx = 0
        # Optionalen Toast ausgeben
        if toast_message:
            st.toast(toast_message)
    else:
        # Versuchen, Index zu finden
        try:
            idx = official_list.index(current_value)
        except ValueError:
            idx = 0  # Fallback

    return st.selectbox(
        label,
        options=local_list,
        accept_new_options=accept_new_options,
        index=idx,
        key=key,
        help=help_text
    )

def bauprodukte():
    st.set_page_config(page_title="Bauprodukte", page_icon="🧱")
    
    st.header("Bauprodukte erfassen")
    
    # Session State vorbereiten
    if "products" not in st.session_state:
        st.session_state["products"] = []
    
    # Zunächst definieren wir das Eingabeformular für ein Bauprodukt
    # weiter unten definieren wir dann noch ein Formular zur Modifikation von bereits definierten oder importierten Formularen
    st.subheader("Neues Bauprodukt anlegen")
    with st.form("AddProductForm", clear_on_submit=True):
        ## Ab hier PDA Stufe 1
        st.subheader("Aufzunehmende Daten pro Bauprodukte in Stufe 1", divider="gray")
        new_id = st.text_input("Produkt-ID", help="Inidvidueller Produktcode; Bspw. für ein Track & Trace des Bauproduktes bzw. der Produkte")
        new_betrachtungsebene = st.selectbox("Betrachtungsebene", options= Data.backend.Betrachtungsebene, accept_new_options= True, help= """
                                             Möglichen Wert aus Dropdown-Menü wählen. Falls kein passender Wert gegeben ist, dann eigene Werteingabe vornehmen. 
                                             Nachfolgend finden Sie weiterführende Erläuterungen sowie Beispiele.
                                             
                                             Die vorliegende Betrachtungsebene orientiert sich an der Definition eines Bauproduktes gemäß der MBO, welche wiederum an der EU-BauPVO orientiert ist.
                                             Das vorliegende Tool wurde grundlegend zur Verwendung im Kontext industrieller Bestandsgroßbauten erstellt. 
                                             Die Kategorien Bausatz sowie Produkt wurden zusammengefasst, da im vorliegenden Kontext oftmals keine Rückschlüsse auf Hersteller gezogen werden können. Ein Bausatz/Produkt könnte bspw. ein Fenster sein.
                                             Ein Baustoff könnte bspw. Klinker sein.
                                             Ein Bauteil könnte wiederum eine Stütze oder ein Unterzug sein.
                                             Als Anlage könnte bspw. ein Modulbauelement oder eine Fertiggarage gelten.""")
        new_bezeichnung = st.text_input("Bezeichnung", help="Beschreibung des vorliegenden Bauproduktes")
        new_verortung = st.text_input("Verortung",help = "3D-Modellbezug (BIM-Schnittstelle), GIS, Zeichnungsviewer, 2D-Zeichnung mit Koordinatenbezug, (markierter) Grundriss - mindestens Etage und Raumnummer; Relevant für Level(s) 2.2 Berichterstattung")
        
        new_klassifizierung = st.selectbox("Klassifizierung",options=DIN276klassifizierung, accept_new_options= True, help="Nach DIN 276. Möglichen Wert aus Dropdown-Menü wählen. Falls kein passender Wert gegeben ist, dann eigene Werteingabe vornehmen.")
        
        new_abfallschlüsselnummer = st.selectbox("Abfallschlüsselnummer",options=Data.backend.Abfallschlüsselnummer, accept_new_options= True, help="Möglichen Wert aus Dropdown-Menü wählen. Falls kein passender Wert gegeben ist, dann eigene Werteingabe vornehmen. Relevant sofern nach Level(s) 2.2 berichtet werden soll.")
        new_material = st.selectbox("Material", options=Data.backend.Materialien, accept_new_options= True, help="""Möglichen Wert aus Dropdown-Menü wählen. Falls kein passender Wert gegeben ist, dann eigene Werteingabe vornehmen. Aufgeführte Wertemöglichkeiten entnommen aus Level(s) 2.2.""")
        new_hersteller = st.text_input("Hersteller")
        new_variante = st.text_input("Variante / Fabrikat", help="Optionale Angabe - bspw. eines Produkttyps eines Herstellers oder Angabe eines Stahlträgerprofils")
        new_menge = st.number_input("Menge", format="%.2f", help = "Bitte nachfolgend Einheit definieren.")
        new_einheit = st.text_input("Einheit")
        new_umrechnungsfaktor = st.text_input("Level(s) 2.2 - Umrechnungsfaktor", help="Relevant sofern nach Level(s) 2.2 berichtet werden soll. Beispiel: Menge = 40 m³; Umrechnungsfaktor = 2400 kg/m³; Menge [kg] = 96000 kg")
        new_menge_kg = st.text_input("Level(s) 2.2 - Menge [kg]", help="Relevant sofern nach Level(s) 2.2 berichtet werden soll. Beispiel: Menge = 40 m³; Umrechnungsfaktor = 2400 kg/m³; Menge [kg] = 96000 kg")
        new_höhe = st.number_input("Höhe [mm]",format="%.0f")
        new_breite = st.number_input("Breite [mm]", format="%.0f")
        new_länge= st.number_input("Länge [mm]", format="%.0f")
        new_zugänglichkeit =st.selectbox("Zugänglichkeit", options=Data.backend.Zugänglichkeit,accept_new_options= True, help="""Information hinsichtlich der  Zugänglichkeit des Bauproduktes im Falle eines Rückbaus.
         Möglichen Wert aus Dropdown-Menü wählen. Falls kein passender Wert gegeben ist, dann eigene Werteingabe vornehmen. Bestehende Wertemöglichkeiten nach Madaster.""")
        new_verbindungsartgrob = st.selectbox("Verbindungsart (grobe Einschätzung)",options=Data.backend.Verbindungart_grob, accept_new_options=True, help= """Möglichen Wert aus Dropdown-Menü wählen. Falls kein passender Wert gegeben ist, dann eigene Werteingabe vornehmen.
                                          Bestehende Wertemöglichkeiten nach DGNB Gebäuderessourcenpass""")
        new_schadstoffverdacht = st.selectbox("Einschätzung hinsichtlich Schadstoffverdacht bzw. Level(s) 2.2 - Abfallart", options=Data.backend.Schadstoffverdacht, accept_new_options=False, help="Information hinsichtlich eines Schadstoffverdachtes bzw. der Abfallart. Relevant sofern nach Level(s) 2.2 berichtet werden soll. Info: Inertabfälle sind Massen, die weder chemisch noch biologisch reaktiv sind, noch sich auflösen oder verbrennen.")
        new_fotos = st.text_area("Fotos", help="Das vorliegende Tool unterstützt zum aktuellen Zeitpunkt keine Eingabe von Fotos. Sie können hier beispielsweise auf Fotos verweisen oder diese zusätzlich beschreiben. Es sollte hierbei genau beschrieben werden, was durch Fotos dargestellt werden soll: Gebrauchszustand, Materialqualität, Einbausituation, Verortung.")
        new_gebrauchszustand = st.text_area("Gebrauchszustand - Visuell", help="Bspw. Hinweise auf Korrosion, vorliegende Risse, Abplatzungen, Verformungen etc.")
        new_funktion = st.selectbox("Funktion des Bauprodukts in der baulichen Anlage", options=Data.backend.Bauprodukt_Funktion,accept_new_options=True, help="Information bzgl. der Funktion des Bauprodukts in der baulichen Anlage in Anlehnung an das Six Layers Modell nach [Brand](https://c2c-bau.org/10-planung/10-1-gebaeudebereiche/). Falls keine passende Wertemöglichkeit gegeben ist, Wert überschreiben.")
        new_anschlussnutzungspotenzial = st.selectbox("Potenzial für Anschlussnutzung", options=Data.backend.Anschlussnutzungspotenzial, accept_new_options=False, help="Initiale Einschätzung bzgl. des vorliegenden Potenzials zur Anschlussnutzung.")
        new_anschlussnutzungspotenzial_begründung = st.text_area("Begründung der Einschätzung")
        new_product_weitereinfosstufe1 = st.text_area("Weitere Informationen - Stufe 1")

        ## Ab hier PDA Stufe 2
        st.subheader("Aufzunehmende Daten pro Bauprodukte in Stufe 2", divider="gray")
        new_einbaujahr = st.text_input("Einbaujahr", help="Jahreszahl oder ungefährer Zeitraum falls nicht vorhanden")
        new_produktionsjahr = st.text_input("Produktionsjahr", help="Jahreszahl oder ungefährer Zeitraum falls nicht vorhanden")
        new_vorgeschichte = st.text_area("Vorgeschichte")
        new_brandeinwirkung = st.text_input("Brandeinwirkung")
        new_frost_tauwechsel = st.text_input("Frost-Tauwechsel")
        new_bestehendeunterlagen = st.text_area("Bestehende Unterlagen", help="z. B. CE-Kennzeichnungen, Ü-Kennzeichnungen, Typenschilder, Datenblätter oder Leistungs-/Konformitätserklärungen")
        new_spezifischeattribute = st.text_area("Spezifische Attribute zum Produkt", help="z. B. Datenblätter, Produktnormen oder Proben")
        new_fachgutachen = st.text_area("Fachgutachten (Baustoffanalyse, Werkstoffanalyse)", help="Basierend auf zerstörenden oder zerstörungsfreien Verfahren z. B. durch bestehende Daten (z. B. Datenblätter) oder Kernbohrungen und durch Prüfungen wie z. B. Tragfähigkeitsprüfungen oder Ermittlung des Verformungsverhaltens.")
        new_schadstoffgutachten = st.text_area("Schadstoffgutachten", help="Falls Verdacht und noch nicht in Stufe 1 geklärt, dann Abklärung mit Schadstoffgutachter.")
        new_verbindungsart = st.selectbox("Verbindungsart", options=Data.backend.Verbindungsart, accept_new_options=False, help="Wertmöglichkeiten nach DGNB Gebäuderessourcenpass bzw. DGNB ZI")
        new_demontierbarkeit = get_demontierbarkeit(new_verbindungsart)
        # Anzeigen der Demontierbarkeit
        st.text_input("Demontierbarkeit:", value=new_demontierbarkeit, disabled= True, placeholder="Tatsächlicher Wert wird erst nach dem Anlegen des Produkts ermittelt", help="Wertmöglichkeiten nach DGNB Gebäuderessourcenpass bzw. DGNB ZI; Wert ergibt sich aufbauend auf der gewählten Verbindungsart")
        
        new_potenzielleanschlussnutzung =st.selectbox("Potenzielle Anschlussnutzung", options=Data.backend.Potenzielle_Anschlussnutzung, accept_new_options= True, help="Multiple Werteeingabe möglich. Hierfür bitte einfach individuell eingeben.")

        new_empfohleneanschlussnutzung = st.selectbox("Level(s) 2.2 - Empfohlene Anschlussnutzung (Auditor)", options= Data.backend.levels_Anschlussnutzung, accept_new_options=False, help="Optionales Eingabefeld sofern nach Level(s) 2.2 berichtet werden soll.")
        new_wahrscheinlicheanschlussnutzung = st.selectbox("Level(s) 2.2 - Wahrscheinliche Anschlussnutzung (Waste Manager)", options= Data.backend.levels_Anschlussnutzung, accept_new_options=False, help="Optionales Eingabefeld sofern nach Level(s) 2.2 berichtet werden soll.")

        new_rückbaumaßnahme = st.selectbox("Level(s) 2.2 - Art der Rückbaumaßnahme", options= Data.backend.levels_Rückbaumaßnahme, accept_new_options=False, help="Optionales Eingabefeld sofern nach Level(s) 2.2 berichtet werden soll. Auswahl einer der fünf Hauptrückbautätigkeiten, die für das Berichtsformat nach Level(s) Indicator 2.2 definiert sind.")
        new_product_weitereinfosstufe2 = st.text_area("Weitere Informationen - Stufe 2")
          
        
        
        
        submitted = st.form_submit_button("Neues Bauprodukt hinzufügen")
        
        
        if submitted:
            if new_id.strip():
                new_product = {
                    "product_id": new_id,
                    "betrachtungsebene" : new_betrachtungsebene,
                    "bezeichnung" : new_bezeichnung,
                    "verortung" : new_verortung,
                    "klassifizierung" : new_klassifizierung,
                    "abfallschlüsselnummer" : new_abfallschlüsselnummer,
                    "material": new_material,
                    "hersteller" : new_hersteller,
                    "variante" : new_variante,
                    "menge" : new_menge,
                    "einheit" : new_einheit,
                    "umrechungsfaktor" : new_umrechnungsfaktor,
                    "menge_kg" : new_menge_kg,
                    "höhe" : new_höhe,
                    "breite" : new_breite,
                    "länge" : new_länge,
                    "zugänglichkeit" : new_zugänglichkeit,
                    "verbindungsartgrob" : new_verbindungsartgrob,
                    "schadstoffverdacht" : new_schadstoffverdacht,
                    "fotos" : new_fotos,
                    "gebrauchszustand" : new_gebrauchszustand,
                    "funktionbauprodukt" : new_funktion,
                    "anschlussnutzungspotenzial" : new_anschlussnutzungspotenzial,
                    "anschlussnutzungspotenzial_begründung" : new_anschlussnutzungspotenzial_begründung,
                    "product_weitereinfosstufe1" : new_product_weitereinfosstufe1,
                    
                    #### ab hier stufe 2
                    "product_einbaujahr" : new_einbaujahr,
                    "product_produktionsjahr" : new_produktionsjahr,
                    "vorgeschichte" : new_vorgeschichte,
                    "brandeinwirkung" : new_brandeinwirkung,
                    "frost_tauwechsel" : new_frost_tauwechsel,
                    "product_bestehende_unterlagen" : new_bestehendeunterlagen,
                    "product_spezifischeattribtue" : new_spezifischeattribute,
                    "fachgutachten" : new_fachgutachen,
                    "schadstoffgutachten" : new_schadstoffgutachten,
                    "verbindungsart" :new_verbindungsart,
                    "demontierbarkeit" :new_demontierbarkeit,
                    "potenzielle_anschlussnutzung" : new_potenzielleanschlussnutzung,
                    "empfohlene_anschlussnutzung" : new_empfohleneanschlussnutzung,
                    "wahrscheinliche_anschlussnutzung" : new_wahrscheinlicheanschlussnutzung,
                    "rückbaumaßnahmenart" : new_rückbaumaßnahme,                    
                    "product_weitereinfosstufe2" : new_product_weitereinfosstufe2
                }
                st.session_state["products"].append(new_product)
                st.success(f"Bauprodukt '{new_id}' erfolgreich hinzugefügt.")
            else:
                st.warning("Bitte mindestens die Produkt-ID angeben.")
    
    # Vorhandene Produkte bearbeiten oder löschen
    if st.session_state["products"]:
        st.subheader("Vorhandene Bauprodukte bearbeiten oder löschen")
        
        product_ids = [p["product_id"] for p in st.session_state["products"]]
        
        selected_idx = st.selectbox(
            "Wähle ein Bauprodukt zum Bearbeiten/Löschen:",
            options=range(len(product_ids)),
            format_func=lambda i: product_ids[i]
        )
        
        selected_product = st.session_state["products"][selected_idx]
        
        ########################################################################## Felder für die Bearbeitung - Keys, damit Änderungen direkt sichtbar bleiben
        # für jedes angelegte Attribut hier noch eine edit-Möglichkeit anlegen
        
        "Stufe 1:"
        
        edit_id = st.text_input(
            "Produkt-ID (Bearbeitung)",
            value=selected_product["product_id"],
            key="edit_id"
        )
        
        edit_betrachtungsebene = dynamic_selectbox(
                                    label="Betrachtungsebene",
                                    official_list=Data.backend.Betrachtungsebene,
                                    current_value=selected_product["betrachtungsebene"],
                                    key="edit_betrachtungsebene",
                                    help_text="""Möglichen Wert aus Dropdown-Menü wählen. Falls kein passender Wert gegeben ist, dann eigene Werteingabe vornehmen. Nachfolgend finden Sie weiterführende Erläuterungen sowie Beispiele.
                                                Die vorliegende Betrachtungsebene orientiert sich an der Definition eines Bauproduktes gemäß der MBO, welche wiederum an der EU-BauPVO orientiert ist.
                                                Das vorliegende Tool wurde grundlegend zur Verwendung im Kontext industrieller Bestandsgroßbauten erstellt. 
                                                Die Kategorien Bausatz sowie Produkt wurden zusammengefasst, da im vorliegenden Kontext oftmals keine Rückschlüsse auf Hersteller gezogen werden können. Ein Bausatz/Produkt könnte bspw. ein Fenster sein.
                                                Ein Baustoff könnte bspw. Klinker sein.
                                                Ein Bauteil könnte wiederum eine Stütze oder ein Unterzug sein.
                                                Als Anlage könnte bspw. ein Modulbauelement oder eine Fertiggarage gelten.""",
                                    accept_new_options=True,
                                    toast_message="Hinweis: Sie haben einen benutzerdefinierten Wert für die Betrachtungsebene importiert, welcher Sich nicht in den eigentlichen Auswahlmöglichkeiten der Select Box wiederfindet."
                                    )
        
        edit_bezeichnung = st.text_input("Bezeichnung (Bearbeitung)",value=selected_product["bezeichnung"],key="edit_bezeichnung")   
        edit_verortung = st.text_input("Verortung (Bearbeitung)",value=selected_product["verortung"],key="edit_verortung")
        
        edit_klassifizierung = dynamic_selectbox(
                                    label="Klassifizierung",
                                    official_list=Data.backend.DIN276klassifizierung,
                                    current_value=selected_product["klassifizierung"],
                                    key="edit_klassifizierung",
                                    help_text="""Nach DIN 276. Möglichen Wert aus Dropdown-Menü wählen. Falls kein passender Wert gegeben ist, dann eigene Werteingabe vornehmen.""",
                                    accept_new_options=True,
                                    toast_message="Hinweis: Sie haben einen benutzerdefinierten Wert für die Klassifizierung importiert, welcher Sich nicht in den eigentlichen Auswahlmöglichkeiten der Select Box wiederfindet."
                                    )
        
        edit_abfallschlüsselnummer = dynamic_selectbox(
                                    label="Abfallschlüsselnummer",
                                    official_list=Data.backend.Abfallschlüsselnummer,
                                    current_value=selected_product["abfallschlüsselnummer"],
                                    key="edit_abfallschlüsselnummer",
                                    help_text="""Möglichen Wert aus Dropdown-Menü wählen. Falls kein passender Wert gegeben ist, dann eigene Werteingabe vornehmen. Relevant sofern nach Level(s) 2.2 berichtet werden soll.""",
                                    accept_new_options=True,
                                    toast_message="Hinweis: Sie haben einen benutzerdefinierten Wert als Abfallschlüsselnummer importiert, welcher Sich nicht in den eigentlichen Auswahlmöglichkeiten der Select Box wiederfindet."
                                    )
        
        edit_material = dynamic_selectbox(
                                    label="Material",
                                    official_list=Data.backend.Materialien,
                                    current_value=selected_product["material"],
                                    key="edit_material",
                                    help_text="""Möglichen Wert aus Dropdown-Menü wählen. Falls kein passender Wert gegeben ist, dann eigene Werteingabe vornehmen. Aufgeführte Wertemöglichkeiten entnommen aus Level(s) 2.2.""",
                                    accept_new_options=True,
                                    toast_message="Hinweis: Sie haben einen benutzerdefinierten Wert als Material verwendet, welcher Sich nicht in den eigentlichen Auswahlmöglichkeiten der Select Box wiederfindet."
                                    )
        
        edit_hersteller = st.text_input("Hersteller", value=selected_product.get("hersteller", ""))
        edit_variante = st.text_input("Variante / Fabrikat", value=selected_product.get("variante", ""), help="Optionale Angabe")
        edit_menge = st.number_input("Menge", value=float(selected_product.get("menge", 0)), format="%.2f")
        edit_einheit = st.text_input("Einheit", value=selected_product.get("einheit", ""))
        edit_umrechnungsfaktor = st.text_input("Level(s) 2.2 - Umrechnungsfaktor", value=selected_product.get("umrechnungsfaktor", ""))
        edit_menge_kg = st.text_input("Level(s) 2.2 - Menge [kg]", value=selected_product.get("menge_kg", ""))
        edit_höhe = st.number_input("Höhe [mm]", value=float(selected_product.get("höhe_mm", 0)), format="%.0f")
        edit_breite = st.number_input("Breite [mm]", value=float(selected_product.get("breite_mm", 0)), format="%.0f")
        edit_länge = st.number_input("Länge [mm]", value=float(selected_product.get("länge_mm", 0)), format="%.0f")
        
        edit_zugänglichkeit = dynamic_selectbox(
                                    label="Zugänglichkeit",
                                    official_list=Data.backend.Zugänglichkeit,
                                    current_value=selected_product["zugänglichkeit"],
                                    key="edit_zugänglichkeit",
                                    help_text="""Information hinsichtlich der  Zugänglichkeit des Bauproduktes im Falle eines Rückbaus.
                                    Nach Madaster ZI bzw. GRP. Möglichen Wert aus Dropdown-Menü wählen. Falls kein passender Wert gegeben ist, dann eigene Werteingabe vornehmen.""",
                                    accept_new_options=True,
                                    toast_message="Hinweis: Sie haben einen benutzerdefinierten Wert als Zugänglichkeit verwendet, welcher Sich nicht in den eigentlichen Auswahlmöglichkeiten der Select Box wiederfindet."
                                    )
        
        edit_verbindungsartgrob = dynamic_selectbox(
                                    label="Verbindungsart (grobe Einschätzung)",
                                    official_list=Data.backend.Verbindungart_grob,
                                    current_value=selected_product["verbindungsartgrob"],
                                    key="edit_verbindungsartgrob",
                                    help_text="""Möglichen Wert aus Dropdown-Menü wählen. Falls kein passender Wert 
                                                gegeben ist, dann eigene Werteingabe vornehmen.""",
                                    accept_new_options=True,
                                    toast_message="Hinweis: Sie haben einen benutzerdefinierten Wert als Verbindungsart (grobe Einschätzung) verwendet, welcher Sich nicht in den eigentlichen Auswahlmöglichkeiten der Select Box wiederfindet."
                                    )
        
        edit_schadstoffverdacht = dynamic_selectbox(
                                    label="Einschätzung hinsichtlich Schadstoffverdacht bzw. Level(s) 2.2 - Abfallart",
                                    official_list=Data.backend.Schadstoffverdacht,
                                    current_value=selected_product["schadstoffverdacht"],
                                    key="edit_schadstoffverdacht",
                                    help_text="""Information hinsichtlich eines Schadstoffverdachtes bzw. der Abfallart.
                                    Relevant sofern nach Level(s) 2.2 berichtet werden soll.
                                    Info: Inertabfälle sind Massen, die weder chemisch noch biologisch reaktiv sind, noch sich auflösen oder verbrennen.""",
                                    accept_new_options=True,
                                    toast_message="Hinweis: Sie haben einen benutzerdefinierten Wert als Einschätzung hinsichtlich Schadstoffverdacht bzw. Level(s) 2.2 - Abfallart verwendet, welcher Sich nicht in den eigentlichen Auswahlmöglichkeiten der Select Box wiederfindet."
                                    )
        
    
        edit_fotos = st.text_area("Fotos", value=selected_product.get("fotos", ""), help="Das vorliegende Tool unterstützt zum aktuellen Zeitpunkt keine Eingabe von Fotos. Sie können hier beispielsweise auf Fotos verweisen oder diese zusätzlich beschreiben. Es sollte hierbei genau beschrieben werden, was durch Fotos dargestellt werden soll: Gebrauchszustand, Materialqualität, Einbausituation, Verortung.")
        edit_gebrauchszustand = st.text_area("Gebrauchszustand - Visuell", value=selected_product.get("gebrauchszustand", ""), help="Bspw. Hinweise auf Korrosion, vorliegende Risse, Abplatzungen, Verformungen etc.")

        edit_funktion = dynamic_selectbox(
                                    label="Funktion des Bauprodukts in der baulichen Anlage",
                                    official_list=Data.backend.Bauprodukt_Funktion,
                                    current_value=selected_product["funktionbauprodukt"],
                                    key="edit_funktion",
                                    help_text="""Information bzgl. der Funktion des Bauprodukts in der baulichen Anlage in Anlehnung an das Six Layers Modell nach [Brand](https://c2c-bau.org/10-planung/10-1-gebaeudebereiche/). Falls keine passende Wertemöglichkeit gegeben ist, Wert überschreiben.""",
                                    accept_new_options=True,
                                    toast_message="Hinweis: Sie haben einen benutzerdefinierten Wert als Funktion des Bauprodukts in der baulichen Anlage verwendet, welcher Sich nicht in den eigentlichen Auswahlmöglichkeiten der Select Box wiederfindet."
                                    )
        
        edit_anschlussnutzungspotenzial = dynamic_selectbox(
                                    label="Potenzial für Anschlussnutzung",
                                    official_list=Data.backend.Anschlussnutzungspotenzial,
                                    current_value=selected_product["anschlussnutzungspotenzial"],
                                    key="edit_anschlussnutzungspotenzial",
                                    help_text="""Initiale Einschätzung bzgl. des vorliegenden Potenzials zur Anschlussnutzung. Falls keine passende Wertemöglichkeit gegeben ist, Wert überschreiben.""",
                                    accept_new_options=True,
                                    toast_message="Hinweis: Sie haben einen benutzerdefinierten Wert als Potenzial für Anschlussnutzung verwendet, welcher Sich nicht in den eigentlichen Auswahlmöglichkeiten der Select Box wiederfindet."
                                    )
        
        edit_anschlussnutzungspotenzial_begründung =  st.text_area("Begründung der Einschätzung",value=selected_product.get("anschlussnutzungspotenzial_begründung", ""))
        edit_product_weitereinfosstufe1 = st.text_area("Weitere Informationen - Stufe 1", value=selected_product.get("product_weitereinfosstufe1", ""))

        ############################# Ab hier die Edit functions für PDA Stufe 2
        "Stufe 2:"
        
        edit_einbaujahr = st.text_input("Einbaujahr",value=selected_product["product_einbaujahr"])
        edit_produktionsjahr = st.text_input("Produktionsjahr", value=selected_product.get("product_produktionsjahr", ""))
        edit_vorgeschichte = st.text_area("Vorgeschichte", value=selected_product.get("vorgeschichte", ""))
        edit_brandeinwirkung = st.text_input("Brandeinwirkung", value=selected_product.get("brandeinwirkung", ""))
        edit_frost_tauwechsel = st.text_input("Frost-Tauwechsel", value=selected_product.get("frost_tauwechsel", ""))
        edit_bestehendeunterlagen = st.text_area("Bestehende Unterlagen", value=selected_product.get("product_bestehende_unterlagen", ""))
        edit_spezifischeattribute = st.text_area("Spezifische Attribute zum Produkt", value=selected_product.get("product_spezifischeattribtue", ""))
        edit_fachgutachen = st.text_area("Fachgutachen (Baustoffanalyse, Werkstoffanalyse)", value=selected_product.get("fachgutachen", ""))
        edit_schadstoffgutachten = st.text_area("Schadstoffgutachten", value=selected_product.get("schadstoffgutachten", ""))

        edit_verbindungsart = dynamic_selectbox(
                                    label="Verbindungsart",
                                    official_list=Data.backend.Verbindungsart,
                                    current_value=selected_product["verbindungsart"],
                                    key="edit_verbindungsart",
                                    help_text="""Wertmöglichkeiten nach DGNB Gebäuderessourcenpass bzw. DGNB ZI.""",
                                    accept_new_options=False,
                                    toast_message="Hinweis: Sie haben einen benutzerdefinierten Wert als Verbindungsart verwendet, welcher Sich nicht in den eigentlichen Auswahlmöglichkeiten der Select Box wiederfindet."
                                    )
        
        edit_demontierbarkeit = get_demontierbarkeit(edit_verbindungsart)
        st.text_input("Demontierbarkeit:", value=edit_demontierbarkeit, disabled=True, help="Wertmöglichkeiten nach DGNB Gebäuderessourcenpass bzw. DGNB ZI; Wert ergibt sich aufbauend auf der gewählten Verbindungsart.")

        edit_potenzielleanschlussnutzung = dynamic_selectbox(
                                    label="Potenzielle Anschlussnutzung",
                                    official_list=Data.backend.Potenzielle_Anschlussnutzung,
                                    current_value=selected_product["potenzielle_anschlussnutzung"],
                                    key="edit_potenzielleanschlussnutzung",
                                    help_text="""Multiple Werteeingabe möglich. Hierfür bitte einfach individuell eingeben.""",
                                    accept_new_options=True,
                                    toast_message="Hinweis: Sie haben einen benutzerdefinierten Wert als potenzielle Anschlussnutzung verwendet, welcher Sich nicht in den eigentlichen Auswahlmöglichkeiten der Select Box wiederfindet."
                                    )
        
        edit_empfohleneanschlussnutzung = dynamic_selectbox(
                                    label="Level(s) 2.2 - Empfohlene Anschlussnutzung (Auditor)",
                                    official_list=Data.backend.levels_Anschlussnutzung,
                                    current_value=selected_product["empfohlene_anschlussnutzung"],
                                    key="edit_empfohleneanschlussnutzung",
                                    help_text="""Optionales Eingabefeld sofern nach Level(s) 2.2 berichtet werden soll.""",
                                    accept_new_options=True,
                                    toast_message="Hinweis: Sie haben einen benutzerdefinierten Wert als Level(s) 2.2 - Empfohlene Anschlussnutzung (Auditor) verwendet, welcher Sich nicht in den eigentlichen Auswahlmöglichkeiten der Select Box wiederfindet."
                                    )
        edit_wahrscheinlicheanschlussnutzung = dynamic_selectbox(
                                    label="Level(s) 2.2 - Wahrscheinliche Anschlussnutzung (Waste Manager)",
                                    official_list=Data.backend.levels_Anschlussnutzung,
                                    current_value=selected_product["wahrscheinliche_anschlussnutzung"],
                                    key="edit_wahrscheinlicheanschlussnutzung",
                                    help_text="""Optionales Eingabefeld sofern nach Level(s) 2.2 berichtet werden soll.""",
                                    accept_new_options=True,
                                    toast_message="Hinweis: Sie haben einen benutzerdefinierten Wert als Level(s) 2.2 - Wahrscheinliche Anschlussnutzung (Waste Manager) verwendet, welcher Sich nicht in den eigentlichen Auswahlmöglichkeiten der Select Box wiederfindet."
                                    )
        
        edit_rückbaumaßnahme = dynamic_selectbox(
                                    label="Level(s) 2.2 - Art der Rückbaumaßnahme",
                                    official_list=Data.backend.levels_Rückbaumaßnahme,
                                    current_value=selected_product["rückbaumaßnahmenart"],
                                    key="edit_rückbaumaßnahme",
                                    help_text="""Optionales Eingabefeld sofern nach Level(s) 2.2 berichtet werden soll. Auswahl einer der fünf Hauptrückbautätigkeiten, die für das Berichtsformat nach Level(s) Indicator 2.2 definiert sind.""",
                                    accept_new_options=False,
                                    toast_message="Hinweis: Sie haben einen benutzerdefinierten Wert als Level(s) 2.2 - Art der Rückbaumaßnahme verwendet, welcher Sich nicht in den eigentlichen Auswahlmöglichkeiten der Select Box wiederfindet."
                                    )
        
        edit_product_weitereinfosstufe2 = st.text_area("Weitere Informationen - Stufe 2", value=selected_product.get("product_weitereinfosstufe2", ""))
        
        ######################################################################
        col1, col2 = st.columns(2)
        
        if col1.button("Änderungen speichern"):
            st.session_state["products"][selected_idx] = {
                            
                #stufe 2
                "product_einbaujahr" : edit_einbaujahr,
                    "product_id": edit_id,
                    "betrachtungsebene" : edit_betrachtungsebene,
                    "bezeichnung" : edit_bezeichnung,
                    "verortung" : edit_verortung,
                    "klassifizierung" : edit_klassifizierung,
                    "abfallschlüsselnummer" : edit_abfallschlüsselnummer,
                    "material": edit_material,
                    "hersteller" : edit_hersteller,
                    "variante" : edit_variante,
                    "menge" : edit_menge,
                    "einheit" : edit_einheit,
                    "umrechungsfaktor" : edit_umrechnungsfaktor,
                    "menge_kg" : edit_menge_kg,
                    "höhe" : edit_höhe,
                    "breite" : edit_breite,
                    "länge" : edit_länge,
                    "zugänglichkeit" : edit_zugänglichkeit,
                    "verbindungsartgrob" : edit_verbindungsartgrob,
                    "schadstoffverdacht" : edit_schadstoffverdacht,
                    "fotos" : edit_fotos,
                    "gebrauchszustand" : edit_gebrauchszustand,
                    "funktionbauprodukt" : edit_funktion,
                    "anschlussnutzungspotenzial" : edit_anschlussnutzungspotenzial,
                    "anschlussnutzungspotenzial_begründung" : edit_anschlussnutzungspotenzial_begründung,
                    "product_weitereinfosstufe1" : edit_product_weitereinfosstufe1,

                    #### ab hier stufe 2
                    "product_einbaujahr" : edit_einbaujahr,
                    "product_produktionsjahr" : edit_produktionsjahr,
                    "vorgeschichte" : edit_vorgeschichte,
                    "brandeinwirkung" : edit_brandeinwirkung,
                    "frost_tauwechsel" : edit_frost_tauwechsel,
                    "product_bestehende_unterlagen" : edit_bestehendeunterlagen,
                    "product_spezifischeattribtue" : edit_spezifischeattribute,
                    "fachgutachten" : edit_fachgutachen,
                    "schadstoffgutachten" : edit_schadstoffgutachten,
                    "verbindungsart" : edit_verbindungsart,
                    "demontierbarkeit" : edit_demontierbarkeit,
                    "potenzielle_anschlussnutzung" : edit_potenzielleanschlussnutzung,
                    "empfohlene_anschlussnutzung" : edit_empfohleneanschlussnutzung,
                    "wahrscheinliche_anschlussnutzung" : edit_wahrscheinlicheanschlussnutzung,
                    "rückbaumaßnahmenart" : edit_rückbaumaßnahme,                    
                    "product_weitereinfosstufe2" : edit_product_weitereinfosstufe2
            }
            st.success("Änderungen wurden gespeichert.")
        
        if col2.button("Produkt löschen"):
            deleted = selected_product["product_id"]
            st.session_state["products"].pop(selected_idx)
            st.success(f"Bauprodukt '{deleted}' wurde gelöscht.")
            
            if not st.session_state["products"]:
                st.stop()
    else:
        st.write("Keine Bauprodukte erfasst.")

bauprodukte()

