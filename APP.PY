from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from mlxtend.frequent_patterns import apriori, association_rules

app = Flask(__name__)

def load_data():
    # Load the dataset
    df = pd.read_csv('retail.csv')

    # Convert item_id and bill_id to strings
    df['item_id'] = df['item_id'].astype(str)
    df['bill_id'] = df['bill_id'].astype(str)

    # Create a mapping of item_id → item_name
    item_name_map = df[['item_id', 'item_name']].drop_duplicates().set_index('item_id')['item_name'].to_dict()

    # Group transactions by bill_id
    transactions = df.groupby('bill_id')['item_id'].apply(list).reset_index()

    # Collaborative Filtering - Item Similarity
    vectorizer = CountVectorizer(tokenizer=lambda x: x, lowercase=False)
    user_item_matrix = vectorizer.fit_transform(transactions['item_id'])
    item_similarity = cosine_similarity(user_item_matrix.T)
    item_similarity_df = pd.DataFrame(
        item_similarity, 
        index=vectorizer.get_feature_names_out(), 
        columns=vectorizer.get_feature_names_out()
    )

    # Association Rule Mining
    transactions_encoded = pd.get_dummies(transactions['item_id'].apply(pd.Series).stack()).groupby(level=0).max()
    transactions_encoded = transactions_encoded.fillna(0).astype(int)
    frequent_itemsets = apriori(transactions_encoded, min_support=0.01, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

    # Trending Items
    df['date'] = pd.to_datetime(df['date'])
    item_trends = df.groupby(['item_id', pd.Grouper(key='date', freq='D')])['quantity'].sum().reset_index()
    item_trends['growth_rate'] = item_trends.groupby('item_id')['quantity'].pct_change()
    trending_items = item_trends.sort_values(by='growth_rate', ascending=False).head(10)

    # Add item names to trending items
    trending_items['item_name'] = trending_items['item_id'].map(item_name_map)

    return df, item_similarity_df, rules, trending_items, item_name_map

# Load data
df, item_similarity_df, rules, trending_items, item_name_map = load_data()
@app.route('/')
def index():
    return render_template(
        'index.html',
        trending_items=trending_items.to_dict(orient='records'),
        rules=rules.head(5).to_dict(orient='records'),
        similar_items={},
        sales_data={}  # Pass empty sales data initially
    )

@app.route('/recommend', methods=['POST'])
def recommend():
    item_id = request.form.get('item_id')

    if not item_id:
        return render_template(
            'index.html',
            error='Please enter a valid Item ID.',
            trending_items=trending_items.to_dict(orient='records'),
            rules=rules.head(6).to_dict(orient='records'),
            similar_items={},
            sales_data={}  # Pass empty sales data
        )

    try:
        # Convert input to string to match DataFrame index
        item_id = str(item_id)

        if item_id not in item_similarity_df.index:
            raise KeyError

        # Get similar items
        similar_items_scores = item_similarity_df[item_id].sort_values(ascending=False)[1:7]

        # Get names of recommended items
        similar_items = [
            {"item_id": idx, "item_name": item_name_map.get(idx, "Unknown"), "similarity": round(score, 2)}
            for idx, score in similar_items_scores.items()
        ]

        # Filter sales data for recommended items
        recommended_item_ids = [item['item_id'] for item in similar_items]
        recommended_sales = df[df['item_id'].isin(recommended_item_ids)]

        # Aggregate sales by item_id
        sales_by_item = recommended_sales.groupby('item_id')['quantity'].sum().reset_index()

        # Map item_id to item_name
        sales_by_item['item_name'] = sales_by_item['item_id'].map(item_name_map)

        # Convert sales data to a format suitable for Chart.js
        sales_data = {
            "labels": sales_by_item['item_name'].tolist(),
            "quantities": sales_by_item['quantity'].tolist()
        }

        return render_template(
            'index.html',
            similar_items=similar_items,
            trending_items=trending_items.to_dict(orient='records'),
            rules=rules.head(5).to_dict(orient='records'),
            sales_data=sales_data  # Pass sales data to the template
        )

    except KeyError:
        return render_template(
            'index.html',
            error=f'Item ID "{item_id}" not found. Try another one.',
            trending_items=trending_items.to_dict(orient='records'),
            rules=rules.head(5).to_dict(orient='records'),
            similar_items={},
            sales_data={}  # Pass empty sales data
        )
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001)