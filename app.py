import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample District Rainfall Data (in mm)
district_rainfall = {
    "Kathmandu": 1360,
    "Pokhara": 3900,
    "Biratnagar": 1550,
    "Nepalgunj": 1302,
    "Butwal": 1827,
    "Dhangadhi": 1500,
    "Jumla": 850,  # Estimate; actual data varies by region
    "Dharan": 1416,
    "Dhankuta": 1810,
    "Ilam": 2552,
    "Bhojpur": 2290,
    "Khandbari": 2041,
    "Bhadrapur": 2352,
    "Damak": 2618,
    "Khumbu Pasang Lhamu": 645,
    "Gaur": 1590,
    "Siraha": 1293,
    "Birgunj": 1862,
    "Jaleshwar": 1493,
    "Malangawa": 1818,
    "Janakpur": 1517,
    "Rajbiraj": 1223,
    "Lahan": 1231,
    "Hetauda": 2069,
    "Bharatpur": 2550,
    "Banepa": 1931,
    "Suryabinayak": 1822,
    "Kirtipur": 2101,
    "Gorkha": 2500,
    "Baglung": 2200,
    "Lamjung": 2300,
    "Syangja": 2100,
    "Tanahun": 2400,
    "Gulariya": 1504,
    "Siddharthanagar": 1763,
    "Tansen": 1949,
    "Tulsipur": 1495,
    "Sitganga": 1633,
    "Birendranagar": 1651,
    "Narayan": 1252,
    "Chandannath": 729,
    "Simikot": 304,
    "Kharpunath": 210,
    "Bajura": 13433,  # This seems unusually high; may need validation
    "Dadeldhura": 1200,
    "Mahendranagar": 1800,
    "Doti": 1100,
}

# Function to calculate rainwater collected (liters)
def calculate_rainwater(roof_area, rainfall, runoff_coeff):
    # Convert rainfall from mm to m and then calculate the volume in liters
    rainwater = roof_area * rainfall * runoff_coeff * 0.001
    return rainwater

# Function to calculate storage tank size (liters)
def calculate_storage_tank(family_size, dry_days, daily_usage_per_person=50):
    # Assuming daily usage per person is 50 liters
    storage_tank_size = family_size * daily_usage_per_person * dry_days
    return storage_tank_size

# Set up Streamlit UI
st.title("Rainwater Harvesting Planner")

# Roof Area Input (in m²)
roof_area = st.number_input("Enter Roof Area (m²):", min_value=1)

# District or Manual Rainfall Input
rainfall_option = st.radio("Select Rainfall Input Type:", ("District-based", "Manual"))

if rainfall_option == "District-based":
    district = st.selectbox("Select District:", list(district_rainfall.keys()))
    rainfall = district_rainfall[district]
    st.write(f"Selected District: {district} | Average Rainfall: {rainfall} mm")
else:
    rainfall = st.number_input("Enter Rainfall (mm):", min_value=0)

# Runoff Coefficient Selection (based on roof type)
roof_type = st.selectbox("Select Roof Type:", ["Concrete", "Metal Sheet", "Tile", "Asphalt"])
if roof_type == "Concrete":
    runoff_coeff = 0.8
elif roof_type == "Metal Sheet":
    runoff_coeff = 0.9
elif roof_type == "Tile":
    runoff_coeff = 0.75
else:
    runoff_coeff = 0.7

st.write(f"Runoff Coefficient for {roof_type} roof: {runoff_coeff}")

# Family Size and Dry Days Input
family_size = st.number_input("Enter Family Size:", min_value=1, max_value=20, value=4)
dry_days = st.number_input("Enter Number of Dry Days:", min_value=1, max_value=365, value=30)

# Calculate the rainwater collected and tank size
rainwater_collected = calculate_rainwater(roof_area, rainfall, runoff_coeff)
storage_tank_size = calculate_storage_tank(family_size, dry_days)

# Display results
st.write(f"Total Rainwater Collected: {rainwater_collected:.2f} Liters per Year")
st.write(f"Recommended Storage Tank Size: {storage_tank_size} Liters")

# Plot the Rainwater Collected vs Household Need (dry days and family size)
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(["Rainwater Collected", "Household Need"], [rainwater_collected, storage_tank_size])
ax.set_ylabel("Liters")
ax.set_title("Rainwater Collected vs Household Need")
st.pyplot(fig)

# Downloadable Report
st.subheader("Download Your Report")
data = {
    "Roof Area (m²)": [roof_area],
    "Rainfall (mm)": [rainfall],
    "Runoff Coefficient": [runoff_coeff],
    "Family Size": [family_size],
    "Dry Days": [dry_days],
    "Total Rainwater Collected (Liters)": [rainwater_collected],
    "Recommended Storage Tank Size (Liters)": [storage_tank_size],
}

df = pd.DataFrame(data)
csv = df.to_csv(index=False)
st.download_button(
    label="Download Report as CSV",
    data=csv,
    file_name="rainwater_harvesting_report.csv",
    mime="text/csv",
)

# Optional: Generate PDF report (Advanced feature)
