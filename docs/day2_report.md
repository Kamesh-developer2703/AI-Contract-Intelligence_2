# Day 2 Report

**Date:** 09/06/2026

**Project:** AI-Powered Contract Intelligence & Risk Scoring

**Team Member:** Kameshwaran

## Objective

Analyze the CUAD dataset structure and understand how legal clauses are represented for machine learning training.

## Tasks Completed

### 1. Explored CUAD Dataset Structure

* Loaded the CUAD dataset JSON file.
* Analyzed the dataset hierarchy.
* Identified key fields:

  * version
  * data
  * title
  * paragraphs
  * qas
  * context

### 2. Examined Contract Information

* Explored contract titles.
* Analyzed paragraph structure.
* Verified contract text storage inside the context field.

### 3. Analyzed Question-Answer Format

* Examined the qas section.
* Identified legal clause categories represented as questions.
* Studied answer annotations associated with each clause.

### 4. Verified Dataset Statistics

* Dataset Version: aok_v1.0
* Total Contracts: 510
* Legal Categories: 41

### 5. Understanding Data for NLP Training

* Understood how contract clauses can be converted into training samples.
* Identified clause type and clause text relationships.
* Planned preprocessing strategy for dataset preparation.

## Results

* Successfully explored the CUAD dataset.
* Understood contract structure and annotations.
* Identified fields required for preprocessing.
* Prepared for training dataset creation.

## Files Used

* data/cuad/CUADv1.json
* notebooks/explore_dataset.py

## Status

✅ Dataset Structure Understood

✅ Contract Data Verified

✅ Question-Answer Format Analyzed

✅ Ready for Dataset Preprocessing

## Next Steps

* Extract contract titles.
* Extract clause categories.
* Generate structured training records.
* Create training_dataset.json for machine learning.
