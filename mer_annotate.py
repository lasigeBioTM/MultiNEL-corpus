import logging
import merpy
import os
import spacy
import sys
import time
from load_icd10cm import load_icd10cm
from tqdm import tqdm
sys.path.append("./")


def annotate_documents(language, name_to_id):
    """Recognises entities (NER) in the retrieved Scielo abstracts, 
       link them to the respective ICD 10 CM code (NEL), if available, 
       and generates the respective annotations file.

    :param language: language version of the dataset to generate: 
        "pt" (Portuguese version), "en" (English version), 
        "es" (Spanish version)
    :param name_to_id:  includes names and the respective codes. 
    :type name_to_id: dict
    """

    # Configure MERPY, preprocessing the selected lexicon 
    lexicon_name = "icd10cm" + language
    
    merpy.create_lexicon(name_to_id.keys(), lexicon_name)
    merpy.create_mappings(name_to_id, lexicon_name)
    merpy.process_lexicon(lexicon_name)

    # Configure sentence segmenter
    spacy_models = {"en": "en_core_web_md", "es": "es_core_news_md", 
                "pt": "pt_core_news_md"}
    nlp = spacy.load(spacy_models[language])

    abstracts_dir = "./scielo_abstracts/" 
    doc_w_ann_count = int()
    entity_count = int()
    linked_mentions = int()
    
    abstracts = os.listdir(abstracts_dir)
    pbar = tqdm(total=int(len(abstracts)/3))
    
    logging.info("Annotating the abstracts...")

    for abstract in abstracts:
        
        if abstract[-2:] == language:
            out_ann = str()
            out_txt = str()

            with open(abstracts_dir + abstract, 'r') as input_file:
                text = input_file.read()
                input_file.close()
                document_ent_count = int()
                
                current_pos = int()
                text_spacy = nlp(text)
                
                for sent in text_spacy.sents:
                    entities = merpy.get_entities(sent.text, lexicon_name)
                   
                    for entity in entities:

                        if entity != ['']:
                            entity_count += 1
                            document_ent_count += 1
                            
                            begin_pos = str(current_pos + int(entity[0]))
                            end_pos = str(current_pos + int(entity[1]))
                            
                            if len(entity) == 4: 
                                # Linked mentions with ICD code
                                linked_mentions += 1
                                out_ann += "T" + str(document_ent_count) \
                                    + "\t" + begin_pos + " " + end_pos + "\t"\
                                    + entity[2] + "\t" + entity[3] + "\n"
                            
                            elif len(entity) == 3: 
                                # Mentions without ICD code
                                out_ann += "T" + str(document_ent_count) \
                                    + "\t" + begin_pos + " " + end_pos  + "\t"\
                                    + entity[2] + "\n"
                    
                    out_txt += sent.text + " "
                    current_pos += len(sent.text) + 1

                if document_ent_count > 0:
                    doc_w_ann_count += 1
                
                # Generate text file, to ensure that annotations spans match
                # the text 
                with open(abstracts_dir + abstract, 'w') as out_txt_file:
                    out_txt_file.write(out_txt)
                    out_txt_file.close()
                    
            # Generate annotations file
            out_ann_filename = "./mer_annotations/" + language + "/" \
                + abstract + ".ann"

            with open(out_ann_filename, 'w') as out_ann_file:
                out_ann_file.write(out_ann)
                out_ann_file.close()
            
            pbar.update(1)
            
    pbar.close()
    logging.info("Done!")

    # Calculate overall annotations stats
    try:
        mentions_ratio = float(entity_count/doc_w_ann_count)
        doc_linked_ratio = float(linked_mentions/doc_w_ann_count)
        linked_ratio = float(linked_mentions/entity_count)
    
    except:
        mentions_ratio = 0.0
        doc_linked_ratio = 0.0
        linked_ratio = 0.0

    stats = "DOCUMENTS WITH ANNOTATIONS: " + str(doc_w_ann_count) + "\n"
    stats += "TOTAL ENTITY MENTIONS: " + str(entity_count) + "\n"
    stats += "ENTITY MENTIONS PER DOCUMENT: " + str(mentions_ratio) + "\n"
    stats += "LINKED ENTITY MENTIONS: " + str(linked_mentions) + "\n"
    stats += "LINKED ENTITY MENTIONS PER DOCUMENT: " \
        + str(doc_linked_ratio) + "\n"
    stats += "RATIO OF LINKED ENTITY MENTIONS: " + str(linked_ratio)

    stats_filename = "mer_annotation_stats_" + language

    with open(stats_filename, "w") as output:
        output.write(stats)
        output.close()
    
    logging.info("Generated " + stats_filename)
    
    
if __name__ == "__main__":
    language = str(sys.argv[1])
    
    # Configure log file
    log_filename = "annotation_" + language + ".log"
    
    logging.basicConfig(
        filename=log_filename, level=logging.INFO, 
        format='%(asctime)s | %(levelname)s: %(message)s', 
            datefmt='%m/%d/%Y %I:%M:%S %p',
        filemode='w')

    name_to_id = load_icd10cm(language)

    annotate_documents(language, name_to_id)
   
