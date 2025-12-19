import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# Chargement et nettoyage
df = pd.read_excel("Questionnaires_cantine_choix_multiples.xlsm")
df = df.fillna("absence de réponse")

def clean_string(x):
    if isinstance(x, str):
        return " ".join(x.strip().split())
    return x

df = df.applymap(clean_string)

graphs = []

for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]):
        fig = px.histogram(df, x=col, title=f"Distribution – {col}")
    else:
        freq = df[col].value_counts().reset_index()
        freq.columns = [col, "Effectifs"]
        freq["Pourcentage"] = 100 * freq["Effectifs"] / freq["Effectifs"].sum()

        fig = px.bar(
            freq,
            x=col,
            y="Pourcentage",
            text="Effectifs",  # Affiche l’effectif au-dessus
            title=f"Répartition – {col}",
            labels={"Pourcentage": "Pourcentage (%)"},
            color="Pourcentage",  # effet visuel proportionnel
            color_continuous_scale="Blues"
        )

        fig.update_traces(textposition='outside')  # effectifs au-dessus des barres
        fig.update_yaxes(range=[0, 110], ticksuffix="%")  # axe y en pourcentage

    graphs.append(dcc.Graph(figure=fig))

# Dash App
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Analyse questionnaires cantine"),
    *graphs
], style={"width": "90%", "margin": "auto"})

if __name__ == "__main__":
    app.run_server()
