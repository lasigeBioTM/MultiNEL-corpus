from bs4 import BeautifulSoup
from datetime import datetime
import os
import requests
import sys
import time

sys.path.append("./")


# Run this module to retrieve clinical case reports from the SciELO repository 
# (https://scielo.org/) that have the abstract text simultaneously in English, 
# Portuguese and Spanish. This will generate three alternative documents for 
# a given abstract in 'scielo_abstracts' dir

start_time = time.time()
print("Retrieving SciELO abstracts...")

start = 1

ids_str = str()
pt_ids_count = int()
es_ids_count = int()
en_ids_count = int()
abstracts_removal = list()
language_list = ["en", "es", "pt"]

while start <= 23101:

    # Search parameters: health sciences, case reports, 
    # english, portuguese, spanish
    url = 'https://search.scielo.org/?q=*&lang=pt&count=100&from=' \
        + str(start) \
        + '&output=site&sort=&format=summary&page=1&where=&filter[subject_area]\
        []=Health+Sciences&filter[type][]=case-report&filter[la][]=en&\
        filter_boolean_operator[la][]=OR&filter[la][]=pt&filter_boolean_\
        operator[la][]=OR&filter[la][]=es'
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    start += 100

    abstracts_dict = dict()

    for abstract in soup.body.find_all('div', attrs={'class':'abstract'}):
        scielo_id = abstract['id']
        text = abstract.text.replace("\n", "").replace("            ", "")\
            .replace("        ", "")
        language = scielo_id[-2:]
        abbr_scielo_id = scielo_id[:-3]
        values_to_add = (language, scielo_id, text)
        
        if abbr_scielo_id in abstracts_dict.keys():
            current_values = abstracts_dict[abbr_scielo_id]
            current_values.append(values_to_add)
            abstracts_dict[abbr_scielo_id] = current_values
        
        else:
            abstracts_dict[abbr_scielo_id] = [values_to_add]

    for abstract_id in abstracts_dict.keys():
        
        if len(abstracts_dict[abstract_id]) == 3:

            if abstracts_dict[abstract_id][0][0] in language_list \
                    and abstracts_dict[abstract_id][1][0] in language_list \
                    and abstracts_dict[abstract_id][2][0] in language_list:
            
                for value in abstracts_dict[abstract_id]:

                    if value[0] == "en":

                        with open('scielo_abstracts/' + value[1], 'w') \
                                as en_file:
                            en_ids_count += 1
                            en_file.write(value[2])
                            en_file.close
                            ids_str += value[1] + "\n"

                    elif value[0] == "es":
                        
                        with open('scielo_abstracts/' + value[1], 'w') \
                                as es_file:
                            es_ids_count += 1
                            es_file.write(value[2])
                            es_file.close
                            ids_str += value[1] + "\n"
                    
                    elif value[0] == "pt":

                        with open('scielo_abstracts/' + value[1], 'w') \
                                as pt_file:
                            pt_ids_count += 1
                            pt_file.write(value[2])
                            pt_file.close
                            ids_str += value[1] + "\n"

# Output file with the SciELO ids of the retrieved abstracts
with open("./article_scielo_ids", "w") as ids_file:
    ids_file.write(ids_str)
    ids_file.close()

# Output statistics file 
total = pt_ids_count + es_ids_count + en_ids_count

stats_str = str(pt_ids_count) + " PT abstracts retrieved\n" \
    + str(es_ids_count) + " ES abstracts retrieved\n" + str(en_ids_count) \
    + " EN abstracts retrieved\n" 
stats_str += str(total) + " Total abstracts retrieved" 
   
with open("./abstract_retrieval_stats", "w") as stats_file:
    stats_file.write(stats_str)
    stats_file.close()

print("Total time (aprox.):", int((time.time() - start_time)/60.0), "minutes")


                    





