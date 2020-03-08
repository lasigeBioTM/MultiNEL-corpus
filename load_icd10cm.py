import os
import sys
import xml.etree.ElementTree as ET

sys.path.append("./")


def load_icd10cm(language):
    """Load ICD 10 CM from local files into dict
    
    Requires:
        language: is str, "pt" to load the portuguese version, "en" to load english version, "es to load the spanish version

    Ensures: 
        name_to_id: is dict with mappings between each ontology concept name and the respective ICD code;
    """
    
    print("Loading ICD 10...")

    name_to_id = dict()

    if language == "en":  #Parse the english version in .xml format
        tree = ET.parse("icd10cm_tabular_2020.xml") 
        root = tree.getroot()

        for chapter in root.iter("chapter"): 
            #chapter_number = chapter.find("name").text
            chapter_name = chapter.find("desc").text
            chapter_code = chapter_name.split("(")[1].strip(")")
            string_to_remove = "(" + chapter_code + ")"
            chapter_name = chapter_name.replace(string_to_remove, "")
            name_to_id[chapter_name] = chapter_code

            for section in chapter.iter("section"): # Retrieve section name and code
                section_code = section.attrib["id"]
                section_name = section.find("desc").text
                string_to_remove = "(" + section_code + ")"
                section_name = section_name.replace(string_to_remove, "")
                name_to_id[section_name] = section_code
                        
                for diagnostic in section.iter("diag"):        
                    diagnostic_code = diagnostic.find("name").text
                    diagnostic_name = diagnostic.find("desc").text

                    if len(diagnostic_code) == 3:
                        parent_code = section_code

                    if len(diagnostic_code) > 3:
                        parent_code = diagnostic_code[:-1]
                        
                        if parent_code[-1:] == ".":
                            parent_code = parent_code[:-1]

                    name_to_id[diagnostic_name] = diagnostic_code
        
    elif language == "pt": 
            
        pt_icd = pd.read_excel('ICD10CMPCS_2017_PT_Longa e Curta_20180821corrigidav5.2.xlsx', sheet_name = ['ICD10CM_2017_Capitulos', 'ICD10CM_2017_Secções', 'ICD10CM_2017_Diagnósticos'], header = 2)

        for row in pt_icd['ICD10CM_2017_Capitulos'].iterrows():
            code, description = row[1][1], row[1][3]
            string_to_remove = '(' + code + ')'
            description = description.replace(string_to_remove, '')
            name_to_id[description] = code

        for row in pt_icd['ICD10CM_2017_Secções'].iterrows():
                
            if row[1][1] != "nan": # Pass duplicate chapter codes in dict
                code, description = row[1][2], row[1][4]
                name_to_id[description] = code

        for row in pt_icd['ICD10CM_2017_Diagnósticos'].iterrows():
            code, description = row[1][0], row[1][2]
                
            if len(code) > 3:
                code = code[:3] + "." + code[3:]
                
            name_to_id[description] = code

    elif language == "es": 
            
        es_icd = pd.read_excel("CIE10_2020_DIAGNOST_REFERENCIA_2019_10_04_1.xlsx", sheet_name = ["CIE10ES 2020 COMPLETA MARCADORE"], header=1)
        
        chapter_dict = {'Cap.01': 'A00-B99', 'Cap.02': 'C00-D49', 'Cap.03': 'D50-D89', 'Cap.04': 'E00-E89', 'Cap.05': 'F01-F99', 'Cap.06': 'G00-G99', 
                'Cap.07': 'H00-H59', 'Cap.08': 'H60-H95', 'Cap.09': 'I00-I99', 'Cap.10': 'J00-J99', 'Cap.11': 'K00-K95', 'Cap.12': 'L00-L99', 
                'Cap.13': 'M00-M99', 'Cap.14': 'N00-N99', 'Cap.15': 'O00-O9A', 'Cap.16': 'P00-P96' , 'Cap.17': 'Q00-Q99', 'Cap.18': 'R00-R99', 
                'Cap.19': 'S00-T88', 'Cap.20': 'V00-Y99', 'Cap.21': 'Z00-Z99'}

        for row in es_icd["CIE10ES 2020 COMPLETA MARCADORE"].iterrows():
    
            code, description = row[1]['Tab.D'], row[1]['CIE-10-ES Diagnósticos 2020']

            if code in chapter_dict.keys():
                code = chapter_dict[code]

            string_to_remove = '(' + code + ')'
            description = description.replace(string_to_remove, '')
            name_to_id[description] = code

    
    print("ICD 10 CM loading complete")
    return name_to_id 


    



