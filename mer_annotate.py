from load_icd10cm import load_icd10cm
import merpy
import os
import sys
import time

sys.path.append("./")


def annotate_documents(language, name_to_id):
    """
    Recognise entities (Named Entity Recognition) and link them to the respective ICD 10 CM code (Named Entity Linking), if available

    Requires:
        language: str, "pt", "en", "es" for Portuguese, English or Spanish, respectively

    Ensures:
        for each abstract in 'scielo_abstracts' dir creates an annotation file in 'mer_annotations' dir and an overall statistics file about the annotation process

    """

    lexicon_name = "icd10cm_" + language
    merpy.create_lexicon(name_to_id.keys(), lexicon_name)
    merpy.create_mappings(name_to_id, lexicon_name)
    merpy.process_lexicon(lexicon_name)

    abstracts_dir = "./scielo_abstracts/" 
    doc_w_ann_count = int()
    entity_count = int()
    linked_mentions = int()
    
    for abstract in os.listdir(abstracts_dir):
        
        if abstract[-2:] == language:
            output_string = str()
          
            with open(abstracts_dir + abstract, 'r') as input_file:
                text = input_file.read()
                input_file.close()
                document_ent_count = int()

                entities = merpy.get_entities(text, lexicon_name)
                
                for entity in entities:

                    if entity != ['']:
                        entity_count += 1
                        document_ent_count += 1
                        
                        if len(entity) == 4: # linked mentions with ICD code
                            linked_mentions += 1
                            output_string += "T" + str(document_ent_count) + "\t" + entity[0] + " " + entity[1] + "\t" + entity[2] + "\t" + entity[3] + "\n"
                        
                        elif len(entity) == 3: # mentions without ICD code
                            output_string += "T" + str(document_ent_count) + "\t" + entity[0] + " " + entity[1] + "\t" + entity[2] + "\n"

                if document_ent_count > 0:
                    doc_w_ann_count += 1

            output_filename = "./mer_annotations/" + language + "/" + abstract + ".ann"

            with open(output_filename, 'w') as output_file:
                output_file.write(output_string)
                output_file.close()

    try:
        mentions_ratio = float(entity_count/doc_w_ann_count)
        doc_linked_ratio = float(linked_mentions/doc_w_ann_count)
        linked_ratio = float(linked_mentions/entity_count)
    
    except:
        mentions_ratio = 0.0
        doc_linked_ratio = 0.0
        linked_ratio = 0.0

    output_str = "DOCUMENTS WITH ANNOTATIONS: " + str(doc_w_ann_count) + "\n"
    output_str += "TOTAL ENTITY MENTIONS: " + str(entity_count) + "\n"
    output_str += "ENTITY MENTIONS PER DOCUMENT: " + str(mentions_ratio) + "\n"
    output_str += "LINKED ENTITY MENTIONS: " + str(linked_mentions) + "\n"
    output_str += "LINKED ENTITY MENTIONS PER DOCUMENT: " + str(doc_linked_ratio) + "\n"
    output_str += "RATIO OF LINKED ENTITY MENTIONS: " + str(linked_ratio)

    file_name = "mer_annotation_stats_" + language

    with open(file_name, "w") as output:
        output.write(output_str)
        output.close()
    
if __name__ == "__main__":

    start_time = time.time()
    language = str(sys.argv[1])
    name_to_id = load_icd10cm(language)
    print("Starting annotation...")
    annotate_documents(language, name_to_id)
    print("...Done!")
    print("Total time (aprox.):", int((time.time() - start_time)/60.0), "minutes\n----------------------------------")
