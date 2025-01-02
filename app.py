import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data  # Updated caching method
def load_data():
    # Load 2019 dataset
    df_2019 = pd.read_csv('Global Food Security Index 2019.csv', skiprows=1, header=None)
    df_2019.columns = ["Index", "Rank", "Country", "Overall_Score", "Affordability", "Availability", "Quality_and_Safety"]
    df_2019.drop(columns=["Index"], inplace=True)

    # Load 2022 dataset
    df_2022 = pd.read_csv('Global Food Security Index 2022.csv')
    df_2022.rename(columns={
        "Overall score": "Overall_Score",
        "Quality and Safety": "Quality_and_Safety"
    }, inplace=True)

    # Ensure Country columns have the same dtype
    df_2019['Country'] = df_2019['Country'].astype(str)
    df_2022['Country'] = df_2022['Country'].astype(str)

    # Merge datasets
    df_merged = pd.merge(
        df_2019,
        df_2022,
        on="Country",
        suffixes=("_2019", "_2022")
    )
    return df_merged

# Load data
df_merged = load_data()

# Streamlit App Layout
st.title("Global Food Security: Key Indicators Across Countries")
st.sidebar.header("Select Visualization")

# Sidebar Options
viz_type = st.sidebar.radio(
    "Choose Visualization Type",
    ("Scatter Plot", "Bar Chart", "Radar Chart")
)

if viz_type == "Scatter Plot":
    st.subheader("Scatter Plot: Comparison of Overall Scores (2019 vs 2022)")
    fig = px.scatter(
        df_merged,
        x='Overall_Score_2019',
        y='Overall_Score_2022',
        hover_name='Country',
        title="Comparison of Overall Food Security Scores (2019 vs 2022)",
        labels={"Overall_Score_2019": "2019 Overall Score", "Overall_Score_2022": "2022 Overall Score"}
    )
    fig.update_traces(marker=dict(size=8, opacity=0.7))
    st.plotly_chart(fig)

elif viz_type == "Bar Chart":
    st.subheader("Top 20 Countries by Overall Score (2022)")
    df_top20 = df_merged.sort_values("Overall_Score_2022", ascending=False).head(20)
    fig = px.bar(
        df_top20,
        x='Country',
        y='Overall_Score_2022',
        title="Top 20 Countries by Overall Food Security Score (2022)",
        labels={"Overall_Score_2022": "Overall Score (2022)"},
        color='Country'
    )
    fig.update_layout(xaxis={'categoryorder': 'total descending'})
    st.plotly_chart(fig)

elif viz_type == "Radar Chart":
    st.subheader("Radar Chart: Country Comparison (2019 vs 2022)")
    country = st.selectbox("Select a Country", df_merged["Country"].unique())
    df_country = df_merged[df_merged['Country'] == country]

    dimensions = ['Affordability', 'Availability', 'Quality_and_Safety']
    values_2019 = [
        df_country['Affordability_2019'].values[0],
        df_country['Availability_2019'].values[0],
        df_country['Quality_and_Safety_2019'].values[0]
    ]
    values_2022 = [
        df_country['Affordability_2022'].values[0],
        df_country['Availability_2022'].values[0],
        df_country['Quality_and_Safety_2022'].values[0]
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_2019,
        theta=dimensions,
        fill='toself',
        name='2019'
    ))
    fig.add_trace(go.Scatterpolar(
        r=values_2022,
        theta=dimensions,
        fill='toself',
        name='2022'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title=f"Radar Chart of {country}'s Food Security Dimensions (2019 vs 2022)"
    )
    st.plotly_chart(fig)
