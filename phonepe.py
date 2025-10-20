import pandas as pd
import os, json
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import pydeck as pdk

import os
import json
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

# ---- Load data ----
import os
import json
import pandas as pd
import streamlit as st

# ---------- Load Data ----------
path = r'C:\Users\sktcs\Documents\data\aggregated\user\country\india\state'

data = []
for state in os.listdir(path):
    state_path = os.path.join(path, state)
    if os.path.isdir(state_path):
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if os.path.isdir(year_path):
                for file in os.listdir(year_path):
                    if file.endswith(".json"):
                        file_path = os.path.join(year_path, file)
                        with open(file_path, "r") as f:
                            content = json.load(f)
                            try:
                                users_data = content["data"]["usersByDevice"]
                                if users_data:
                                    total_users = sum([x["count"] for x in users_data])
                                    data.append({
                                        "state": state.title().replace("-", " "),
                                        "year": int(year),
                                        "quarter": int(file.strip(".json")),
                                        "total_users": total_users
                                    })
                            except Exception:
                                continue

df_user = pd.DataFrame(data)

# ---------- Add Coordinates ----------
state_coords = {
    'Andhra Pradesh': [15.9129, 79.7400],
    'Arunachal Pradesh': [28.2180, 94.7278],
    'Assam': [26.2006, 92.9376],
    'Bihar': [25.0961, 85.3131],
    'Chhattisgarh': [21.2787, 81.8661],
    'Goa': [15.2993, 74.1240],
    'Gujarat': [22.2587, 71.1924],
    'Haryana': [29.0588, 76.0856],
    'Himachal Pradesh': [31.1048, 77.1734],
    'Jharkhand': [23.6102, 85.2799],
    'Karnataka': [15.3173, 75.7139],
    'Kerala': [10.8505, 76.2711],
    'Madhya Pradesh': [22.9734, 78.6569],
    'Maharashtra': [19.7515, 75.7139],
    'Manipur': [24.6637, 93.9063],
    'Meghalaya': [25.4670, 91.3662],
    'Mizoram': [23.1645, 92.9376],
    'Nagaland': [26.1584, 94.5624],
    'Odisha': [20.9517, 85.0985],
    'Punjab': [31.1471, 75.3412],
    'Rajasthan': [27.0238, 74.2179],
    'Sikkim': [27.5330, 88.5122],
    'Tamil Nadu': [11.1271, 78.6569],
    'Telangana': [18.1124, 79.0193],
    'Tripura': [23.9408, 91.9882],
    'Uttar Pradesh': [26.8467, 80.9462],
    'Uttarakhand': [30.0668, 79.0193],
    'West Bengal': [22.9868, 87.8550],
    'Delhi': [28.7041, 77.1025],
    'Jammu And Kashmir': [33.7782, 76.5762],
    'Ladakh': [34.1526, 77.5771],
}

df_user['latitude'] = df_user['state'].map(lambda x: state_coords.get(x, [None, None])[0])
df_user['longitude'] = df_user['state'].map(lambda x: state_coords.get(x, [None, None])[1])
df_user = df_user.dropna(subset=['latitude', 'longitude'])

# ---------- Streamlit App ----------
st.title("📍 PhonePe User Map (Year-wise)")

# Sidebar filter
year_list = sorted(df_user["year"].unique())
selected_year = st.sidebar.selectbox("Select Year", year_list)

# Filter data for selected year
filtered_df = df_user[df_user["year"] == selected_year]

# Optional: Aggregate by state (if multiple quarters)
filtered_df = filtered_df.groupby(["state", "latitude", "longitude"])["total_users"].sum().reset_index()

st.subheader(f"Total Users by State – {selected_year}")
st.map(filtered_df[['latitude', 'longitude']])





st.set_page_config(page_title = "Phonepe Transaction Dynamic" , layout = "wide")
st.title("📈 Decoding Transaction Dynamics on PhonePe")
path = r"C:\Users\sktcs\Documents\data\aggregated\transaction\country\india\state"
data = []
for state in os.listdir(path):
    state_path = os.path.join(path,state)
    for year in os.listdir(state_path):
        year_path = os.path.join(state_path,year)
        for file in os.listdir(year_path):
            file_path = os.path.join(year_path,file)
            quater = file.split('.')[0]
            with open(file_path,'r') as f:
                json_data = json.load(f)
                for record in json_data['data']['transactionData']:
                    data.append([
                        state,
                        year,
                        quater,
                        record['name'],
                        record['paymentInstruments'][0]['count'],
                        record['paymentInstruments'][0]['amount']
                        ])
