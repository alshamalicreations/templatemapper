# 🏥 IonClinic Excel Tool

A professional desktop application for migrating Excel-based clinic data into the **IonClinic Backup** format.

IonClinic Excel Tool automatically detects patient records, treatment history, payment history, and other clinic data from Excel workbooks, converts them into the IonClinic backup schema, validates the data, and generates a ready-to-import backup file.

---

## ✨ Features

### 📂 Excel Processing

- Read Excel workbooks (`.xlsx`)
- Automatically detect worksheet types
- Analyze workbook structure
- Preview detected data before migration

### 👤 Patient Migration

- Import patient records
- Generate unique patient IDs (UUIDs)
- Preserve patient relationships
- Clean and validate patient information

### 📅 Appointment Migration

- Import treatment history
- Convert treatments into appointments
- Preserve appointment dates
- Link appointments to patients

### 💳 Payment Migration

- Import payment history
- Calculate total paid
- Calculate remaining balance
- Preserve payment methods and payment dates

### ✅ Data Validation

- Detect duplicate patients
- Detect invalid phone numbers
- Detect invalid dates
- Detect missing required fields
- Generate validation reports
- Automatically clean common data issues

### 📄 Export

- Generate IonClinic-compatible backup
- Export migration reports
- Save migration logs
- Preserve workbook integrity

---

# 🚀 Version Roadmap

## Version 1.0

- ✅ Derma Excel Migration
- ✅ Patient Import
- ✅ Appointment Import
- ✅ Payment Import
- ✅ Backup Export

---

## Version 1.1

- Custom Excel Mapping
- User-defined column mapping
- Save mapping profiles

---

## Version 1.2

- Drag & Drop Excel Files
- Batch Processing
- Faster Import Engine

---

## Version 1.3

- Arabic Interface
- English Interface
- Theme Support

---

## Version 2.0

### Plugin System

Supported Importers:


- DentalSoft
- EasyClinic
- Custom Excel Importers

---

# 🛠️ Technologies

- Python
- PySide6
- OpenPyXL
- Pandas
- RapidFuzz
- Loguru

---

# 📌 Project Status

🚧 **Currently under active development**

The first release focuses on migrating Derma Excel workbooks into the IonClinic Backup format.

---

# 🤝 Contributing

Contributions, bug reports, feature requests, and suggestions are welcome.

If you'd like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a Pull Request.

---

# 📄 License

This project is licensed under the **MIT License**.

---

# ⭐ Support

If you find this project useful, please consider giving it a **⭐ Star** on GitHub.

It helps others discover the project and supports future development.