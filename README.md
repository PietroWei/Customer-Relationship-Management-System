# 📊 Customer Relationship Management (CRM) System

## 🔍 Project Overview
This project is a **Customer Relationship Management (CRM) System** that allows businesses to:
- Manage **customer interactions** (emails, calls, meetings).
- Track **leads and sales history**.
- Analyze **high-value customers** using **PostgreSQL**.
- Visualize insights in **Power BI**.

## 🏗️ Features
- **Database Design**: PostgreSQL schema for customers, leads, interactions, and sales.
- **Data Generation**: Python script to generate and insert realistic CRM data.
- **Data Analysis**: SQL queries for customer engagement and sales performance.
- **Dashboarding**: Power BI for visual analytics.

---

## 🛠️ Installation
### 1️⃣ Install PostgreSQL
Download and install [PostgreSQL](https://www.postgresql.org/download/). During setup:
- Set a **username** (default: `postgres`).
- Set a **password** (remember it for later!).

### 2️⃣ Clone This Repository
```sh
git clone https://github.com/pietrowei/crm_project.git
cd crm_project
```

### 3️⃣ Install Python Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up the Database
Create a new PostgreSQL database:
```sql
CREATE DATABASE crm_db;
```

### 5️⃣ Configure Environment Variables
Create a `.env` file in the project root and add:
```
DB_NAME=crm_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

**⚠️ Important**: Do not commit `.env` to GitHub! It's ignored in `.gitignore`.

### 6️⃣ Run the Data Generation Script
```sh
python scripts/generate_data.py
```

---

## 📊 Power BI Dashboard
- Open `dashboards/crm_dashboard.pbix` in **Power BI**.
- Connect it to your **PostgreSQL database**.
- Refresh the data to visualize insights!

---

## 📌 SQL Queries for Insights
Example: Find **top 10 customers by revenue**:
```sql
SELECT c.name, SUM(s.amount) AS total_spent
FROM customers c
JOIN sales_history s ON c.id = s.customer_id
GROUP BY c.name
ORDER BY total_spent DESC
LIMIT 10;
```

---

## 🚀 Future Enhancements
- Web-based CRM dashboard (Django/Flask).
- Customer churn prediction with Machine Learning.
- More advanced Power BI visualizations.

---

## 📝 License
This project is open-source and available under the **MIT License**.

---

## 🤝 Contributing
Pull requests are welcome! Feel free to improve the project.

📩 Questions? Contact me at [pietrogazzi01@gmail.com].

