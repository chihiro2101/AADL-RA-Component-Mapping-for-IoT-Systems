# Experimental Procedure / Data Collection Protocol

This document describes the experimental procedure used to collect human judgments for validating the ground-truth mappings between **AADL models** and the **IoT Reference Architecture (RA)**.

---

## 1. Objective

The objective of this experiment is to **collect reliable human judgments** for validating model–RA component mappings that are used as **ground truth** in subsequent experiments.

---

## 2. Experimental Setting

* Data collection is conducted **remotely** using an online spreadsheet (**Google Sheets**).
* Participants complete the validation task **independently**, without communication with other participants.
* No time limit is enforced, although the expected completion time is approximately **1 hour**.

---

## 3. Materials

### 3.1 Validation Spreadsheet

The main material is a Google Spreadsheet in which **each row corresponds to a single model–RA component mapping**.
**Google Spreadsheet:**
[https://docs.google.com/spreadsheets/d/1apI68NZzbwQeexx5ArsLfPgPYNi1pvvZiL1uL-2vijE/edit?usp=sharing](https://docs.google.com/spreadsheets/d/1apI68NZzbwQeexx5ArsLfPgPYNi1pvvZiL1uL-2vijE/edit?usp=sharing)

For each mapping, the following information is provided:

* `AADL_model`: name of the AADL model
* `AADL_node_name`: name of the AADL component
* `IOT_RA_component`: name of the corresponding RA component(s)
* `graphical_illustration`: link to a visual illustration of the mapping
* `Validation_status`: annotation field with three possible values
  (`Correct`, `Incorrect`, `Uncertain`)
* `Correction_suggestion`: optional free-text field for comments or alternative mappings

### 3.2 RA Component Description Sheet

The spreadsheet includes an additional sheet named **`iot_ra_components_description`**, which contains:

* A list of all IoT RA components
* A short functional description for each RA component
* A visual illustration of the IoT Reference Architecture

This sheet is provided to support a **consistent understanding of RA semantics** among participants.

### 3.3 Instruction Material

Participants are provided with a short written instruction document that defines
the annotation criteria and explains how to complete the validation task.

The instruction material includes:
- Clear definitions of what is a *correct* versus *incorrect* mapping
- Common examples and edge cases
- Step-by-step instructions on how to record validation decisions in the spreadsheet

The full instruction document is available in:
**[Annotation Guidelines](ANNOTATION_GUIDELINES.md)**

---

## 4. Workload Distribution

* The full dataset consists of **187 mappings**.
* The mappings are divided into **four batches**, each containing approximately **40–50 mappings**.
* Each participant is assigned **exactly one batch**.
* A total of **12 participants** take part in the study.
* Each batch is validated by **three independent participants**, resulting in **three judgments per mapping**.

---

## 5. Procedure

### 5.1 Recruitment and Consent

Participants receive a written description of the study, including:

* The purpose of the experiment
* The expected completion time (approximately **30–60 minutes**)

Participants provide **informed consent** before starting the task.

---

### 5.2 Briefing and Instruction

Before beginning the task, participants are provided with:

* A brief overview of the **goal of the validation task**
* An explanation of:

  * AADL model components
  * IoT RA components
  * The intended interpretation of model–RA mappings
* Practical instructions on:

  * How to use the Google Spreadsheet
  * How to access RA descriptions, AADL models, and graphical illustrations

Participants are required to read the **[Annotation Guidelines](ANNOTATION_GUIDELINES.md)**, which define:

* The criteria for *Correct*, *Incorrect*, and *Uncertain* mappings
* Common examples and edge cases
* How to record validation decisions in the spreadsheet

---

### 5.3 Main Validation Task

For each assigned mapping, participants perform the following steps:

* Review the mapping information provided in the spreadsheet
* Consult, when needed:

  * The RA component descriptions
  * The IoT Reference Architecture visualization
  * The corresponding AADL model file
  * The graphical mapping illustration
* Select one value in the **`Validation_status`** column:

  * `Correct`
  * `Incorrect`
  * `Uncertain`
* Optionally provide a brief explanation or suggest an alternative RA component in the **`Correction_suggestion`** column, especially for *Incorrect* or *Uncertain* cases

Participants are instructed to base their decisions on **functional responsibility**, rather than naming similarity.

---

### 5.4 Debriefing

After completing the task, participants may provide feedback on:

* Unclear or difficult mappings
* Ambiguities in the annotation guidelines
* General comments on the task or materials

---

## 6. Data Aggregation

* Each mapping receives **three independent judgments**.
* The final label for each mapping is determined using **majority voting**.
* Mappings with:

  * High disagreement, or
  * A majority of `Uncertain` labels
    are **flagged for manual inspection** by the authors.

---

## 7. Quality Assurance

* A small number of **straightforward mappings** may be included to detect random or inconsistent answers.
* Participant responses are reviewed to ensure basic consistency before aggregation.

---

## 8. Outcome

The result of this procedure is a **validated and reliable ground-truth dataset** that can be confidently used for:

* Experimental evaluation
* Benchmarking mapping approaches
* Further analysis of model–RA alignment techniques