aggregated_transaction=pd.DataFrame(data, columns = ["state", "year", "quarter", "transaction_name",  "count", "amount"])
aggregated_transaction.head()
st.dataframe(aggregated_transaction.head())
st.subheader("1️⃣ Top 10 States by Total Transaction Amount")
top_states = aggregated_transaction.groupby("state")["amount"].sum().nlargest(10)
fig1, ax1 = plt.subplots()
top_states.plot(kind="bar", ax=ax1)
ax1.set_ylabel("Total Transaction Amount (₹)")
ax1.set_title("Top 10 Performing States")
st.pyplot(fig1)

st.subheader("2️⃣ Quarterly Trend of Transactions")
trend = aggregated_transaction.groupby("quarter")["amount"].sum().reset_index()
fig2, ax2 = plt.subplots()
ax2.plot(trend["quarter"], trend["amount"], marker="o")
plt.xticks(rotation=45)
ax2.set_title("Quarterly Transaction Trend (India)")
ax2.set_ylabel("Total Amount (₹)")
st.pyplot(fig2)

st.subheader("3️⃣ Transaction Type Distribution")
type_dist = aggregated_transaction.groupby("transaction_name")["amount"].sum()
print(type_dist)
fig3, ax3 = plt.subplots()
ax3.pie(type_dist, labels=type_dist.index, autopct="%1.1f%%", startangle=90)
ax3.axis("equal")
st.pyplot(fig3)

st.subheader("4️⃣ State vs Quarter Heatmap (Transaction Amount)")
heat_data = aggregated_transaction.pivot_table(values="amount",
                               index="state",
                               columns="transaction_name",
                               aggfunc="sum")
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.heatmap(heat_data, cmap='YlGnBu', ax=ax4)
st.pyplot(fig4)

st.subheader("5️⃣ State-wise Contribution by Transaction Type")
type_state = aggregated_transaction.groupby(["state", "quarter"])["amount"].sum().unstack().fillna(0)
fig5, ax5 = plt.subplots(figsize=(12, 6))
type_state.plot(kind="bar", stacked=True, ax=ax5)
plt.xticks(rotation=90)
ax5.set_title("State-wise Transaction Type Distribution")
st.pyplot(fig5)

st.set_page_config(page_title="Insurance Penetration & Growth - PhonePe", layout="wide")

st.title("🛡️ Insurance Penetration and Growth Potential Analysis")
st.markdown("""
Analyze how insurance transactions vary across states, years, and product types on PhonePe.
""")
path = r"C:\Users\sktcs\Documents\data\aggregated\insurance\country\india\state"

data = []

for state in os.listdir(path):
    state_path = os.path.join(path, state)
    if os.path.isdir(state_path):
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if os.path.isdir(year_path):
                for file in os.listdir(year_path):
                    if file.endswith(".json"):
                        quarter = file.replace(".json", "")  # file name = quarter
                        file_path = os.path.join(year_path, file)
                        with open(file_path, "r") as f:
                            json_data = json.load(f)

                            # Loop through transactionData
                            for record in json_data["data"]["transactionData"]:
                                for pi in record["paymentInstruments"]:
                                    data.append({
                                        "state": state,
                                        "year": int(year),
                                        "quarter": int(quarter),
                                        "transaction_type": record["name"],
                                        "type": pi["type"],
                                        "count": pi["count"],
                                        "amount": pi["amount"]
                                    })

# Convert to DataFrame
aggregated_insurance = pd.DataFrame(data)
st.dataframe(aggregated_insurance.head())

 # Sidebar filters
st.sidebar.header("🔍 Filters")
selected_year = st.sidebar.multiselect("Select Year(s):",options=sorted(aggregated_insurance["year"].unique()),
                                       default=sorted(aggregated_insurance["year"].unique()))
selected_state = st.sidebar.multiselect("Select State(s):",options=sorted(aggregated_insurance["state"].unique()),
                                        default=sorted(aggregated_insurance["state"].unique()))
selected_type = st.sidebar.multiselect("Select Policy Type(s):",options=sorted(aggregated_insurance["quarter"].unique()),
                                       default=sorted(aggregated_insurance["quarter"].unique()))

filtered_df = aggregated_insurance[(aggregated_insurance["year"].isin(selected_year)) &(aggregated_insurance["state"].isin(selected_state)) &(aggregated_insurance["quarter"].isin(selected_type))]

# Overview
st.subheader("📋 Filtered Dataset Overview")
st.dataframe(filtered_df.head())

