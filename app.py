import streamlit as st
import pandas as pd
import os

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv("final_directory_dataset_cleaning.csv")

st.set_page_config(page_title="Cleaning Services", layout="wide")

st.title("🏠 Home Cleaning Services - Newark")

# -------------------------
# SIDEBAR FILTERS
# -------------------------
st.sidebar.header("Filters")

search = st.sidebar.text_input("Search business")
rating_filter = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.5)

price_filter = st.sidebar.selectbox(
    "Price Category", ["All", "Budget", "Mid-range", "Premium"]
)

# -------------------------
# FILTER LOGIC
# -------------------------
filtered_df = df[df["rating"] >= rating_filter]

if price_filter != "All":
    filtered_df = filtered_df[filtered_df["price_category"] == price_filter]

if search:
    filtered_df = filtered_df[
        filtered_df["name"].str.contains(search, case=False, na=False)
    ]

filtered_df = filtered_df.sort_values(by="score", ascending=False)

st.subheader(f"Showing {len(filtered_df)} results")

# -------------------------
# CREATE LEADS FILE
# -------------------------
if not os.path.exists("leads.csv"):
    pd.DataFrame(columns=["business", "name", "phone", "requirement"]).to_csv("leads.csv", index=False)

# -------------------------
# DISPLAY + LEAD FORM
# -------------------------
for i, row in filtered_df.iterrows():
    with st.container():
        col1, col2 = st.columns([3, 1])

        with col1:
            st.subheader(row["name"])
            st.write(f"⭐ {row['rating']} | 📝 {int(row['reviews'])} reviews")
            st.write(f"📍 {row['address']}")
            st.write(f"🏷 {row['best_for']}")
            st.write(f"🧹 Services: {row['services']}")

        with col2:
            st.write(f"💰 {row['price_category']}")
            if pd.notna(row["website"]):
                st.markdown(f"[🌐 Visit]({row['website']})")

        # -------------------------
        # LEAD FORM
        # -------------------------
        with st.expander("📩 Request Service"):
            user_name = st.text_input(f"Name_{i}")
            user_phone = st.text_input(f"Phone_{i}")
            user_req = st.text_area(f"Requirement_{i}")

            if st.button(f"Submit_{i}"):
                new_lead = pd.DataFrame([{
                    "business": row["name"],
                    "name": user_name,
                    "phone": user_phone,
                    "requirement": user_req
                }])

                new_lead.to_csv("leads.csv", mode='a', header=False, index=False)

                st.success("✅ Request submitted!")

        st.divider()