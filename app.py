import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Define the environmental impact data with emojis
data = {
    "Environmental Impact": [
        "🌡️ Climate Change", "☀️ Ozone Depletion", "🏥 Human Toxicity (Cancer)",
        "🏥 Human Toxicity (Non-Cancer)", "💨 Particulate Matter", "🔋 Ionizing Radiation",
        "🚗 Photochemical Ozone Formation", "🌱 Acidification", "🌊 Eutrophication (Marine)",
        "🌊 Eutrophication (Freshwater)", "💧 Water Use", "⛏️ Resource Use (Minerals/Metals)"
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

# --- App Layout ---
st.title(" LCA Monetization Tool ")

# Step explanation
st.markdown("## **Read me**")
st.info("This tool estimates and visualizes the financial impact of various environmental impact categories. Users can input environmental impact data from a Life Cycle Assessment (LCA) study, apply monetization factors, and generate an interactive visualisation.")
st.markdown("### 📌 How to use this tool")
st.markdown("- 📊 Enter your environmental impact values in the first tab.")
st.markdown("- 💰 Select your monetization factor in the second tab. (You can also use your custom factors.)")
st.markdown("- 📈 View the results in the third tab. You can also export your result to CSV file.")
# Tabs for better organization
tab1, tab2, tab3 = st.tabs(["📊 Environment Impacts Input", "💰 Monetization Factor", "📈 See Results"])

with tab1:
    st.header("🔢 Enter Your Environmental Impact Values")
    st.info("Ensure that you conduct LCA using the 'EF3.1 method' and input your results below.")
    input_values = []
    cols = st.columns(2)
    for i, impact in enumerate(df["Environmental Impact"]):
        with cols[i % 2]:
            value = st.number_input(f"{impact} ({df['Unit'][i]})", min_value=0.0, step=0.01, value=10.0)
            input_values.append(value)
    df["Input Value"] = input_values

with tab2:
    st.header("💰 Select Cost Factor")
    cost_options = ["Minimum Value", "Maximum Value", "Average Value", "My Model"]
    cost_factor = st.radio("Choose Cost Factor", cost_options, horizontal=True)

    if cost_factor == "My Model":
        my_model_values = []
        with st.expander("Enter Your Custom Cost Factors (Expand)"):
            st.info("💶 Please specify your custom cost factor for each impact category in Euros (€).")
            cols = st.columns(2)
            for i, impact in enumerate(df["Environmental Impact"]):
                with cols[i % 2]:
                    my_value = st.number_input(f"Cost Factor for {impact} (€)", min_value=0.0, step=0.01, value=10.0)
                    my_model_values.append(my_value)
        df["Cost Factor"] = my_model_values
    else:
        df["Cost Factor"] = df[cost_factor]

    df["Cost (€)"] = df["Input Value"] * df["Cost Factor"]
    df["Percentage (%)"] = (df["Cost (€)"] / df["Cost (€)"].sum()) * 100

with tab3:
    total_cost = df["Cost (€)"].sum()
    st.header("📊 Calculation Results")
    st.markdown(f"### **Total Estimated Cost: €{total_cost:,.2f}**")
    st.dataframe(df[["Environmental Impact", "Cost (€)", "Percentage (%)"]], height=500)


    # Create a stacked bar chart using Altair for interactivity
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("sum(Cost (€))", title="Total Cost (€)"),
            y=alt.Y("Environmental Impact", title=""),
            color=alt.Color("Environmental Impact", legend=alt.Legend(title="Category")),
            tooltip=["Environmental Impact", "Cost (€)", "Percentage (%)"]
        )
        .properties(width=900, height=400)
    )

    st.altair_chart(chart, use_container_width=True)
st.header("License")
st.info("This project is open-source and available under the MIT License.")
st.info("For any inquiries or suggestions, please reach out to the [developer](https://www.linkedin.com/in/songsus/).")