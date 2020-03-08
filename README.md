
# MultiNEL Corpus: Multilingual Named Entity Linking Corpus

A silver standard parallel corpus containing 1917 English, Spanish and Portuguese clinical case reports (639 for each language) annotated with medical diagnostic codes from the ICD10-CM 
([International Classification of Diseases, 10th Revision, Clinical Modification](https://en.wikipedia.org/wiki/ICD-10_Clinical_Modification)) terminology. To create a new corpus follow the instructions below.


## Dependencies
*requirements.txt* file:
- python >= 3.5
- [bs4](https://pypi.org/project/beautifulsoup4/)
- [merpy](https://pypi.org/project/merpy/)


## **Usage**



### **1. Get the data**

To download the English, Portuguese and Spanish versions of ICD10-CM:


```
./get_data.sh
```


Returns:
- *icd10cm_tabular_2020.xml* file with the English version
- *ICD10CMPCS_2017_PT_Longa e Curta_20180821corrigidav5.2.xlsx* file with the Portuguese version
- *CIE10_2020_DIAGNOST_REFERENCIA_2019_10_04_1.xlsx* file with the Spanish version



### **2. Retrieve abstracts from [SciELO](https://scielo.org/) repository**


To retrieve the clinical case reports (corresponding to SciELO search filters: * AND subject_area:("Health Sciences") AND type:("case-report") AND la:("es" OR "pt" OR "en")) whose abstract text is simultaneously in English, Portuguese and Spanish:
  

```
python retrieve_abstracts.py
```
 

Returns:
- *scielo_abstracts* dir containing the retrieved abstracts (file names with termination *en*, *pt*, *es* refer respectively to English, Portuguese and Spanish texts)
- *article_scielo_ids* file
- *abstract_retrieval_stats* file 



### **3. Annotate the abstracts**

To recognize the medical diagnostic entities in the abstracts and to link them to the appropriate code in the ICD10-CM terminology using MER (\<language\> is *en*, *pt* or *es*):


```
python mer_annotate.py <language>
```


Returns:
- *mer_annotations* dir containing the subdirectories *en*, *pt* and *es*, each subdirectory contains the annotations files for the abstracts in the referred language
- *mer_annotation_stats_*[LANGUAGE] file 

Example of the annotation file *S0034-70942002000300010-scl_pt.ann*:


[Term number]	[Begin] [End]	[Entity mention]	[ICD10-CM code]

>
>T1	626 645	insuficiência renal	N17-N19
>
>T2	29 47	doença de Moyamoya	I67.5
>
>T3	342 360	doença de Moyamoya	I67.5
>
>T4	541 559	doença de Moyamoya	I67.5
