import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st
import pandas as pd

st.title("Chargement et fusion de données d'accidents")

## Chargement des données
@st.cache_data
def load_data(file):
    return pd.read_csv(file, sep=';', decimal=',')

caract_file = st.file_uploader("Chargez le fichier caract-2023.csv", type="csv")
lieux_file = st.file_uploader("Chargez le fichier lieux-2023.csv", type="csv")
vehicules_file = st.file_uploader("Chargez le fichier vehicules-2023.csv", type="csv")
usagers_file = st.file_uploader("Chargez le fichier usagers-2023.csv", type="csv")

if caract_file and lieux_file and vehicules_file and usagers_file:
    caract_df = load_data(caract_file)
    lieux_df = load_data(lieux_file)
    vehicules_df = load_data(vehicules_file)
    usagers_df = load_data(usagers_file)

    ## Fusion des bases de données
    merged_df = caract_df.merge(lieux_df, on='Num_Acc')
    merged_df = merged_df.merge(vehicules_df, on='Num_Acc')
    merged_df = merged_df.merge(usagers_df, on='Num_Acc')

    # Supprimer les doublons
    merged_df = merged_df.drop_duplicates()

    # Vérifier que les doublons ont été supprimés
    print(f"Nombre de doublons après suppression : {merged_df.duplicated().sum()}")
    print(f"Dimensions du DataFrame après suppression des doublons : {merged_df.shape}")
    # Définir les codes des véhicules motorisés
    codes_motorises = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14]

    # Filtrer les données pour conserver uniquement les véhicules motorisés
    accidents_motorises = merged_df[merged_df['catv'].isin(codes_motorises)]

    accidents_motorises['lat'] = pd.to_numeric(accidents_motorises['lat'], errors='coerce')
    accidents_motorises['long'] = pd.to_numeric(accidents_motorises['long'], errors='coerce')
    accidents_motorises.loc[:, 'dep'] = pd.to_numeric(accidents_motorises['dep'], errors='coerce')
    accidents_motorises.loc[:, 'com'] = pd.to_numeric(accidents_motorises['com'], errors='coerce')

    
    st.success("Les données ont été chargées et fusionnées avec succès!")
    st.write("Aperçu des données fusionnées :")
    st.dataframe(merged_df.head())

    ## Affichage des statistiques
    st.subheader("Statistiques des données fusionnées")
    st.write(merged_df.describe())

else:
    st.warning("Veuillez charger tous les fichiers CSV pour procéder à la fusion des données.")


import pandas as pd
import plotly.express as px

# Titre de l'application
st.title("Visualisation des accidents motorisés")

# Ajout de la description de la gravité
gravite_dict = {
    1: "Blessé léger",
    2: "Indemne",
    3: "Blessé hospitalisé",
    4: "Tué"
}
accidents_motorises['grav_desc'] = accidents_motorises['grav'].map(gravite_dict)

# Filtrage des lignes avec des valeurs valides
accidents_motorises = accidents_motorises.dropna(subset=['lat', 'long', 'grav_desc'])

# Création de la carte
fig = px.scatter_mapbox(
    accidents_motorises,
    lat='lat',
    lon='long',
    color='grav_desc',
    color_discrete_map={
        "Indemne": "#0080ff",
        "Blessé léger": "#ffff66",
        "Blessé hospitalisé": "#ff9933",
        "Tué": "#ff3300"
    },
    title="Répartition géographique des accidents motorisés par gravité",
    mapbox_style="open-street-map",
    zoom=12,
    height=800,
    hover_name='grav_desc'
)

fig.update_layout(legend_title="Gravité")

# Affichage de la carte dans Streamlit
st.plotly_chart(fig, use_container_width=True)

# Affichage des données brutes (optionnel)
if st.checkbox("Afficher les données brutes"):
    st.write(accidents_motorises)