st.subheader("1️⃣ Top 10 States by Total Insurance Amount")
top_states = filtered_df.groupby("state")["amount"].sum().nlargest(10)
fig6, ax6 = plt.subplots()
top_states.plot(kind="bar", ax=ax6, color="teal")
ax1.set_ylabel("Total Insurance Amount (₹)")
ax1.set_title("Top 10 Performing States in Insurance")
st.pyplot(fig6)

st.subheader("2️⃣ Yearly Insurance Transaction Growth")
yearly = filtered_df.groupby("year")["amount"].sum().reset_index()
fig7, ax7 = plt.subplots()
ax7.plot(yearly["year"], yearly["amount"], marker="o", color="purple")
ax7.set_title("Yearly Insurance Growth Trend")
ax7.set_xlabel("Year")
ax7.set_ylabel("Total Amount (₹)")
st.pyplot(fig7)

st.subheader("3️⃣ Distribution by Transaction Type")
type_dist = filtered_df.groupby("transaction_type")["amount"].sum()
fig8, ax8 = plt.subplots()
ax8.pie(type_dist, labels=type_dist.index, autopct="%1.1f%%", startangle=90)
ax8.axis("equal")
st.pyplot(fig8)

st.subheader("4️⃣ State vs Quarter Heatmap (Insurance Amount)")
heat_data = filtered_df.pivot_table(values="amount", index="state", columns="quarter", aggfunc="sum")
fig9, ax9 = plt.subplots(figsize=(10, 6))
sns.heatmap(heat_data, cmap="YlGnBu", ax=ax9)
ax9.set_title("Quarterly Insurance Intensity Across States")
st.pyplot(fig9)

st.subheader("5️⃣ State-wise Policy Type Contribution")
type_state = filtered_df.groupby(["state", "type"])["amount"].sum().unstack().fillna(0)
fig10, ax10 = plt.subplots(figsize=(12, 6))
type_state.plot(kind="bar", stacked=True, ax=ax10)
plt.xticks(rotation=90)
ax10.set_title("State-wise Policy Type Breakdown")
st.pyplot(fig10)

path = r'C:\Users\sktcs\Documents\data\aggregated\user\country\india\state'

data = []

for state in os.listdir(path):
    state_path = os.path.join(path, state)
    if os.path.isdir(state_path):
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if os.path.isdir(year_path):
                for file in os.listdir(year_path):
                    if file.endswith(".json"):
                        quarter = file.replace(".json", "")  # file name is quarter
                        file_path = os.path.join(year_path, file)

                        with open(file_path, "r") as f:
                            json_data = json.load(f)

                            # Safely check before iterating
                            if (
                                json_data.get("data") 
                                and json_data["data"].get("usersByDevice")
                            ):
                                for record in json_data["data"]["usersByDevice"]:
                                    data.append({
                                        "state": state,
                                        "year": int(year),
                                        "quarter": int(quarter),
                                        "brand": record["brand"],
                                        "count": record["count"],
                                        "percentage": record["percentage"]
                                    })

# Convert to DataFrame
aggregated_user = pd.DataFrame(data)
st.dataframe(aggregated_user.head())

st.set_page_config(page_title = "📱 PhonePe Device Dominance Dashboard", layout = "wide")
st.title("📱 PhonePe Device Dominance & User Engagement Dashboard")
st.markdown("""
Gain insights into user preferences, regional dominance, and engagement trends across device brands on PhonePe.
""")

st.sidebar.header("Filter Options")
years = sorted(aggregated_user['year'].unique())
states = sorted(aggregated_user['state'].unique())
brands = sorted(aggregated_user['brand'].unique())
quarters = sorted(aggregated_user['quarter'].unique())

selected_years = st.sidebar.multiselect("Select Year(s)", years, default=years)
selected_states = st.sidebar.multiselect("Select State(s)", states, default=states)
selected_brands = st.sidebar.multiselect("Select Brand(s)", brands, default=brands)
selected_quarters = st.sidebar.multiselect("Select Quarter(s)",quarters,default = quarters)

filtered_df = aggregated_user[
    (aggregated_user['year'].isin(selected_years)) &
    (aggregated_user['state'].isin(selected_states)) &
    (aggregated_user['brand'].isin(selected_brands)) &
    (aggregated_user['quarter'].isin(selected_quarters))
]

filtered_df = aggregated_user[(aggregated_user['year'].isin(selected_year)) & (aggregated_user['state'].isin(selected_states))]
st.subheader("🏆 Top 10 Device Brands by User Count")
top_brands = (filtered_df.groupby('brand')['count'].sum().sort_values(ascending = False).head(10).reset_index())

