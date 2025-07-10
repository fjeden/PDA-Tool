import streamlit as st
import json
from Data.backend import Bauwerkskategorien
from Data.backend import Gebäudeklassen
from Data.backend import Bauweise

def projektinformationen():
    
    st.set_page_config(page_title="Projektinformationen", page_icon=":file_folder:")
    
    st.header("Projektinformationen")
    
    # JSON-Import-Abschnitt
    st.subheader("Import eines bestehenden Projektes")
    uploaded_file = st.file_uploader("Laden Sie hier ein bestehendes Projekt als JSON-Datei hoch", type=["json"])
    if uploaded_file is not None:
        # Button zum tatsächlichen Einlesen der JSON-Datei
        if st.button("Import JSON"):
            try:
                data = json.load(uploaded_file)
                
                # Liegen die Schlüssel im JSON vor, werden sie in st.session_state übernommen
                if "project_info" in data:
                    st.session_state["project_info"] = data["project_info"]
                   
                if "products" in data:
                    st.session_state["products"] = data["products"]
                
                st.success("Daten für das Projekt " + st.session_state["project_info"].get("Projektname", "") + " erfolgreich importiert!")
            except Exception as e:
                st.error(f"Fehler beim Einlesen der JSON-Datei: {e}")
    
    # Session State vorbereiten (falls noch nicht geschehen)
    if "project_info" not in st.session_state:
        st.session_state["project_info"] = {}
    
    # Vorhandene Daten laden oder leere Vorgaben anzeigen
    project_name = st.text_input(
        "Projektname",
        value=st.session_state["project_info"].get("Projektname", "")
    )
    project_standort = st.text_input(
        "Standort",
        value=st.session_state["project_info"].get("Standort", "")
    )
    
    project_yearofconstruction = st.text_input(
        "Baujahr",
        value=st.session_state["project_info"].get("Baujahr", "")
    )
    
    prev_bauweise= st.session_state["project_info"].get("Bauweise", "")  
    local_bauweise = Bauweise.copy()
    if prev_bauweise not in Bauweise and prev_bauweise != "": 
        local_bauweise.insert(1,prev_bauweise)
        index_bauweise = 1
        st.toast("Achtung, Sie haben einen benutzerdefinierten Wert für die Bauweise/-art importiert, welcher Sich nicht in den Auswahlmöglichkeiten der Select Box wiederfindet.")  
    else:
        try: 
            index_bauweise = Bauweise.index(prev_bauweise)   
        except:
            index_bauweise = 0     
    project_bauweise = st.selectbox(
        "Bauweise/-art",
        options= local_bauweise,
        index= index_bauweise,
        accept_new_options= True,
        help= """Denkbare Möglichkeit aus Dropdown-Menü wählen. Falls kein passender Wert gegeben ist, dann eigene Werteingabe vornehmen.
        Die gegebenen Werte sind dem DGNB Gebäuderessourcenpass entnommen.
        """
    )
    
    prev_gebäudeklasse =  st.session_state["project_info"].get("Gebäudeklasse", "") 
    local_gebäudeklasse = Gebäudeklassen.copy() 
    if prev_gebäudeklasse not in Gebäudeklassen and prev_gebäudeklasse != "":        
        local_gebäudeklasse.insert(1,prev_gebäudeklasse)
        index_gebäudeklasse = 1
        st.toast("Achtung, Sie haben einen benutzerdefinierten Wert für die Bauwerkskategorie importiert, welcher Sich nicht in den Auswahlmöglichkeiten der Select Box wiederfindet.")    
    else:
        try: 
            index_gebäudeklasse = Gebäudeklassen.index(prev_gebäudeklasse)      
        except:
            index_gebäudeklasse = 0        
    project_gebäudeklasse = st.selectbox(
        "Gebäudeklasse",
        options= local_gebäudeklasse,
        index= index_gebäudeklasse,
        accept_new_options= False,
        help= "Wählen Sie hier bitte die Gebäudeklasse nach MBO § 2"
    )
    
    prev_bauwerkskategorie = st.session_state["project_info"].get("Bauwerkskategorie", "")  
    local_cats = Bauwerkskategorien.copy()
    if prev_bauwerkskategorie not in Bauwerkskategorien and prev_bauwerkskategorie != "": 
        local_cats.insert(1,prev_bauwerkskategorie)
        index_class = 1
        st.toast("Achtung, Sie haben einen benutzerdefinierten Wert für die Bauwerkskategorie importiert, welcher Sich nicht in den Auswahlmöglichkeiten der Select Box wiederfindet.")  
    else:
        try: 
            index_class = Bauwerkskategorien.index(prev_bauwerkskategorie)   
        except:
            index_class = 0     
    project_bauwerkskategorie = st.selectbox(
        "Bauwerkskategorie und Nutzungsart",
        options= local_cats,
        index= index_class,
        accept_new_options= False,
        help= "Wählen Sie hier bitte die Bauwerkskategorie nach HOAI Anlage 10.2"
    )
    
    project_bri= st.number_input(
        "BRI (Brutto-Rauminhalt) [m³]",
        value=st.session_state["project_info"].get("BRI", 0.0),
        format="%.2f",   # zwei Nachkommastellen
        help = "Nach DIN 277"
    )
    
    project_bgf = st.number_input(
        "BGF (Brutto-Grundfläche) [m²]",
        value = st.session_state["project_info"].get("BGF", 0.0),
        format="%.2f",   # zwei Nachkommastellen
        help = "Nach DIN 277"
    )
    
    project_umbaumassnahmen = st.text_area(
        "Informationen über vergangene Umbaumaßnahmen",
        value=st.session_state["project_info"].get("Umbaumassnahmen", "")
    )
    
    project_nutzungsgeschichte = st.text_area(
        "Nutzungsgeschichte",
        value=st.session_state["project_info"].get("Nutzungsgeschichte", "")
    )
    
    project_grobeErschliessung = st.text_area(
        "Grobe Erschließung",
        value=st.session_state["project_info"].get("Grobe Erschliessung", ""),
        help= "z. B. Fahrstuhl vorhanden, Einrüstung möglich etc."
    )
    
    project_lagerung = st.text_area(
        "Lokale Möglichkeiten für die Lagerung von sekundären Bauprodukten bzw. Ersatzbaustoffen oder zur Aufbereitung ebenjener",
        value=st.session_state["project_info"].get("Lagerung", "")
    )
    
    project_weitereInfos = st.text_area(
        "Weitere grundlegende Informationen",
        value=st.session_state["project_info"].get("Weitere Infos", ""),
        help = "Auflistung von bspw. zur Verfügung stehender Dokumente etc."
    )
    

    # Button zum Speichern
    if st.button("Speichern"):
        st.session_state["project_info"]["Projektname"] = project_name
        st.session_state["project_info"]["Standort"] = project_standort
        # st.session_state["project_info"]["description"] = project_description
        st.session_state["project_info"]["Bauwerkskategorie"] = project_bauwerkskategorie
        st.session_state["project_info"]["Baujahr"] = project_yearofconstruction
        st.session_state["project_info"]["Bauweise"] = project_bauweise
        st.session_state["project_info"]["Gebäudeklasse"] = project_gebäudeklasse
        st.session_state["project_info"]["BRI"] = project_bri
        st.session_state["project_info"]["BGF"] = project_bgf
        st.session_state["project_info"]["Umbaumassnahmen"] = project_umbaumassnahmen
        st.session_state["project_info"]["Nutzungsgeschichte"] = project_nutzungsgeschichte
        st.session_state["project_info"]["Grobe Erschliessung"] = project_grobeErschliessung
        st.session_state["project_info"]["Lagerung"] = project_lagerung
        st.session_state["project_info"]["Weitere Infos"] = project_weitereInfos
        st.success("Projektinformationen wurden gespeichert.")

# Wird ausgeführt, sobald diese Seite in der Streamlit-Navigation ausgewählt wird
projektinformationen()