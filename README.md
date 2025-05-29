# 🛒 Retail.AI – Retail Recommendation & Analytics Web App

Retail.AI is a Flask-based web application that provides intelligent product recommendations and analytics for retail transactions. It uses **collaborative filtering**, **association rule mining**, and **sales trend analysis** to power a simple yet effective dashboard for understanding and improving product performance.

---

## 🚀 Features

- 📈 **Trending Items** – View items with the highest recent sales growth.
- 🤝 **Frequently Bought Together** – Association rule mining using the Apriori algorithm.
- 🧠 **Item-Based Recommendations** – Similar item suggestions via cosine similarity.
- 📊 **Sales Visualization** – Interactive chart of recommended items’ sales.

---

## 🗂️ Project Structure


---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/retail.AI.git
cd retail.AI
### Create and activate a virtual environment (recommended
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
### Install dependencies
pip install -r requirements.txt

## 🧪 Running the App
Step 1: Ensure retail.csv is present in the root directory
This file should contain at least the following columns:

bill_id

item_id

item_name

quantity

date

## Step 2: Start the Flask app
python run.py
## Step 3: Open your browser
Go to: http://127.0.0.1:8000 

📚 How It Works
🔹 Data Loading & Preprocessing
Loads retail transactions and groups items per bill.

Cleans and formats item IDs and names.

🔹 Item Similarity (Collaborative Filtering)
Creates a user-item matrix using CountVectorizer.

Calculates item-item cosine similarity for recommendations.

🔹 Association Rule Mining
Uses the Apriori algorithm to find frequently co-purchased item sets.

Generates association rules based on lift metric.

🔹 Trending Items
Aggregates item sales per day.

Computes sales growth rate to identify trending products.

🔹 Web Routes
/ → Homepage: shows trending items, top rules.

/recommend → Form submission: shows similar items and their sales data.

📊 Sample Dashboard (What You See)
✅ Top trending items with growth rate

✅ Most frequent itemsets

✅ Enter an item ID → Get similar items & a sales chart


🧠 Technologies Used
Tool	Purpose
Flask	Web framework
Pandas	Data manipulation
scikit-learn	Cosine similarity (collaborative filtering)
mlxtend	Apriori & association rule mining
HTML/CSS	Frontend (via Jinja templates)
Chart.js	(Optional) Frontend chart visualization

📁 Example Retail Dataset Format
bill_id	item_id	item_name	quantity	date
101	A101	Sugar	2	2023-10-01
101	B205	Tea	1	2023-10-01
102	A101	Sugar	1	2023-10-02

🤝 Contributing
Feel free to fork the repo, raise issues, or submit pull requests.

📜 License
MIT License. See LICENSE file for details.

👤 Author
Umair Abbas