fig11, ax11 = plt.subplots(figsize=(8, 4))
sns.barplot(x='brand', y='count', data=top_brands, palette='viridis', ax=ax11)
ax11.set_title("Top 10 Device Brands by Registered Users")
st.pyplot(fig11)

st.subheader("🥧 Device Market Share")

fig12, ax12 = plt.subplots()
ax12.pie(
    top_brands['count'],
    labels=top_brands['brand'],
    autopct='%1.1f%%',
    startangle=90,
    wedgeprops={'edgecolor': 'white'}
)
ax12.set_title("Device Market Share Among Top Brands")
st.pyplot(fig12)

st.subheader("📈 Yearly Trend of Device Usage by Brand")

trend_df = (
    filtered_df.groupby(['year', 'brand'])['count']
    .sum()
    .reset_index()
)

fig13, ax13 = plt.subplots(figsize=(10, 5))
sns.lineplot(
    data=trend_df,
    x='year',
    y='count',
    hue='brand',
    marker='o',
    palette='tab10',
    ax=ax13
)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
ax13.set_title("Yearly Trend of Registered Users by Brand")
st.pyplot(fig13)

st.subheader("🌍 Regional Device Dominance (Heatmap)")

heatmap_data = (
    filtered_df.groupby(['state', 'brand'])['count']
    .sum()
    .unstack(fill_value=0)
)

fig14, ax14 = plt.subplots(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap='YlGnBu', linewidths=0.3)
ax14.set_title("Device Popularity by State")
st.pyplot(fig14)

st.subheader("🕒 Quarterly Distribution of Device Usage")

fig15, ax15 = plt.subplots(figsize=(8, 5))
sns.boxplot(
    x='quarter',
    y='count',
    hue='brand',
    data=filtered_df,
    showfliers=False,
    ax=ax15
)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
ax15.set_title("Quarterly Variation in Device Usage")
st.pyplot(fig15)

st.markdown("## 🔍 Insights Summary")
st.markdown("""
- **Top Brands:** Identify the most popular device brands across India.  
- **Market Share:** Understand brand contribution to total users.  
- **Trends:** Track brand adoption growth or decline across years.  
- **Regional Dominance:** See which brands lead in different states.  
- **Quarterly Shifts:** Analyze seasonal usage variations and emerging preferences.
""")

base_path = r"C:\Users\sktcs\Documents\data\map\user\hover\country\india\state"

all_data = []
for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            with open(file_path, "r") as f:
                data = json.load(f)

            quarter = file.replace(".json", "")
            year = os.path.basename(os.path.dirname(file_path))
            state = os.path.basename(os.path.dirname(os.path.dirname(file_path)))

            if data.get("data") and data["data"].get("hoverData"):
                for district, values in data["data"]["hoverData"].items():
                    all_data.append({
                        "state": state,
                        "year": int(year),
                        "quarter": int(quarter),
                        "district": district,
                        "registeredUsers": values.get("registeredUsers", 0),
                        "appOpens": values.get("appOpens", 0)
                    })

user_hover = pd.DataFrame(all_data)
st.dataframe(user_hover.head())

st.set_page_config(page_title="📊 PhonePe Market Expansion Dashboard", layout="wide")

st.title("💼 PhonePe Transaction & User Engagement Dashboard")
st.markdown("""
Analyze user activity across states and districts to identify regions with high engagement and 
market expansion opportunities.
""")

total_users = user_hover['registeredUsers'].sum()
total_opens = user_hover['appOpens'].sum()
top_state = user_hover.groupby('state')['registeredUsers'].sum().idxmax()

col1, col2, col3 = st.columns(3)
col1.metric("👥 Total Registered Users", f"{total_users:,}")
col2.metric("📱 Total App Opens", f"{total_opens:,}")
col3.metric("🏆 Top Performing State", top_state)

st.subheader("📊 Top 10 States by Registered Users")

