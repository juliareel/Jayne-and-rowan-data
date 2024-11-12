import pandas as pd
from sqlalchemy import create_engine

# Database credentials
host = "cbdhrtd93854d5.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com"
database = "d3ukq1l0lc26bd"
port = "5432"
username = "uapst7uqgl9l0n"
password = "pfcd5ad7623fefef4cff01ee504b9d22aaca49bfe9d7ce2ff71231f0c995f6020"

# Create the database URL and connection
db_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(db_url)

def execute_query(query):
    return pd.read_sql(query, engine)

def load_invite_groups():
    query = "SELECT group_name FROM invited_by_groups"
    return pd.read_sql(query, engine)['group_name'].tolist()

def load_parties():
    query = "SELECT party_name FROM parties ORDER BY party_id"
    return pd.read_sql(query, engine)['party_name'].tolist()
