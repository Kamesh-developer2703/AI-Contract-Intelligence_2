# Week 1 Progress Report



## AI-Powered Contract Intelligence \& Risk Scoring System



### Team Lead: Kameshwaran



Day 1 - Environment Setup \& Dataset Analysis



1. Set up the project repository and folder structure.
2. Created and managed GitHub branches for team members.
3. Downloaded and explored the CUAD (Contract Understanding Atticus Dataset).
4. Analyzed the dataset structure and identified:



* &#x20;  510 commercial contracts
* &#x20;  41 legal clause categories
* &#x20;  Contract text stored in context
* &#x20;  Clause annotations stored in qas



Documented dataset findings for future development.



Outcome:

Successfully understood the structure of the CUAD dataset and prepared the project environment.



\--------------------------------------------------------------------------------------------------------------



Day 2 - Question \& Answer Exploration



1. &#x20;	Explored the Question-Answer format used in CUAD.
2. &#x20;	Analyzed how clause categories are represented as questions.
3. &#x20;	Extracted contract questions and corresponding answers.
4. &#x20;	Developed scripts to understand and process contract annotations.
5. &#x20;	Created a sample training-ready JSON structure.



Outcome:

Successfully converted raw contract annotations into a structured format suitable for machine learning.



\----------------------------------------------------------------------------------------------------------------



Day 3 - Dataset Preprocessing



Developed preprocessing scripts to extract:



* &#x20;  Contract Title
* &#x20;  Clause Type
* &#x20;  Clause Text
* &#x20;  Converted all CUAD contracts into structured records.
* &#x20;   Generated a complete training dataset.



Results:



&#x20;Contracts Processed: 510

&#x20;Training Records Generated: 6702



Outcome:

Created the primary training dataset required for clause classification.



\----------------------------------------------------------------------------------------------------------



&#x20;Day 4 - Dataset Splitting \& Statistics



1. Generated dataset statistics.
2. Performed Train-Validation split (80:20).

Created:



* &#x20; Train.json
* &#x20; Validation.json
* &#x20; Dataset\_statistics.json
* &#x20; Verified data consistency and distribution.



Outcome:

Prepared datasets for model training and evaluation.



\-----------------------------------------------------------------------------------------------------------



Day 5 - RoBERTa Dataset Preparation



Created label mapping for legal clause categories.

Converted clause categories into numerical labels.

Prepared training data in RoBERTa-compatible format.

Generated:



* label\_mapping.json
* roberta\_train.json
* Developed the initial RoBERTa training pipeline structure.



Results:



* Total Legal Categories: 41
* Training Samples Prepared: 5361



Outcome:

* Prepared the dataset for transformer-based model training in Week 2.



\-------------------------------------------------------------------------------------------------------------------------------



Week 1 Summary



Files Created



* \* sample\_training.json
* \* training\_dataset.json
* \* train.json
* \* validation.json
* \* dataset\_statistics.json
* \* label\_mapping.json
* \* roberta\_train.json



Key Achievements



* \* Analyzed and processed the CUAD dataset.
* \* Generated 6702 structured training records.
* \* Prepared train and validation datasets.
* \* Created label mappings for legal clause classification.
* \* Prepared the complete NLP pipeline for RoBERTa model training.



Next Steps (Week 2)



* \* RoBERTa Model Fine-Tuning
* \* Clause Classification
* \* Model Evaluation
* \* Confidence Score Generation
* \* Risk Detection Pipeline Development



