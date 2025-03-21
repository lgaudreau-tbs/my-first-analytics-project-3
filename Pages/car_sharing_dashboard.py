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



















