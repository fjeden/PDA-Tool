import streamlit as st
st.set_page_config(page_title="Datenschutz & Impressum", page_icon="📖")

st.header("Datenschutzerklärung und Impressum")

st.subheader("Datenschutzerklärung | **UNTER BEARBEITUNG**")

# Aussage Mcclay: Die Datenschutzerklärung der RWTH können Sie als Basis verwenden. 
# Punkte 3 bis 11 müssten Sie allerdings tatsächlich an Ihre eigenen Angaben und Gegebenheiten anpassen. 
# Wenn Sie beispielsweise keine YouTube Videos einbinden, muss auch nichts zu YouTube in der Erklärung stehen.
# Auch der Punkt „Bereitstellung der Website und Erstellung von Logfiles“ ist in Ihrer Hostingumgebung wahrscheinlich komplett unterschiedlich zu dem, was auf der RWTH-Seite gilt. 
# Hier fragen Sie am besten beim Hoster (IT Center?) nach, um zu erfahren, wie dort die Gegebenheiten sind.
st.markdown("**<u>I. Allgemeines</u>**", unsafe_allow_html=True)
"""Das vorliegende Webtool ist im Rahmen des Verbundprojektes [DeConDB](https://daten.plus/projekte/de-con-db) (Förderkennzeichen: 19FS2062A-D) entstanden.

**Über das Förderprogramm mFUND des BMDS**

Im Rahmen des Förderprogramms mFUND unterstützt das BMDS seit 2016 Forschungs- und Entwicklungsprojekte rund um datenbasierte digitale Innovationen für die Mobilität 4.0. 
Die Projektförderung wird ergänzt durch eine aktive fachliche Vernetzung zwischen Akteuren aus Politik, Wirtschaft, Verwaltung und Forschung und die Bereitstellung von offenen Daten auf der Mobilithek.
Weitere Informationen finden Sie unter [www.mfund.de](https://www.bmv.de/DE/Themen/Digitales/mFund/Ueberblick/ueberblick.html).
"""
# Erstelle zwei Spalten für die Bilder
col1, col2 = st.columns(2)

with col1:
    # Bild in der zweiten Spalte
    st.image("Data/mFUND_Logo_Mobilitaet_RGB.png", use_container_width=True)
    
with col2:
    # Bild in der ersten Spalte
    st.image("Data/BMDS_Fz_2025_Office_de.png",  use_container_width=True)

st.markdown("**<u>II. Verantwortlicher für die Datenverarbeitung</u>**", unsafe_allow_html=True)

st.markdown("""
            Der Verantwortliche im Sinne der EU-Datenschutz-Grundverordnung und anderer nationaler Datenschutzgesetze der Mitgliedsstaaten sowie sonstiger datenschutzrechtlicher Bestimmungen ist:
            
            Rektor der RWTH Aachen University<br>
            Templergraben 55<br>
            52062 Aachen (Hausanschrift)<br>
            52056 Aachen (Postanschrift)<br>
            Telefon: +49 241 80 1<br>
            Telefax: +49 241 80 92312<br>
            E-Mail: rektorat@rwth-aachen.de<br>
            Website: www.rwth-aachen.de/rektorat<br>
            
            Verantwortlich für die Umsetzung der Website ist:

            Lehrstuhl und Institut für Baumanagement, Digitales Bauen und Robotik im Bauwesen<br>
            Jülicher Straße 209d<br>
            52070 Aachen

            Institutsleitung: Univ.-Prof. Dr.-Ing. Katharina Klemt-Albert<br>
            Telefon: +49 241 80 25140<br>
            E-Mail: info@icom.rwth-aachen.de

            Projektleitung: Fabian Edenhofner<br>
            Telefon: +49 241 80 20078<br>
            E-Mail: edenhofner@icom.rwth-aachen.de
            
            """, unsafe_allow_html=True)


#####################################################################################################################################################
#Impressum
st.markdown("---")
st.subheader("Impressum")
st.markdown("""**<u>Herausgeberin</u>**""", unsafe_allow_html=True)

st.markdown("""
            Herausgegeben im Auftrag des Rektors der Rheinisch-Westfälischen Technischen Hochschule (RWTH) Aachen.

            Rheinisch-Westfälische Technische Hochschule (RWTH) Aachen<br>
            Templergraben 55<br>
            52062 Aachen (Hausanschrift)<br>
            52056 Aachen (Postanschrift)<br>
            Telefon: +49 241 80-1<br>
            E-Mail: impressum@rwth-aachen.de

            Die Rheinisch-Westfälische Technische Hochschule (RWTH) Aachen ist eine Körperschaft des öffentlichen Rechts.<br>
            Sie wird durch den Rektor, Univ.-Prof. Dr. rer. nat. Dr. h.c. mult. Ulrich Rüdiger, vertreten.""", unsafe_allow_html=True)

st.markdown("**<u>Zuständige Aufsichtsbehörde</u>**", unsafe_allow_html=True) 

"Ministerium für Kultur und Wissenschaft des Landes Nordrhein Westfalen, Völklinger Straße 49, 40221 Düsseldorf."

st.markdown("**<u>Umsatzsteuer-Identifikationsnummer</u>**", unsafe_allow_html=True) 

"Gemäß § 27 a Umsatzsteuergesetz: DE 121689807"

st.markdown("**<u>Konzept und Design</u>**", unsafe_allow_html=True) 

"3pc GmbH Neue Kommunikation"

st.markdown("**<u>Inhaltliche Verantwortlichkeit</u>**", unsafe_allow_html=True) 

st.markdown("""
            Institutsleitung: Univ.-Prof. Dr.-Ing. Katharina Klemt-Albert<br>
            E-Mail: info@icom.rwth-aachen.de

            Projektleitung: Fabian Edenhofner<br>
            Telefon: +49 241 80 20078<br>
            E-Mail: edenhofner@icom.rwth-aachen.de

            Die vorliegende Website ist im Rahmen des Verbundvorhabens [DeConDB](https://daten.plus/projekte/de-con-db) (Förderkennzeichen 19FS2062A-D) entstanden.
            """, unsafe_allow_html=True)
