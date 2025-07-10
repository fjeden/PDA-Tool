import streamlit as st
import json
import pandas as pd
import io
# import zipfile

def create_excel_file(project_info: dict, products: list) -> bytes:
    """
    Hilfsfunktion, um eine Excel-Datei (Bytes) im Speicher zu erzeugen.
    - Tabellenblatt "Projektinfo"
    - Tabellenblatt "Bauprodukte"
    """
    # df_info = pd.DataFrame([{
    #     "Projektname": project_info.get("name", ""),
    #     "Standort": project_info.get("location", ""),
    #     "Bauwerkskategorie": project_info.get("Bauwerkskategorie", ""),
    #     "Baujahr": project_info.get("Baujahr", ""),
    #     "Bauweise": project_info.get("Bauweise", ""),
    #     "Gebäudeklasse": project_info.get("Gebäudeklasse", ""),
    #     "BRI": project_info.get("BRI", ""),
    #     "BGF": project_info.get("BGF", ""),
    #     "Umbaumaßnahmen": project_info.get("Umbaumassnahmen", ""),
    #     "Nutzungsgeschichte": project_info.get("Nutzungsgeschichte", ""),
    #     "Grobe Erschließung": project_info.get("GrobeErschliessung", ""),
    #     "Lagerung": project_info.get("Lagerung", ""),
    #     "Weitere Infos": project_info.get("weitereInfos", "")
    # }])
    df_info = pd.DataFrame([project_info]) if project_info else pd.DataFrame()
    
    df_products = pd.DataFrame(products) if products else pd.DataFrame()
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_info.to_excel(writer, sheet_name="Projektinfo", index=False)
        df_products.to_excel(writer, sheet_name="Bauprodukte", index=False)
    output.seek(0)
    return output.getvalue()

# def download_all_photos_as_zip(products: list) -> bytes:
#     """
#     Erzeugt ein ZIP-Archiv im Speicher, das alle Fotos zu allen Bauprodukten enthält.
#     Jede Datei wird anhand ihres 'filename' beschriftet.
#     """
#     zip_buffer = io.BytesIO()
#     with zipfile.ZipFile(zip_buffer, "w") as zf:
#         for product in products:
#             photo_list = product.get("photos", [])
#             for photo_info in photo_list:
#                 fname = photo_info["filename"]
#                 data = photo_info["data"]   # Binärdaten des Bildes
#                 zf.writestr(fname, data)    # in ZIP speichern
#     zip_buffer.seek(0)
#     return zip_buffer.getvalue()

def ueberblick():
    
    st.set_page_config(page_title="Übersicht", page_icon="📋")
   
    st.header("Projektübersicht und Export")
    
    if "project_info" not in st.session_state:
        st.session_state["project_info"] = {}
    if "products" not in st.session_state:
        st.session_state["products"] = []
    
    project_info = st.session_state["project_info"]
    products = st.session_state["products"]
    
    # Projektinformationen
    st.subheader("Projektinformationen")
    st.write("Projektname:", project_info.get("Projektname", ""))
    # st.write("Standort:", project_info.get("location", ""))
    # st.write("Bauwerkskategorie & Nutzungsart:", project_info.get("Bauwerkskategorie", ""))
    
    # Bauprodukte
    st.subheader("Erfasste Bauprodukte")
    if products:
        st.write("Sie haben insgesamt ", len(products), " Produkte erfasst.")
        # for i, p in enumerate(products, start=1):
        #     st.markdown(f"**{i}. {p['product_id']}**")
        #     # st.write(f"• Material: {p['material']}")
            
        #     st.write("---")
    else:
        st.write("Keine Bauprodukte erfasst.")
    
    # JSON-Export
    st.subheader("Export")
    data_to_export = {
        "project_info": project_info,
        "products": products
    }
    json_str = json.dumps(data_to_export, indent=4, ensure_ascii=False)
    st.download_button(
        label="JSON herunterladen",
        data=json_str,
        file_name="pre_demolition_audit.json",
        mime="application/json"
    )
    
    # Excel-Export
    excel_data = create_excel_file(project_info, products)
    st.download_button(
        label="Excel herunterladen",
        data=excel_data,
        file_name="pre_demolition_audit.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

ueberblick()