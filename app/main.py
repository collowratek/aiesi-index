import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

# Page config - clean, minimal
st.set_page_config(
    page_title="AIESI Index",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clean light theme CSS
st.markdown("""
<style>
    /* Clean light background */
    .stApp {
        background: #fafafa;
    }

    /* Hide all Streamlit chrome */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Typography */
    h1, h2, h3 {
        font-weight: 500;
        color: #1a1a1a;
    }

    /* Hero stat */
    .hero {
        text-align: center;
        padding: 3rem 1rem;
        margin-bottom: 1rem;
    }

    .hero-stat {
        font-size: 5rem;
        font-weight: 300;
        color: #1a1a1a;
        line-height: 1;
        letter-spacing: -0.03em;
    }

    .hero-label {
        font-size: 1.1rem;
        color: #666;
        margin-top: 0.75rem;
        font-weight: 400;
    }

    /* Minimal header */
    .site-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        margin-bottom: 0;
        border-bottom: 1px solid #eee;
    }

    .site-title {
        font-size: 1rem;
        font-weight: 500;
        color: #1a1a1a;
        margin: 0;
    }

    .site-subtitle {
        font-size: 0.75rem;
        color: #999;
        margin-left: 0.75rem;
    }

    .site-link {
        color: #666;
        text-decoration: none;
        font-size: 0.85rem;
    }

    .site-link:hover {
        color: #1a1a1a;
    }

    /* Tab styling - minimal */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 1px solid #eee;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        border-bottom: 2px solid transparent;
        color: #999;
        padding: 0.75rem 1.5rem;
        font-size: 0.9rem;
    }

    .stTabs [aria-selected="true"] {
        background: transparent;
        border-bottom: 2px solid #1a1a1a;
        color: #1a1a1a;
    }

    /* Clean cards */
    .stat-row {
        display: flex;
        gap: 2rem;
        justify-content: center;
        margin: 2rem 0;
    }

    .stat-item {
        text-align: center;
    }

    .stat-value {
        font-size: 1.5rem;
        font-weight: 500;
        color: #1a1a1a;
    }

    .stat-label {
        font-size: 0.8rem;
        color: #999;
        margin-top: 0.25rem;
    }

    /* Footer */
    .site-footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid #eee;
        color: #999;
        font-size: 0.8rem;
    }

    .site-footer a {
        color: #666;
        text-decoration: none;
    }

    /* Hide streamlit elements */
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
    }

    /* Selectbox visible */
    .stSelectbox > div > div {
        background: white;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    .stSelectbox > div > div:hover {
        border-color: #999;
    }

    /* DataFrame clean */
    .stDataFrame {
        border: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)  # 5min cache, v6 TALIS+Eurostat
def load_data():
    return pd.read_csv("data/processed/aiesi_data.csv")

@st.cache_data
def load_geojson():
    with open("data/geojson/eu27.geojson", "r") as f:
        return json.load(f)

def create_map(df, geojson, dimension):
    """Clean, minimal choropleth map - focused on EU"""
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations="country_code",
        featureidkey="properties.ISO_A2",
        color=dimension,
        color_continuous_scale=[
            [0, "#c62828"],      # Deep red - low score
            [0.25, "#ef5350"],   # Red
            [0.4, "#ffb74d"],    # Amber
            [0.5, "#fff176"],    # Yellow - middle
            [0.65, "#aed581"],   # Light green
            [0.8, "#66bb6a"],    # Green
            [1, "#2e7d32"]       # Deep green - high score
        ],
        range_color=[0, 1],
        mapbox_style="carto-positron",
        zoom=3.2,
        center={"lat": 54, "lon": 8},  # Shifted west, more zoom
        opacity=0.85,
        hover_name="country",
        hover_data={
            "country_code": False,
            dimension: ":.2f"
        }
    )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=420,
        paper_bgcolor='#f5f5f5',  # Light gray background
        coloraxis_colorbar=dict(
            title="",
            tickvals=[0, 0.33, 0.66, 1],
            ticktext=["0", "0.33", "0.66", "1"],
            len=0.4,
            thickness=8,
            outlinewidth=0,
            x=0.98,
            xpad=0
        )
    )

    return fig

def create_ranking(df):
    """Simple horizontal bar ranking"""
    df_sorted = df.sort_values('overall_score', ascending=True)

    fig = go.Figure()

    # Color bars by score: red (low) → yellow (mid) → green (high)
    colors = []
    for score in df_sorted['overall_score']:
        if score <= 0.33:
            colors.append('#c62828')
        elif score <= 0.5:
            colors.append('#ef5350')
        elif score <= 0.66:
            colors.append('#ffb74d')
        else:
            colors.append('#2e7d32')

    fig.add_trace(go.Bar(
        y=df_sorted['country'],
        x=df_sorted['overall_score'],
        orientation='h',
        marker_color=colors,
        marker_line_width=0,
        hovertemplate='%{y}: %{x:.2f}<extra></extra>'
    ))

    fig.update_layout(
        height=650,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#666', size=11),
        xaxis=dict(
            gridcolor='#eee',
            range=[0, 1],
            tickvals=[0, 0.25, 0.5, 0.75, 1],
            showline=False
        ),
        yaxis=dict(
            showgrid=False,
            showline=False
        ),
        margin=dict(l=100, r=20, t=20, b=40)
    )

    return fig

def main():
    df = load_data()
    geojson = load_geojson()

    # Minimal header
    st.markdown("""
    <div class="site-header">
        <div>
            <span class="site-title">AIESI Index</span>
            <span class="site-subtitle">AI in Education Salience Index</span>
        </div>
        <a href="https://skolagpt.cz" target="_blank" class="site-link">skolagpt.cz</a>
    </div>
    """, unsafe_allow_html=True)

    # Hero insight - one number
    countries_with_curriculum = len(df[df['ai_in_curriculum'] >= 0.5])
    countries_without = 27 - countries_with_curriculum

    st.markdown(f"""
    <div class="hero">
        <div class="hero-stat">{countries_without}</div>
        <div class="hero-label">zemí EU27 nemá AI v kurikulu</div>
    </div>
    """, unsafe_allow_html=True)

    # Simple tabs - no icons
    tab1, tab2, tab3 = st.tabs(["Mapa", "Žebříček", "O datech"])

    with tab1:
        # Dimension selector - right aligned, minimal
        col1, col2 = st.columns([4, 1])
        with col2:
            dimension = st.selectbox(
                "Zobrazit",
                options=["overall_score", "edu_policy_coverage", "adoption_score"],
                format_func=lambda x: {
                    "overall_score": "Celkové skóre",
                    "edu_policy_coverage": "Pokrytí politik",
                    "adoption_score": "Adopce",
                }[x],
                label_visibility="collapsed"
            )

        # Map - constrained width
        fig = create_map(df, geojson, dimension)
        col_map1, col_map2, col_map3 = st.columns([1, 6, 1])
        with col_map2:
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # Key stats below map - minimal
        top = df.loc[df['overall_score'].idxmax()]
        cz = df[df['country_code'] == 'CZ'].iloc[0]
        cz_rank = (df['overall_score'] > cz['overall_score']).sum() + 1

        eu_mean = df['overall_score'].mean()
        eu_sd = df['overall_score'].std()
        st.markdown(f"""
        <div class="stat-row">
            <div class="stat-item">
                <div class="stat-value">{top['country']}</div>
                <div class="stat-label">nejvyšší skóre ({top['overall_score']:.1f})</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{cz_rank}.</div>
                <div class="stat-label">Česko</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{eu_mean:.1f} ± {eu_sd:.1f}</div>
                <div class="stat-label">průměr EU (± SD)</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        fig2 = create_ranking(df)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

        # Download link - minimal
        csv = df.to_csv(index=False)
        st.download_button(
            "Stáhnout CSV",
            data=csv,
            file_name="aiesi_data.csv",
            mime="text/csv"
        )

    with tab3:
        st.markdown("""
        ### AIESI Index v6

        Explorativní nástroj měřící, jak moc je AI ve vzdělávání „velkým tématem" v zemích EU27.

        **Dvě dimenze (rovné váhy):**
        - **Pokrytí politik (50 %)** — checklist existence strategií, kurikula, školení učitelů, pilotů
        - **Adopce (50 %)** — dva nezávislé zdroje: TALIS 2024 (% učitelů s AI) + Eurostat 2025 (% populace s GenAI)

        **Interpretace skóre:**
        - 0,0–0,3: Nízká salience
        - 0,3–0,7: Střední salience
        - 0,7–1,0: Vysoká salience
        """)

        # Data quality note
        if 'adoption_method' in df.columns:
            n_both = (df['adoption_method'] == 'both').sum()
            n_eurostat = (df['adoption_method'] == 'eurostat_only').sum()
            st.markdown(f"""
        **Kvalita adopčních dat:**
        {n_both} zemí s oběma zdroji (TALIS + Eurostat), {n_eurostat} pouze s Eurostat
        (DE, IE, HR, SI, CY, EL, LU — neúčastnily se TALIS 2024).
            """)

        # Dimension correlation
        rho = df['edu_policy_coverage'].rank().corr(df['adoption_score'].rank())
        st.markdown(f"**Korelace dimenzí (Spearman):** ρ = {rho:.2f} — dimenze jsou téměř nezávislé.")

        # Sensitivity analysis summary
        try:
            sa = pd.read_csv("data/processed/sensitivity_analysis.csv")
            st.markdown(f"""
        **Citlivostní analýza ({len(sa)} kombinací vah, rozsah 20–80 %):**
        Spearman rho pořadí: min {sa['spearman_rho'].min():.3f}, průměr {sa['spearman_rho'].mean():.3f}
        — pořadí zemí je stabilní při změnách vah.
            """)
        except FileNotFoundError:
            pass

        st.markdown("""
        **Hlavní omezení:**
        - Pokrytí politik měří existenci (checklist), nikoliv kvalitu či financování
        - 7 zemí má adopci pouze z Eurostat (bez TALIS učitelského průzkumu)
        - N=27, výsledky interpretujte s přiměřenou opatrností

        **Zdroje:**
        OECD TALIS 2024 (učitelé, 20/27 zemí), Eurostat 2025 isoc_ai_iaiu (GenAI populace, 27/27),
        European Schoolnet 2024

        **Sběr dat:** leden 2025, adopční data aktualizována březen 2026
        """)

        # PDF methodology download
        with open("docs/AIESI_Metodologie.pdf", "rb") as pdf_file:
            st.download_button(
                "Stáhnout metodologii (PDF)",
                data=pdf_file,
                file_name="AIESI_Metodologie.pdf",
                mime="application/pdf"
            )

    # Footer
    st.markdown("""
    <div class="site-footer">
        <a href="https://skolagpt.cz">skolagpt.cz</a> · Data: 2025, v6
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
