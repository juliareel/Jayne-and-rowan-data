import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Database credentials
host = "cbdhrtd93854d5.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com"
database = "d3ukq1l0lc26bd"
port = "5432"
username = "uapst7uqgl9l0n"
password = "pfcd5ad7623fefef4cff01ee504b9d22aaca49bfe9d7ce2ff71231f0c995f6020"

# Create the database URL
db_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"

# Create a database connection using SQLAlchemy
engine = create_engine(db_url)

# Function to load data from your PostgreSQL database
# @st.cache  # This decorator caches the data for faster performance
def load_data():
    query = """
    -- Main, basic query to pull all invite list data, getting data for foreign key IDs
SELECT 
    invite_list.name,
    parties.party_name,
    invited_by_groups.group_name as invitatation_group,
    invite_list.response,
    CASE 
        WHEN invite_list.definite_invite = 1 THEN 'Yes'
        ELSE 'No'
    END AS definite_invite,
    partner_guest.name AS partner_name -- Getting the name of the partner guest
FROM invite_list
LEFT JOIN parties
ON invite_list.party_id = parties.party_id
LEFT JOIN invited_by_groups 
ON invite_list.invite_group_id = invited_by_groups.invite_group_id
LEFT JOIN invite_list AS partner_guest -- Self-join to get the partner's name
ON invite_list.partner_id = partner_guest.guest_id
order by party_name, invited_by_groups.group_name; """
    return pd.read_sql(query, engine)

# Streamlit app
st.title("Dashboard App")

# Load and display data
try:
    data = load_data()
    st.subheader("Data Overview")
    st.dataframe(data)
except Exception as e:
    st.error(f"Error loading data: {e}")

# Additional features (e.g., filters, visualizations, etc.)
st.subheader("Data Insights")
st.write(data.describe())

# You can add more Streamlit elements for interactivity and visualizations
