# # In die Kommandozeile den Befehl eigeben um die virtuelle Umgebung zu starten
# .venv\Scripts\Activate.ps1

#und dann bring die App zum laufen mit: streamlit run Startseite.py

import streamlit as st
# import json

def main():
    st.set_page_config(page_title="Pre-Demolition-Audit Tool", layout="centered", page_icon=":recycle:")
    
    # st.sidebar.title("Navigation")
    # st.sidebar.markdown("---")  # Trenner
    
    
    st.title("Pre-Demolition-Audit Tool")
    st.markdown(
        '''        
        Das vorliegende Tool entstand im Rahmen des Forschungsprojektes [DeConDB](https://daten.plus/projekte/de-con-db) und
        stellt einen möglichen Ansatz zur Dokumentation eines Pre-Demolition-Audits (PDA) dar. 
        
        Nutzen Sie das Menü in der linken Seitenleiste, um zu den einzelnen Schritten zu navigieren.
        
        Neben grundlegenden Projektinformationen können einzelne Bauprodukte angelegt werden. Auf der Übersicht-Seite können die definierten Informationen in zusammengefasster Form eingesehen
        sowie die Ergebnisse als JSON-Datei oder Excel-Datei ausgegeben werden. Eine mit dem vorliegenden Tool exportierte JSON-Datei
        kann ebenso wieder importiert und das Projekt weiterbearbeitet werden.
        
        Bitte achten Sie darauf, etwaige eingegebene Informationen zu speichern. Nutzen Sie hierfür die gegebenen Buttons.
        Achten Sie bitte zudem darauf, dass ein Neuladen der Seite zu einem etwaigen Verlust von Daten führt.
        
        ''')
    st.divider()
    st.subheader("Weitere Infos")  
    st.markdown('''
                Grundlegend basiert der Aufbau des Tools auf dem Pre-Demolition-Audit nach [DIN SPEC 91484](https://www.din.de/de/wdc-beuth:din21:371235753).
                Außerdem wurden Anteile aus dem [EU construction & demolition waste management protocol including guidelines for pre-demolition and pre-renovation audits of construction works](https://op.europa.eu/en/publication-detail/-/publication/d63d5a8f-64e8-11ef-a8ba-01aa75ed71a1) 
                sowie dem [Level(s) Indicator 2.2](https://susproc.jrc.ec.europa.eu/product-bureau/sites/default/files/2020-10/20201013%20New%20Level(s)%20documentation_2.2%20C&d%20waste_Publication%20v1.0.pdf) übernommen.
                Der Outcome des Tools kann somit als Ausgangsbasis für ein Level(s)-konformes PDA verwendet werden.
                Darüber hinaus wurden stellenweise Parameter und Wertemöglichkeiten aus den Ansätzen der Zirkularitätsindizes bzw. der Gebäuderessourcenpässe von [Madaster](https://docs.madaster.com/de/de/knowledge-base/calculations) und der [DGNB](https://www.dgnb.de/de/nachhaltiges-bauen/zirkulaeres-bauen/zirkularitaetsindizes-fuer-bauwerke) entnommen.
                Weiterhin wurden die so zusammengestellten Informationsanforderungen durch eine entsprechende Praxisbeteiligung ergänzt sowie validiert.
                ''')
    
    st.markdown('''Weitere Informationen zum Projekt [DeConDB](https://daten.plus/projekte/de-con-db) können Sie unserem [Projektblog](https://blog.rwth-aachen.de/decondb/) entnehmen.
                Bei weiteren Anmerkungen/Fragen gerne [Fabian Edenhofner](https://www.icom.rwth-aachen.de/cms/icom/Das-Institut/Team/Kontaktdaten/Research-Assistants/~ptkpf/Edenhofner-Fabian/) kontaktieren.
                ''')
    

    

    # # JSON-Import-Abschnitt
    # st.subheader("Import eines bestehenden Projektes")
    # uploaded_file = st.file_uploader("Laden Sie hier ein bestehendes Projekt als JSON-Datei hoch", type=["json"])
    # if uploaded_file is not None:
    #     # Button zum tatsächlichen Einlesen der JSON-Datei
    #     if st.button("Import JSON"):
    #         try:
    #             data = json.load(uploaded_file)
                
    #             # Liegen die Schlüssel im JSON vor, werden sie in st.session_state übernommen
    #             if "project_info" in data:
    #                 st.session_state["project_info"] = data["project_info"]
    #                 # st.write("Projektname: " + st.session_state["project_info"].get("name", ""))
    #             if "products" in data:
    #                 st.session_state["products"] = data["products"]
                
    #             st.success("Daten für das Projekt " + st.session_state["project_info"].get("name", "") + " erfolgreich importiert!")
    #         except Exception as e:
    #             st.error(f"Fehler beim Einlesen der JSON-Datei: {e}")

if __name__ == "__main__":
    # Wichtig: Session State kann an dieser Stelle initialisiert werden,
    # falls noch nicht vorhanden
    if "project_info" not in st.session_state:
        st.session_state["project_info"] = {}
    if "products" not in st.session_state:
        st.session_state["products"] = []
    
    main()