top_states = (
    user_hover.groupby('state')['registeredUsers']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig16, ax16 = plt.subplots(figsize=(8, 4))
sns.barplot(x='registeredUsers', y='state', data=top_states, palette='viridis', ax=ax16)
ax16.set_title("Top 10 States by Registered Users")
st.pyplot(fig16)

st.subheader("🌍 District-level Engagement Heatmap")

heatmap_data = (
    user_hover.groupby(['state', 'district'])['appOpens']
    .sum()
    .unstack(fill_value=0)
)

fig17, ax17 = plt.subplots(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap="YlGnBu", cbar_kws={'label': 'App Opens'})
ax17.set_title("District-wise App Engagement")
st.pyplot(fig17)

st.subheader("📈 Yearly Growth in Registered Users")

yearly_trend = (
    user_hover.groupby(['year'])['registeredUsers']
    .sum()
    .reset_index()
)

fig18, ax18 = plt.subplots(figsize=(8, 4))
sns.lineplot(data=yearly_trend, x='year', y='registeredUsers', marker='o', ax=ax18)
ax18.set_title("Yearly Growth in Registered Users")
st.pyplot(fig18)

st.subheader("🔄 Engagement Efficiency: App Opens vs Registered Users")

fig19, ax19 = plt.subplots(figsize=(8, 5))
sns.scatterplot(
    data=user_hover,
    x='registeredUsers',
    y='appOpens',
    hue='state',
    alpha=0.7
)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
ax19.set_title("App Opens vs Registered Users by State")
st.pyplot(fig19)

st.subheader("🕒 Quarterly Transaction Activity")

quarterly_data = (
    user_hover.groupby(['quarter'])[['registeredUsers', 'appOpens']]
    .sum()
    .reset_index()
    .melt(id_vars='quarter', var_name='Metric', value_name='Count')
)

fig20, ax20 = plt.subplots(figsize=(8, 4))
sns.barplot(data=quarterly_data, x='quarter', y='Count', hue='Metric', palette='Set2', ax=ax20)
ax20.set_title("Quarterly User & App Engagement Comparison")
st.pyplot(fig5)

base_path = r"C:\Users\sktcs\Documents\data\top\insurance\country\india\state"

all_data = []

for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)

            with open(file_path, "r") as f:
                data = json.load(f)

            state = os.path.basename(os.path.dirname(file_path))
            year = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
            quarter = file.replace(".json", "")

            # Loop through categories (some may be None)
            for category in ["states", "districts", "pincodes"]:
                records = data["data"].get(category, [])
                if records:   # only iterate if it's not None/empty
                    for item in records:
                        row = {
                            "year": state,
                            "state": year,
                            "quarter": quarter,
                            "category": category,
                            "entityName": item.get("entityName"),
                            "insuranceCount": item.get("metric", {}).get("count", 0),
                            "insuranceAmount": item.get("metric", {}).get("amount", 0)
                        }
                        all_data.append(row)

top_insurance = pd.DataFrame(all_data)
print(top_insurance.head())
st.dataframe(top_insurance.head(5))

st.set_page_config(page_title="Insurance Engagement Dashboard", layout="wide")

st.title("📈 Insurance Engagement Analysis - PhonePe")
st.markdown("""
Analyze insurance transaction trends across India to understand user engagement, regional performance, and market opportunities.
""")

st.sidebar.header("Filter Options")
year_filter = st.sidebar.multiselect("Select Year(s):", sorted(top_insurance["year"].unique()))
state_filter = st.sidebar.multiselect("Select State(s):", sorted(top_insurance["state"].unique()))

filtered_df = top_insurance[(top_insurance["year"].isin(year_filter)) & (top_insurance["state"].isin(state_filter))]

state_count = filtered_df.groupby('state')['insuranceCount'].sum().nlargest(10) 
state_count = state_count.reset_index()

#st.dataframe(state_count.head())

fig21 = px.bar(state_count, x="state", y="insuranceCount", color="state",title="Top 10 States by Insurance Transaction Count")
st.plotly_chart(fig21, use_container_width=True)

state_amount = (
    filtered_df.groupby("state")["insuranceAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig22 = px.bar(state_amount, x="state", y="insuranceAmount", color="state",
              title="Top 10 States by Insurance Transaction Amount")
st.plotly_chart(fig22, use_container_width=True)

trend = (
    filtered_df.groupby(["year", "quarter"])
    [["insuranceCount", "insuranceAmount"]]
    .sum()
    .reset_index()
)
trend["period"] = trend["year"].astype(str) + "-Q" + trend["quarter"].astype(str)
fig23 = px.line(trend, x="period", y="insuranceCount", markers=True,
               title="Quarterly Trend of Insurance Transactions")

st.plotly_chart(fig23, use_container_width=True)

selected_state = st.selectbox("Select a State for District-level Analysis:", sorted(filtered_df["state"].unique()))
district_df = filtered_df[filtered_df["state"] == selected_state].groupby("entityName")["insuranceCount"].sum().reset_index()

fig24 = px.pie(district_df, values="insuranceCount", names="entityName",
              title=f"District-wise Insurance Share - {selected_state}")
st.plotly_chart(fig24, use_container_width=True)

fig25 = px.scatter(filtered_df, x="insuranceCount", y="insuranceAmount",
                  color="state", size="insuranceAmount",
                  title="Correlation between Transaction Count and Amount")
st.plotly_chart(fig25, use_container_width=True)


