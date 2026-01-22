import streamlit as st
import plotly.express as px
import pandas as pd
import json

st.set_page_config(
    page_title="AIESI - AI in Education Salience Index",
    page_icon="🎓",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/aiesi_data.csv")
    return df

@st.cache_data
def load_geojson():
    with open("data/geojson/eu27.geojson", "r") as f:
        return json.load(f)

def main():
    st.title("🎓 AIESI - AI in Education Salience Index")
    st.markdown("*Jak moc je AI ve vzdělávání velkým tématem v zemích EU27*")

    df = load_data()
    geojson = load_geojson()

    # Sidebar
    st.sidebar.header("Nastavení")

    dimension = st.sidebar.selectbox(
        "Vyberte dimenzi",
        options=["overall_score_v3", "edu_policy_score", "adoption_score", "media_score", "policy_score"],
        format_func=lambda x: {
            "overall_score_v3": "Celkové skóre (4D)",
            "edu_policy_score": "Vzdělávací AI politika",
            "adoption_score": "Praktická adopce",
            "media_score": "Mediální zájem",
            "policy_score": "Obecná AI připravenost"
        }[x]
    )

    color_scale = st.sidebar.selectbox(
        "Barevná škála",
        options=["Viridis", "RdYlGn", "Blues", "Reds", "YlOrRd"],
        index=1
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Dimenze indexu")
    st.sidebar.markdown("""
    - **Edu Policy**: AI v kurikulu, strategie vzdělávání, piloty
    - **Adopce**: Učitelé používající AI, EdTech ekosystém
    - **Média**: Google Trends zájem o "AI education"
    - **Obecná AI**: Vládní AI strategie, rozpočty (proxy)
    """)

    # Map
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations="country_code",
        featureidkey="properties.ISO_A2",
        color=dimension,
        color_continuous_scale=color_scale,
        range_color=[0, 1],
        mapbox_style="carto-positron",
        zoom=2.5,
        center={"lat": 54, "lon": 10},
        opacity=0.7,
        hover_name="country",
        hover_data={
            "country_code": False,
            "overall_score_v3": ":.2f",
            "edu_policy_score": ":.2f",
            "adoption_score": ":.2f",
            "media_score": ":.2f",
            "ai_curriculum_type": True,
            "teachers_ai_usage_pct": ":.0f"
        },
        labels={
            "overall_score_v3": "Celkové skóre",
            "edu_policy_score": "Edu Policy skóre",
            "adoption_score": "Adopce skóre",
            "media_score": "Media skóre",
            "ai_curriculum_type": "AI v kurikulu",
            "teachers_ai_usage_pct": "Učitelé s AI (%)"
        }
    )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=600,
        coloraxis_colorbar=dict(
            title=dict(text="Skóre", side="right"),
            tickformat=".2f"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # Stats - using the new 4D overall score
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Průměrné skóre EU27", f"{df['overall_score_v3'].mean():.2f}")

    with col2:
        top_country = df.loc[df['overall_score_v3'].idxmax()]
        st.metric("Nejvyšší skóre", f"{top_country['country']} ({top_country['overall_score_v3']:.2f})")

    with col3:
        bottom_country = df.loc[df['overall_score_v3'].idxmin()]
        st.metric("Nejnižší skóre", f"{bottom_country['country']} ({bottom_country['overall_score_v3']:.2f})")

    with col4:
        countries_with_curriculum = df[df['ai_in_curriculum'] >= 0.5].shape[0]
        st.metric("Země s AI v kurikulu", f"{countries_with_curriculum}/27")

    # Dimension comparison chart
    st.markdown("### Porovnání dimenzí")

    chart_df = df[['country', 'edu_policy_score', 'adoption_score', 'media_score']].melt(
        id_vars=['country'],
        var_name='Dimenze',
        value_name='Skóre'
    )
    chart_df['Dimenze'] = chart_df['Dimenze'].map({
        'edu_policy_score': 'Edu Policy',
        'adoption_score': 'Adopce',
        'media_score': 'Média'
    })

    fig2 = px.bar(
        chart_df,
        x='country',
        y='Skóre',
        color='Dimenze',
        barmode='group',
        color_discrete_map={'Edu Policy': '#9b59b6', 'Adopce': '#3498db', 'Média': '#e74c3c'}
    )
    fig2.update_layout(
        xaxis_title="",
        yaxis_title="Skóre (0-1)",
        xaxis_tickangle=-45,
        height=400
    )
    st.plotly_chart(fig2, use_container_width=True)

    # AI Curriculum Status
    st.markdown("### AI v kurikulu podle zemí")
    curriculum_df = df[['country', 'ai_curriculum_type', 'has_edu_ai_strategy', 'edu_ai_pilots']].copy()
    curriculum_df['status'] = curriculum_df['ai_curriculum_type'].map({
        'standalone': 'Samostatný předmět',
        'integrated': 'Integrováno',
        'piloting': 'Pilotování',
        'none': 'Není v kurikulu'
    })

    fig3 = px.bar(
        curriculum_df.sort_values('ai_curriculum_type', ascending=False),
        x='country',
        y=[1]*len(curriculum_df),
        color='status',
        color_discrete_map={
            'Samostatný předmět': '#27ae60',
            'Integrováno': '#3498db',
            'Pilotování': '#f39c12',
            'Není v kurikulu': '#e74c3c'
        }
    )
    fig3.update_layout(
        xaxis_title="",
        yaxis_title="",
        yaxis_visible=False,
        xaxis_tickangle=-45,
        height=250,
        showlegend=True,
        legend_title="Status AI v kurikulu"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Data table
    with st.expander("📊 Zobrazit všechna data"):
        display_cols = ["country", "overall_score_v3", "edu_policy_score", "adoption_score", "media_score",
                       "ai_curriculum_type", "teachers_ai_usage_pct", "data_quality"]
        st.dataframe(
            df[display_cols].sort_values("overall_score_v3", ascending=False),
            use_container_width=True,
            hide_index=True,
            column_config={
                "country": "Země",
                "overall_score_v3": st.column_config.NumberColumn("Celkové skóre", format="%.2f"),
                "edu_policy_score": st.column_config.NumberColumn("Edu Policy", format="%.2f"),
                "adoption_score": st.column_config.NumberColumn("Adopce", format="%.2f"),
                "media_score": st.column_config.NumberColumn("Média", format="%.2f"),
                "ai_curriculum_type": "AI v kurikulu",
                "teachers_ai_usage_pct": st.column_config.NumberColumn("Učitelé s AI (%)", format="%.0f"),
                "data_quality": "Kvalita dat"
            }
        )

    # Footer
    st.markdown("---")
    st.markdown("""
    **Zdroje:** OECD TALIS 2024, European Schoolnet 2024, GoStudent Edu AI Index 2025, Google Trends 2024

    **Metodologie:** Index kombinuje 3 dimenze (rovnoměrné váhy):
    - **Edu Policy** (33%): AI v kurikulu, vzdělávací AI strategie, školení učitelů, pilotní programy
    - **Adopce** (33%): Učitelé používající AI (TALIS), přístup studentů, EdTech startupy
    - **Média** (33%): Google Trends zájem o "AI education" v dané zemi

    **AI v kurikulu:**
    - 🟢 Samostatný předmět: Chorvatsko, Švédsko
    - 🔵 Integrováno: Dánsko, Estonsko, Finsko, Francie, Německo, Španělsko
    - 🟡 Pilotování: Řecko, Itálie, Nizozemsko, Slovinsko
    - 🔴 Není: 15 zemí včetně ČR

    **Datum sběru dat:** 2025-01-22
    """)

if __name__ == "__main__":
    main()
