import streamlit as st
import pandas as pd

st.title("🚗 Car Sharing Dashboard")
st.write("This is where the dashboard for the car sharing dataset will go.")


# Function to load CSV files into dataframes
@st.cache_data
def load_data():
    cars = pd.read_csv("datasets/cars.csv")
    trips = pd.read_csv("datasets/trips.csv")
    cities = pd.read_csv("datasets/cities.csv")
    return cars, trips, cities

cars_df, trips_df, cities_df = load_data()

st.write("Cars dataset", cars_df.head())
st.write("Trips dataset", trips_df.head())
st.write("Cities dataset", cities_df.head())


st.write("Colonnes de trips_df:", trips_df.columns)
st.write("Colonnes de cars_df:", cars_df.columns)

# Fusionner trips avec cars en adaptant les clés de jointure
trips_df_merged = trips_df.merge(cars_df, left_on='car_id', right_on='id', how='left')

# Fusionner trips_merged avec cities
trips_df_merged = trips_df_merged.merge(cities_df, on='city_id', how='left')

# Vérifier la fusion
st.write("Aperçu des données fusionnées :", trips_df_merged.head())


# Supprimer les colonnes ID inutiles après la fusion
cols_to_drop = ["id_x", "id_y", "car_id", "city_id", "customer_id"]

# Vérifier quelles colonnes existent avant de les supprimer
existing_cols_to_drop = [col for col in cols_to_drop if col in trips_df_merged.columns]

# Supprimer uniquement les colonnes qui existent
trips_df_merged = trips_df_merged.drop(columns=existing_cols_to_drop)

# Vérifier après suppression
st.write("Aperçu des colonnes après nettoyage:", trips_df_merged.head())




# Convertir pickup_time et dropoff_time en datetime
trips_df_merged["pickup_time"] = pd.to_datetime(trips_df_merged["pickup_time"])
trips_df_merged["dropoff_time"] = pd.to_datetime(trips_df_merged["dropoff_time"])

# Créer une nouvelle colonne "pickup_date" en extrayant uniquement la date
trips_df_merged["pickup_date"] = trips_df_merged["pickup_time"].dt.date

# Vérifier si la transformation a bien fonctionné
st.write("Aperçu des données après conversion :", trips_df_merged[["pickup_time", "dropoff_time", "pickup_date"]].head())


selected_brand = st.sidebar.selectbox(
    "Select a Car Brand", 
    options=["All"] + list(trips_df_merged["brand"].unique()),  # Option "All" pour tout afficher
)

# Filtrer si une marque spécifique est sélectionnée
if selected_brand != "All":
    trips_df_merged = trips_df_merged[trips_df_merged["brand"] == selected_brand]


# Calculer le nombre total de trajets
total_trips_df = trips_df_merged.shape[0]  # Nombre total de lignes (chaque ligne = 1 trajet)

# Calculer la distance totale parcourue
total_distance = trips_df_merged["distance"].sum()  # Somme de la colonne "distance"

# Trouver le modèle de voiture ayant généré le plus de revenus
top_car_df = (
    trips_df_merged.groupby("model")["revenue"]
    .sum()
    .idxmax()
)  # Regroupe par modèle, somme des revenus, trouve le max

# Afficher les métriques dans 3 colonnes
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Trips", value=total_trips_df)

with col2:
    st.metric(label="Top Car Model by Revenue", value=top_car_df)

with col3:
    st.metric(label="Total Distance (km)", value=f"{total_distance:,.2f}")
























