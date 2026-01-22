# 💰 FinTrack Pro - Personal Financial Management System

FinTrack Pro is a desktop-based financial tracking application developed as a final project for the Software Engineering course. It allows users to record daily expenses, set financial savings goals, and track their progress through interactive charts.

This project is built with Python and Streamlit, designed to run locally without requiring complex installation steps.

## 🎯 Key Features

* **Dashboard:** A visual summary of total savings and financial goals using Plotly charts.
* **Virtual Advisor:** A built-in algorithm that calculates the necessary monthly savings to reach specific financial targets.
* **Expense Tracking:** Simple module to record daily expenses by category (e.g., Food, Transport).
* **Data Persistence:** All user data is securely stored locally in a `proje_final.db` (SQLite) file.

## 🛠️ Tech Stack

The project follows the architecture defined in the UML diagrams and Requirements Analysis (SRS) document:

* **Language:** Python 3.10+
* **UI Framework:** Streamlit (Running in "App Mode" for a desktop-like experience)
* **Database:** SQLite (Chosen for its portability and zero-configuration)
* **Visualization:** Plotly & Pandas

## 🚀 Installation & Usage

To run the project on your local machine, follow these steps:

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Application:**
    ```bash
    python run_app.py
    ```
    *(Note: The application will launch in a dedicated window without browser tabs, thanks to the custom launcher script.)*

## 📂 Project Structure

* `main.py`: The core application logic and UI code.
* `run_app.py`: A script to launch the Streamlit app as a standalone desktop window.
* `proje_final.db`: Local SQLite database file.
* `requirements.txt`: List of required Python libraries.
* `docs/`: Contains project documentation (SRS Report and Usability Test Results).

---
**Developer:** Tunahan Oral
**Course:** Software Engineering / Final Project
**Student ID:** 2220202043
