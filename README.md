# **AADL–RA Component Mapping for IoT Systems**

This repository contains a curated dataset for studying and evaluating the mapping between **AADL architectural models** and a **Reference Architecture (RA)** for **IoT devices**.
It is designed to support research on **model alignment, architecture synthesis, and component-level correspondence** between system designs and a domain reference model.

The dataset provides:

* A formal **IoT Reference Architecture**
* A collection of **AADL system models**
* **Ground-truth mappings** between AADL components and RA components

---

## 📌 Repository Structure

```
.
├── RA/
│   ├── iot.ecore
│   ├── iot.gram
│   ├── iot_ra_component.txt
│   └── iot.png
│
├── AADL_models/
│   └── <model_name>.aaxl2
│
└── Component_mapping/
    ├── mapping_files/
    │   └── mapping_<model_name>.json
    └── mapping_png/
        └── mapping_<model_name>.png
```

---

## 📁 RA (Reference Architecture)

The **RA** folder defines the Reference Architecture for IoT systems.

| File                   | Description                                                                  |
| ---------------------- | ---------------------------------------------------------------------------- |
| `iot.ecore`            | The Ecore metamodel defining the structure of the IoT Reference Architecture |
| `iot.gram`             | Grammar file for parsing and processing the RA                               |
| `iot_ra_component.txt` | Textual description of the functionality of each RA component                |
| `iot.png`              | Visual diagram of the IoT Reference Architecture                             |

This RA represents a domain-level view of how IoT systems are structured and how responsibilities are distributed among components.

---

## 📁 AADL_models

This folder contains **AADL system models** in `.aaxl2` format.

Each file represents a concrete IoT system architecture expressed in AADL.

File naming convention:

```
<model_name>.aaxl2
```

Each model corresponds to a mapping file and a visualization in the `Component_mapping` folder.

---

## 📁 Component_mapping

This folder provides the **ground-truth alignment** between AADL models and the IoT Reference Architecture.

It contains two subfolders:

### 🔹 `mapping_files/`

JSON files describing how AADL components map to RA components.

Each file:

```
mapping_<model_name>.json
```

corresponds to:

```
AADL_models/<model_name>.aaxl2
```

These mappings explicitly state which AADL components implement or correspond to which RA components.

---

### 🔹 `mapping_png/`

Visual representations of the mappings.

Each PNG file:

```
mapping_<model_name>.png
```

is a graphical illustration of the JSON mapping, making it easier to understand the alignment between the system model and the reference architecture.

---

## 🎯 Purpose of the Dataset

This repository is intended for:

* Evaluating **architecture-to-RA mapping algorithms**
* Supporting **architecture synthesis and consistency checking**

The provided mappings are **manually curated ground truth**, enabling quantitative and qualitative evaluation of automated techniques.

