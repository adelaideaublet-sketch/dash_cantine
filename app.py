import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

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
        fig = px.bar(freq, x=col, y="Effectifs", title=f"Répartition – {col}")

    graphs.append(dcc.Graph(figure=fig))

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Analyse questionnaires cantine"),
    *graphs
], style={"width": "90%", "margin": "auto"})

if __name__ == "__main__":
    app.run_server()

