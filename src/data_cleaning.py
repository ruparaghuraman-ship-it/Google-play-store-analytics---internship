from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'data'

def clean_installs(value):
    if pd.isna(value): return np.nan
    return pd.to_numeric(str(value).replace(',','').replace('+','').strip(), errors='coerce')

def clean_size(value):
    if pd.isna(value): return np.nan
    value=str(value).strip()
    if value.lower()=='varies with device': return np.nan
    if value.lower().endswith('m'): return pd.to_numeric(value[:-1], errors='coerce')
    if value.lower().endswith('k'): return pd.to_numeric(value[:-1], errors='coerce')/1024
    return pd.to_numeric(value, errors='coerce')

def load_data():
    apps=pd.read_csv(DATA_DIR/'Play Store Data.csv')
    reviews=pd.read_csv(DATA_DIR/'User Reviews.csv')
    apps=apps.drop_duplicates(subset=['App']).copy()
    apps['Installs_Num']=apps['Installs'].map(clean_installs)
    apps['Size_MB']=apps['Size'].map(clean_size)
    apps['Reviews_Num']=pd.to_numeric(apps['Reviews'], errors='coerce')
    apps['Rating_Num']=pd.to_numeric(apps['Rating'], errors='coerce')
    apps['Last Updated']=pd.to_datetime(apps['Last Updated'], errors='coerce')
    apps['Price_Num']=pd.to_numeric(apps['Price'].astype(str).str.replace('$','',regex=False), errors='coerce').fillna(0)
    apps['Revenue']=np.where(apps['Type'].astype(str).str.lower().eq('paid'), apps['Price_Num']*apps['Installs_Num'], 0.0)
    for c in ['Sentiment_Subjectivity','Sentiment_Polarity']:
        reviews[c]=pd.to_numeric(reviews[c],errors='coerce')
    stats=reviews.groupby('App').agg(Mean_Subjectivity=('Sentiment_Subjectivity','mean'),Mean_Polarity=('Sentiment_Polarity','mean')).reset_index()
    return apps.merge(stats,on='App',how='left'), reviews
