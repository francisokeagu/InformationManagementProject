# Library Management System - Installation Guide

This guide explains how to set up the Library Management System project on your local machine.

---

## 1. Requirements

- **Python 3.10 or later**
- `pip` package manager
- Optional: Virtual environment (recommended)

---

## 2. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-project-folder> 
```
---

## 3. Install Required Packages
Install all dependencies listed in requirements.txt:

```bash
pip install -r requirements.txt
```
Minimal requirements.txt includes:
```shell
pandas>=2.3
numpy>=2.3
kaggle>=1.7
SQLAlchemy>=2.0
```
---

## 4. Verify the Dataset

Ensure all CSV files are loaded correctly:
```bash 
python verify_dataset.py
```
You should see previews of all tables like books.csv, members.csv, etc.


## Notes

Ensure Python version is compatible with the packages listed.

After setup, your project is ready to run and further develop.
