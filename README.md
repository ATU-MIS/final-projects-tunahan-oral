# 💎 FinTrack Pro Elite | Personal Financial Decision Support System

FinTrack Pro is a high-end, full-stack financial management application developed as a final project. It is designed to help users track their financial goals, manage daily transactions, and receive AI-driven advice through a Virtual Financial Advisor engine.

## 🌟 Key Features

-   **Strategic Executive Dashboard:** Interactive data visualization using Plotly to track goal achievement rates and net assets.
-   **Virtual Financial Advisor:** An OOP-based decision engine that analyzes income/expense ratios to provide feasibility reports.
-   **Expense & Income Ledger:** A structured tracking module to record and categorize financial movements.
-   **Algorithmic Reporting:** Generation of "Financial Health Scores" and spending distribution analysis through advanced analytics.
-   **Data Persistence:** Integrated SQLite database layer ensuring all user data is stored securely and locally.

## 🏗️ Technical Architecture (UML Compliance)

The software is built on a layered architecture, strictly adhering to the provided UML Design Documents:

1.  **Domain Layer (OOP):** Implementation of `User`, `FinancialGoal`, `Transaction`, and `Advisor` classes to manage business logic.
2.  **Data Layer:** Relational database management using SQLite for persistence.
3.  **UI Layer:** Modern, responsive frontend built with Streamlit and CSS-injection for an elite user experience.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Pip (Python Package Manager)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ATU-MIS/se-projects1-tunahan-oral.git
2. Install the required engineering libraries:
   
   pip install streamlit pandas plotly

3. Launch the application:
   python -m streamlit run main.py

📂 Project Structure
├── main.py              # Full-stack Application Logic
├── proje_final.db       # Relational SQLite Database (Auto-generated)
├── README.md            # Project Documentation
├── requirements.txt     # Dependency List
├── FinTrack_Baslatici.bat # One-click Launcher
└── docs/                # SRS Documents and UML Diagrams


Developer: Tunahan Oral

Course: Software Engineering / Final Project

Status: Version 1.0 (Stable)