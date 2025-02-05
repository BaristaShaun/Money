import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define the environmental impact data
data = {
    "Environmental Impact": [
        "Climate Change", "Ozone Depletion", "Human Toxicity (Cancer)",
        "Human Toxicity (Non-Cancer)", "Particulate Matter", "Ionizing Radiation",
        "Photochemical Ozone Formation", "Acidification", "Eutrophication (Marine)",
        "Eutrophication (Freshwater)", "Water Use", "Resource Use (Minerals/Metals)"
    ],
    "Unit": [
        "kg CO2 eq", "kg CFC-11 eq", "CTUh", "CTUh", "Disease incidences",
        "kBg U235 eq", "kg NMVOC eq", "mol H+ eq", "kg N eq", "kg P eq", "m³", "kg Sb eq"
    ],
    "Minimum Value": [
        0.042, 0.008, 7.04E+05, 1.53E+05, 7.98E+05,
        1.22E-03, 2.30E-03, 3.50E-01, 1.94, 2.15E-01, 2.15E-01, 1.65E+00
    ],
    "Maximum Value": [
        0.685, 461, 9.19E+05, 1.66E+05, 7.98E+05,
        1.01E+00, 1.84E+01, 3.50E-01, 12.8, 1.96, 2.15E-01, 1.92E+04
    ],
    "Average Value": [
        0.3635, 230.504, 811500, 159500, 798000,
        0.50561, 9.20115, 0.35, 7.37, 1.0875, 0.215, 9600.825
    ]
}

df = pd.DataFrame(data)

st.title("Environmental Impact Cost Calculator")
st.markdown(
    "**Note:** Ensure that you conduct LCA using the 'EF3.1 method' and input your results below."
)

# User input section
st.subheader("Enter Values for Each Environmental Impact")
input_values = []

for i, impact in enumerate(df["Environmental Impact"]):
    value = st.number_input(f"{impact} ({df['Unit'][i]})", min_value=0.0, step=0.01, value=10.0)
    input_values.append(value)

df["Input Value"] = input_values

# Cost Calculation
st.subheader("Select Cost Factor")
cost_options = ["Minimum Value", "Maximum Value", "Average Value", "My Model"]
cost_factor = st.selectbox("Choose Cost Factor", cost_options)

if cost_factor == "My Model":
    my_model_values = []
    for impact in df["Environmental Impact"]:
        my_value = st.number_input(f"Enter your model's cost factor for {impact}", min_value=0.0, step=0.01, value=10.0)
        my_model_values.append(my_value)
    df["Cost Factor"] = my_model_values
else:
    df["Cost Factor"] = df[cost_factor]

df["Cost (€)"] = df["Input Value"] * df["Cost Factor"]

total_cost = df["Cost (€)"].sum()

st.subheader("Calculation Results")
st.dataframe(df[["Environmental Impact", "Cost (€)"]], height=600)
df_chart = df.set_index("Environmental Impact")["Cost (€)"]
df_chart_normalized = df_chart / df_chart.max()
st.subheader("Normalized Stacked Cost Breakdown")
st.bar_chart(df_chart_normalized)