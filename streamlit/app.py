import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import os

# --- Connexion ---
base    = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(base, '..', 'airbnb_analytics', 'dev.duckdb')

con = duckdb.connect(DB_PATH, read_only=True)

# --- Config page ---
st.set_page_config(
    page_title="Airbnb Analytics",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Airbnb Analytics Platform")
st.markdown("Tableau de bord analytique : données Airbnb")

# --- Onglets ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Logements",
    "👤 Hôtes",
    "💬 Avis",
    "🌕 Impact Pleine Lune"
])

# ── Tab 1 : Logements ─────────────────────────────────────────
with tab1:
    st.header("Analyse des logements par type")

    df = con.execute("SELECT * FROM main_gold.gold_listings_summary").df()

    col1, col2, col3 = st.columns(3)
    col1.metric("Types de logements", len(df))
    col2.metric("Prix moyen global", f"${df['avg_price'].mean():.2f}")
    col3.metric("Total annonces", f"{df['nb_listings'].sum():,}")

    fig = px.bar(
        df, x="room_type", y="avg_price",
        color="room_type",
        title="Prix moyen par type de logement",
        labels={"avg_price": "Prix moyen ($)", "room_type": "Type"}
    )
    st.plotly_chart(fig, use_container_width=True)

    col4, col5 = st.columns(2)
    with col4:
        fig2 = px.pie(
            df, names="room_type", values="nb_listings",
            title="Répartition des annonces par type"
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col5:
        fig3 = px.bar(
            df, x="room_type", y="avg_min_nights",
            color="room_type",
            title="Nombre minimum de nuits moyen",
            labels={"avg_min_nights": "Nuits min.", "room_type": "Type"}
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Détail par type")
    st.dataframe(df, use_container_width=True)

# ── Tab 2 : Hôtes ─────────────────────────────────────────────
with tab2:
    st.header("Performance des hôtes")

    df = con.execute("SELECT * FROM main_gold.gold_host_performance").df()

    # host_is_superhost est BOOLEAN dans dev.duckdb
    df["type"] = df["host_is_superhost"].map({True: "Superhost", False: "Hôte normal"})

    col1, col2, col3 = st.columns(3)
    col1.metric("Total hôtes",    f"{df['nb_hosts'].sum():,}")
    col2.metric("Total annonces", f"{df['nb_listings'].sum():,}")
    col3.metric("Total avis",     f"{df['nb_reviews'].sum():,}")

    col4, col5 = st.columns(2)
    with col4:
        fig = px.pie(
            df, names="type", values="nb_hosts",
            title="Répartition superhosts vs hôtes normaux"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col5:
        fig2 = px.bar(
            df, x="type", y="avg_price",
            color="type",
            title="Prix moyen selon le statut de l'hôte",
            labels={"avg_price": "Prix moyen ($)", "type": "Statut"}
        )
        st.plotly_chart(fig2, use_container_width=True)

    col6, col7 = st.columns(2)
    with col6:
        fig3 = px.bar(
            df, x="type", y="nb_listings",
            color="type",
            title="Nombre d'annonces par statut",
            labels={"nb_listings": "Annonces", "type": "Statut"}
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col7:
        fig4 = px.bar(
            df, x="type", y="nb_reviews",
            color="type",
            title="Nombre d'avis par statut",
            labels={"nb_reviews": "Avis", "type": "Statut"}
        )
        st.plotly_chart(fig4, use_container_width=True)

# ── Tab 3 : Avis ──────────────────────────────────────────────
with tab3:
    st.header("Évolution des avis dans le temps")

    df = con.execute("SELECT * FROM main_gold.gold_reviews_sentiment").df()

    # review_month est TIMESTAMP dans dev.duckdb
    df["review_month"] = pd.to_datetime(df["review_month"])

    col1, col2 = st.columns(2)
    with col1:
        years = sorted(df["review_month"].dt.year.unique().tolist())
        selected_years = st.multiselect("Filtrer par année", years, default=years)
    with col2:
        sentiments = sorted(df["sentiment"].unique().tolist())
        selected_sentiments = st.multiselect("Filtrer par sentiment", sentiments, default=sentiments)

    df_filtered = df[
        df["review_month"].dt.year.isin(selected_years) &
        df["sentiment"].isin(selected_sentiments)
    ]

    fig = px.line(
        df_filtered, x="review_month", y="nb_reviews",
        color="sentiment",
        title="Tendance des sentiments par mois",
        labels={"nb_reviews": "Nombre d'avis", "review_month": "Mois"},
        color_discrete_map={
            "positive": "#2ecc71",
            "negative": "#e74c3c",
            "neutral":  "#95a5a6"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

    df_global = (
        df_filtered
        .groupby("sentiment")["nb_reviews"]
        .sum()
        .reset_index()
    )
    fig2 = px.pie(
        df_global, names="sentiment", values="nb_reviews",
        title="Répartition globale des sentiments",
        color="sentiment",
        color_discrete_map={
            "positive": "#2ecc71",
            "negative": "#e74c3c",
            "neutral":  "#95a5a6"
        }
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Tab 4 : Pleine Lune ───────────────────────────────────────
with tab4:
    st.header("🌕 Impact des nuits de pleine lune sur les avis")

    df = con.execute("SELECT * FROM main_gold.gold_full_moon_impact").df()

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            df, x="sentiment", y="nb_reviews",
            color="period_type", barmode="group",
            title="Nombre d'avis : pleine lune vs nuit normale",
            labels={
                "nb_reviews":  "Nombre d'avis",
                "period_type": "Période",
                "sentiment":   "Sentiment"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(
            df, x="sentiment", y="pct_within_period",
            color="period_type", barmode="group",
            title="Répartition (%) des sentiments par période",
            labels={
                "pct_within_period": "% des avis",
                "period_type":       "Période",
                "sentiment":         "Sentiment"
            }
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Tableau comparatif")
    pivot = df.pivot_table(
        index="sentiment",
        columns="period_type",
        values="pct_within_period"
    ).reset_index()
    st.dataframe(pivot, use_container_width=True)

    st.info(
        "💡 Si le % de sentiments négatifs est plus élevé en pleine lune, "
        "cela suggère un impact sur la satisfaction des voyageurs."
    )

con.close()