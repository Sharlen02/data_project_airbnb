# 🏠 Airbnb Analytics Platform

Plateforme analytique des données Airbnb construite avec **dbt**, **DuckDB** et **Streamlit**.

---

## 📋 Présentation du projet

Ce projet met en place un pipeline de données complet permettant d'analyser :
- Les logements Airbnb (prix, types, disponibilités)
- Les performances des hôtes (superhosts vs hôtes normaux)
- Les avis clients et leur évolution dans le temps
- L'impact des nuits de pleine lune sur les sentiments des avis

---

## 👥 Répartition des tâches

| Membre | Rôle | Responsabilités |
|--------|------|-----------------|
| **Bientakonné KARAMBIRI** | Data Engineer – Bronze | Setup dbt, seeds, modèles Bronze, configuration DuckDB |
| **Stephen AGGEY** | Data Engineer – Silver | Nettoyage des données, typage, tests qualité dbt |
| **Sharlen D'ALMEIDA** | Data Analyst – Gold & Streamlit | Agrégats métier, dashboard Streamlit |

### Architecture

```
CSV Sources
    │
    ▼
dbt Seeds (DuckDB)
    │
    ├── Bronze (vues brutes)
    │       │
    ├── Silver (nettoyage, typage)
    │       │
    └── Gold  (analyses métier)
                │
                ▼
        Dashboard Streamlit
```

### Stack technique

| Outil | Rôle |
|-------|------|
| DuckDB | Moteur analytique |
| dbt (dbt-fusion) | Transformations et tests |
| Streamlit | Dashboard interactif |
| Plotly | Visualisations |
| Git / GitHub | Versioning collaboratif |

---

## 📁 Structure du projet

```
data_project_airbnb/
├── airbnb_analytics/           ← Projet dbt
│   ├── models/
│   │   ├── bronze/             ← Vues brutes (SELECT * depuis seeds)
│   │   │   ├── schema.yml
│   │   │   ├── bronze_listings.sql
│   │   │   ├── bronze_hosts.sql
│   │   │   ├── bronze_reviews.sql
│   │   │   └── bronze_full_moon_dates.sql
│   │   ├── silver/             ← Nettoyage et typage
│   │   │   ├── schema.yml
│   │   │   ├── silver_listings.sql
│   │   │   ├── silver_hosts.sql
│   │   │   ├── silver_reviews.sql
│   │   │   └── silver_full_moon_dates.sql
│   │   └── gold/               ← Analyse métier
│   │       ├── schema.yml
│   │       ├── gold_listings_summary.sql
│   │       ├── gold_host_performance.sql
│   │       ├── gold_reviews_sentiment.sql
│   │       └── gold_full_moon_impact.sql
│   ├── seeds/
│   │   ├── schema.yml
│   │   ├── listings.csv        ← Non versionné (Ajouter les tables de données)
│   │   ├── hosts.csv           ← Non versionné (Ajouter les tables de données)
│   │   ├── reviews.csv         ← Non versionné (Ajouter les tables de données)
│   │   └── seed_full_moon_dates.csv ← Non versionné (Ajouter les tables de données)
│   ├── seeds/scripts/
│   │   └── load_reviews.py     ← Chargement manuel reviews (ligne malformée)
│   ├── tests/
│   │   ├── assert_price_positive.sql
│   │   └── assert_sentiment_coverage.sql
│   ├── dbt_project.yml
│   └── profiles.yml.example
├── streamlit/
│   └── app.py                  ← Dashboard Streamlit
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Prérequis

- Python 3.10+
- Git

### 1. Cloner le dépôt

```bash
git clone https://github.com/Sharlen02/data_project_airbnb.git
cd data_project_airbnb
```

### 2. Créer l'environnement virtuel

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer le profil dbt

Copier le fichier exemple et l'adapter :

```bash
cp airbnb_analytics/profiles.yml.example ~/.dbt/profiles.yml
```

Éditer `~/.dbt/profiles.yml` et adapter le chemin :

```yaml
airbnb_analytics:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: "/chemin/absolu/vers/data_project_airbnb/airbnb_analytics/dev.duckdb"
      threads: 4
```

---

## 📦 Données sources

Les fichiers CSV ne sont pas versionnés (taille > 100 MB).  
Les télécharger depuis le lien partagé par l'équipe et les placer dans `airbnb_analytics/seeds/` :

airbnb_analytics/seeds/
''
├── [hosts.csv](https://logbrain-datasets.s3.eu-west-1.amazonaws.com/airbnb/hosts.csv)  
├── [reviews.csv](https://logbrain-datasets.s3.eu-west-1.amazonaws.com/airbnb/reviews.csv)   
├── [listings.json](https://logbrain-datasets.s3.eu-west-1.amazonaws.com/airbnb/listings.csv)   
└── [seed_full_moon_dates.csv](https://logbrain-datasets.s3.eu-west-1.amazonaws.com/airbnb/seed_full_moon_dates.csv)

---

## 🚀 Lancer le pipeline

### 1. Charger les seeds

```bash
cd airbnb_analytics

# Charger listings, hosts et full_moon_dates
dbt seed --select listings hosts seed_full_moon_dates

# Charger reviews séparément (ligne malformée ligne 18028)
python seeds/scripts/load_reviews.py
```

### 2. Lancer les transformations

```bash
dbt run
```

### 3. Lancer les tests qualité

```bash
dbt test
```

### 4. Générer la documentation dbt

```bash
dbt compile --write-catalog
dbt docs serve
```

### 5. Lancer le dashboard Streamlit

```bash
# Depuis la racine data_project_airbnb/
streamlit run streamlit/app.py
# Ouvre http://localhost:8501
```

---

## 📊 Fonctionnalités du dashboard

| Onglet | Contenu |
|--------|---------|
| 📊 Logements | Prix moyen, répartition par type, nuits minimum |
| 👤 Hôtes | Superhosts vs hôtes normaux, prix et avis comparés |
| 💬 Avis | Évolution mensuelle des sentiments, filtres par année |
| 🌕 Pleine Lune | Impact des nuits de pleine lune sur les sentiments |

---

## 🧪 Tests dbt

| Test | Modèle | Type |
|------|--------|------|
| `unique` + `not_null` sur `id` | silver_listings, silver_hosts | Générique |
| `accepted_values` sur `room_type` | silver_listings | Générique |
| `accepted_values` sur `sentiment` | silver_reviews | Générique |
| `relationships` host_id → hosts | silver_listings | Générique |
| `relationships` listing_id → listings | silver_reviews | Générique |
| Prix strictement positif | silver_listings | Custom |
| Sentiment dans les valeurs attendues | silver_reviews | Custom |

---

## ⚠️ Problèmes connus

### reviews.csv — ligne malformée (ligne 18028)

Le fichier `reviews.csv` contient une ligne avec des guillemets non conformes au standard CSV. `dbt seed` ne peut pas la charger directement. La solution est d'utiliser le script Python dédié qui active `ignore_errors = true` via DuckDB :

```bash
python airbnb_analytics/seeds/scripts/load_reviews.py
```

La ligne ignorée correspond à l'avis du listing `271340` du `2016-05-04`.

---

## 🌿 Branches Git

| Branche | Responsable | Contenu |
|---------|-------------|---------|
| `main` | Sharlen | Version stable |
| `develop` | Tous | Intégration continue |
| `bronze/bientakonne` | Bientakonne | Couche Bronze + infrastructure |
| `silver/stephen` | Stephen | Couche Silver + tests qualité |
| `gold/sharlen` | Sharlen | Couche Gold + Streamlit |
