import xml.etree.ElementTree as ET
import streamlit as st
import json
from deep_translator import GoogleTranslator


file = st.file_uploader("Upload your .resx file")
targetLang = None
with open("langCodes.json") as json_file:
    json_data = json.loads(json_file.read())
    countryDisplayNames = [obj['language'] for obj in json_data]
    targetLang = st.selectbox("Select the language you want to translate to", countryDisplayNames)

def create_resx():
    currentBatchValues = ""
    batch_count = 30
    values = []
    batchIndex = 0
    translatedText = ""

    if file is not None:
        tree = ET.parse(file)
        root = tree.getroot()

        for data_node in root.findall('data'):
            batchIndex += 1
            value_node = data_node.find('value')
            value = value_node.text if value_node is not None else None
            currentBatchValues += f"{value}\n"
            if(batchIndex > batch_count):
                batchIndex = 0
                values.append(f"{currentBatchValues}")
                currentBatchValues = ""
        values.append(f"{currentBatchValues}")

        selectedLang = None
        if(targetLang is not None):
            with open("langCodes.json") as json_file:
                langCodes = json.loads(json_file.read())
                for lang in langCodes:
                    if(lang['language'] == targetLang):
                        selectedLang = lang
                        for batch in values:
                            translatedText += GoogleTranslator(source='auto', target=selectedLang['countryCode']).translate(batch) + "\n"
                        translatedValues = translatedText.splitlines()

            i = 0

            print(f"length input: {len(root.findall('data'))}")
            print(f"length output: {len(translatedValues)}")

            for node in root.findall('data'):
                value_node = node.find('value')
                try:
                    value_node.text = translatedValues[i]
                except:
                    break
                i += 1

            tree.write(f"App.{selectedLang['code']}.resx", encoding="utf-8", xml_declaration=True)
            print(f"'App.{selectedLang['code']}.resx' created successfully")
            st.text(f"'App.{selectedLang['code']}.resx' created successfully!")

if st.button("Translate"):
    create_resx()