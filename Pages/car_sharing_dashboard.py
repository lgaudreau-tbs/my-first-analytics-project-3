import streamlit as st
import pandas as pd

st.title("🚗 Car Sharing Dashboard")
st.write("This is where the dashboard for the car sharing dataset will go.")


@st.cache_data
def load_data():
    cars = pd.read_csv("datasets/cars.csv")
    trips = pd.read_csv("datasets/trips.csv")
    cities = pd.read_csv("datasets/cities.csv")
    return cars, trips, cities

cars_df, trips_df, cities_df = load_data()



trips_df_merged = trips_df.merge(cars_df, left_on='car_id', right_on='id', how='left')
trips_df_merged = trips_df_merged.merge(cities_df, on='city_id', how='left')

cols_to_drop = ["id_x", "id_y", "car_id", "city_id", "customer_id"]
existing_cols_to_drop = [col for col in cols_to_drop if col in trips_df_merged.columns]
trips_df_merged = trips_df_merged.drop(columns=existing_cols_to_drop)


trips_df_merged["pickup_time"] = pd.to_datetime(trips_df_merged["pickup_time"])
trips_df_merged["dropoff_time"] = pd.to_datetime(trips_df_merged["dropoff_time"])
trips_df_merged["pickup_date"] = trips_df_merged["pickup_time"].dt.date


selected_brand = st.sidebar.selectbox(
    "Select a Car Brand", 
    options=["All"] + list(trips_df_merged["brand"].unique()), 
)

if selected_brand != "All":
    trips_df_merged = trips_df_merged[trips_df_merged["brand"] == selected_brand]


total_trips_df = trips_df_merged.shape[0]  

total_distance = trips_df_merged["distance"].sum()  

top_car_df = (
    trips_df_merged.groupby("model")["revenue"]
    .sum()
    .idxmax()
) 

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Trips", value=total_trips_df)

with col2:
    st.metric(label="Top Car Model by Revenue", value=top_car_df)

with col3:
    st.metric(label="Total Distance (km)", value=f"{total_distance:,.2f}")


st.write("### Preview of the Merged Trips DataFrame")
st.write(trips_df_merged.head())


if not trips_df_merged.empty:

    # 📈 1. **Nombre de trajets au fil du temps (Trips Over Time)**
    trips_df_over_time = trips_df_merged.groupby("pickup_date").size().reset_index(name="total_trips")
    st.subheader("📊 Trips Over Time")
    st.line_chart(trips_df_over_time.set_index("pickup_date"))

    # 🚗 2. **Revenu par modèle de voiture (Revenue Per Car Model)**
    revenue_per_model = trips_df_merged.groupby("model")["revenue"].sum().reset_index()
    st.subheader("💰 Revenue Per Car Model")
    st.bar_chart(revenue_per_model.set_index("model"))

    # 📊 3. **Croissance du revenu cumulée (Cumulative Revenue Growth Over Time)**
    revenue_over_time = trips_df_merged.groupby("pickup_date")["revenue"].sum().cumsum().reset_index()
    st.subheader("📈 Cumulative Revenue Growth Over Time")
    st.area_chart(revenue_over_time.set_index("pickup_date"))

    # 🚀 **Bonus : Nombre de trajets par modèle de voiture**
    trips_df_per_model = trips_df_merged["model"].value_counts().reset_index()
    trips_df_per_model.columns = ["model", "trip_count"]
    st.subheader("🚘 Number of Trips Per Car Model")
    st.bar_chart(trips_df_per_model.set_index("model"))

else:
    st.write("⚠️ No data available for visualization. Check your dataset loading and filtering.")


























