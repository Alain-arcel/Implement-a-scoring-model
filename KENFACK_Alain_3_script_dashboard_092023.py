# Importation des bibliothèques
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import requests
import pandas as pd
import plotly.graph_objects as go
import json




# Liste des variables pertinentes
relevant_features = [
    "EXT_SOURCE_2", "EXT_SOURCE_3", "CODE_GENDER", "BURO_AMT_CREDIT_MAX_OVERDUE_MEAN",
    "AMT_GOODS_PRICE", "INSTAL_DPD_MEAN", "DAYS_EMPLOYED", "INSTAL_AMT_PAYMENT_SUM", "AMT_ANNUITY"
]

# Récupération des IDs clients depuis l'API
def get_client_ids():
    api_url = "http://127.0.0.1:8000/client_ids"
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json()
    else:
        return []

# Récupération de la liste des features
def get_features():
    api_url = "http://127.0.0.1:8000/features"
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json()
    else:
        return []

# Création de l'application Dash et utilisation du thème FLATLY de Bootstrap
app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])
server = app.server

# Mise en page de l'application
# Définition de l'en-tête de l'application avec un titre, un sous-titre et un arrière-plan coloré
header = html.Div(
    [
        html.H1('Tableau de bord de gestion des risques', style={'color': 'white', 'fontWeight': 'bold', }),
        html.P("Support d'aide à la décision pour l'octroi d'un crédit", style={'color': 'w','fontStyle': 'italic', "fontWeight" : "bold"}),
    ],
    style={'backgroundColor': '#ef4155', 'textAlign': 'center'}
)

# Définition de la barre latérale de l'application
sidebar = html.Div(
    [
        dbc.Row(
            [
                # Titre de la barre latérale
                html.H5('Choix des informations à afficher',
                        style={'marginTop': '12px', 'marginLeft': '4px', "fontSize" : "18px"})
            ],
            style={"height": "8vh"},
            className='bg-info text-white font-italic'
        ),
        dbc.Row(
            [
                html.Div([
                    # Sélection de l'idendifiant client
                    html.P('Idendifiant client',
                           style={'marginTop': '8px', 'marginBottom': '4px', 'textAlign': 'center', "fontSize" : "14px"},
                           className='fontWeight-bold'),
                    dcc.Dropdown(id='client-dropdown', multi=False,
                                 options=[{'label': str(client_id), 'value': client_id}
                        for client_id in get_client_ids()],
                                 style={'width': '280'}
                                 ),
                    # Sélection de la variable pour la comparaison avec les autres clients
                    html.P('Comparaison aux autres clients',
                           style={'marginTop': '16px', 'marginBottom': '4px', 'textAlign': 'center'},
                           className='fontWeight-bold'),
                    dcc.Dropdown(id='variable-dropdown', multi=False,
                                 options=[{'label': variable, 'value': variable}
                                          for variable in get_features()],
                                 style={'width': '280'}
                                 ),
                    
                    # Sélection les informations supplémentaires
                    html.P('Informations supplémentaires à afficher',
                           style={'marginTop': '16px', 'marginBottom': '4px', 'textAlign': 'center', "fontSize" : "14px"},
                           className='fontWeight-bold'),
                    dcc.Checklist(
                        id='info-checklist',
                        options=[
                            {'label': 'Informations influençant la décision', 'value': 'decision'},
                            {'label': 'Comparaison aux clients similaires', 'value': 'comparison'},
                            {'label' : "Comparaison à l'ensemble des clients", "value" : "comparison_all"},
                            {'label': 'Dérive des données', 'value': 'drift'},
                            {'label': "Importances des variables", 'value': 'importance'}
                        ],
                        value=[],  # Aucune option sélectionnée par défaut
                        style={'width': '320px', "fontSize" : "14px"}),
                    # Bouton pour appliquer les sélections
                    html.Button(id='my-button', n_clicks=0, children='Appliquer les sélections',
                                style={'marginTop': '16px', 'textAlign': 'center'},
                                className='bg-success text-white')
                ])
            ],
            style={'height': '50vh', 'margin': '8px'}
        ),
    ]
)

# Définition du contenu principal de l'application
content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Décision de crédit',
                               className='bg-info text-white fontWeight-bold', style={"margin": "8px"}),
                        html.Div(id='credit-decision-output', style={"marginTop": "-10px"})
                    ]
                ),  # Ajout de la virgule ici
                dbc.Col(
                    [
                        html.P('Informations personnelles du client', className='bg-info text-white fontWeight-bold', style={"margin": "8px"}),
                        html.Div(id='client-info-output', style={"height": "45vh", 'margin': '8px', "marginTop": "60px", 'textAlign': 'center', "fontSize": "14px"})
                    ]
                )
            ],
            style={'height': '50vh',
                   'marginTop': '16px', 'marginLeft': '8px',
                   'marginBottom': '0px', 'marginRight': '8px', 'textAlign': 'center'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Informations influençant la décision',
                               className='bg-info text-white fontWeight-bold', style = {"margin" : "8px"}),
                        dcc.Graph(id='shap-client')
                        ]
                )],
                style={'height': '50vh',
                   'marginTop': '150px', 'marginLeft': '8px',
                   'marginBottom': '8px', 'marginRight': '8px', 'textAlign': 'center'}),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Comparaison aux clients similaires',
                               className='bg-info text-white fontWeight-bold', style = {"margin" : "8px"}),
                        dcc.Graph(id = "nearest-neighbors-plot")
                        
                    ]
                ),
                
            ],
            style={'height': '50vh',
                   'marginTop': '170px', 'marginLeft': '8px',
                   'marginBottom': '8px', 'marginRight': '8px', 'textAlign': 'center'}
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P("Comparaison du client à l'ensemble des clients",
                               className='bg-info text-white fontWeight-bold', style = {"margin" : "8px"}),
                        dcc.Graph(id = "comparison-to-all-clients-plot")
                    ]
                )],
                style={'height': '50vh',
                   'marginTop': '180px', 'marginLeft': '8px',
                   'marginBottom': '8px', 'marginRight': '8px', 'textAlign': 'center'}),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Dérive des données',
                               className='bg-info text-white fontWeight-bold', style = {"margin" : "8px"}),
                        dcc.Graph(id = "data-drift-plot")
                    ]
                )
            ],
            style={'height': '50vh',
                   'marginTop': '200px', 'marginLeft': '8px',
                   'marginBottom': '30px', 'marginRight': '8px', 'textAlign': 'center'}
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Importances des variables',
                               className='bg-info text-white fontWeight-bold', style = {"margin" : "8px"}),
                    dcc.Graph(id='shap-values-plot')
                    ]
                )
            ],
            style={'height': '50vh',
                   'marginTop': '200px', 'marginLeft': '8px',
                   'marginBottom': '8px', 'marginRight': '8px', 'textAlign': 'center'}
        )
    ]
)

# Configuration de la mise en page de l'application avec la barre latérale et le contenu principal

app.layout = dbc.Container(
    [
        header,
        dbc.Row(
            [
                dbc.Col(sidebar, width=3, className='bg-light'),
                dbc.Col(content, width=9)]
        )],
    fluid=True
)


# Fonction pour afficher les informations du client avec Plotly
@app.callback(
    Output('client-info-output', 'children'),
    [Input('client-dropdown', 'value')]
)

def display_client_info(client_id):
    if client_id is None:
        return ""

    # Appel de l'API pour obtenir les informations du client
    api_url = f"http://127.0.0.1:8000/client_data/{client_id}"
    response = requests.get(api_url)

    if response.status_code == 200:
        client_data = response.json()

        # Création d'un dataframe à partir des données du client
        df_client = pd.DataFrame(client_data)

        # Création du dictionnaire de correspondance des noms de colonnes renommées
        noms_colonnes_renommees = {
            'CODE_GENDER': 'Sexe',
            'DAYS_BIRTH': 'Âge',
            'NAME_FAMILY_STATUS_MARRIED': 'Marié',
            'CNT_CHILDREN': 'Enfant',
            'FLAG_OWN_CAR': 'Véhiculé',
            'FLAG_OWN_REALTY': 'Bien immobilier',
            'DAYS_EMPLOYED': "Années d'expérience",
        }

        # Renommer les colonnes du DataFrame
        df_client.rename(columns=noms_colonnes_renommees, inplace=True)

        # Convertir la colonne "âge" de jours en années
        df_client['Âge'] = round(df_client['Âge'] / -365,0)

        # Convertir la colonne "Nombre de jour de travail" de jours en années
        df_client["Années d'expérience"] = round(df_client["Années d'expérience"] / -365,0)

        # Sélection des colonnes à afficher
        colonnes_a_afficher = ['Sexe', 'Âge', 'Marié', 'Enfant', 'Véhiculé', 'Bien immobilier', "Années d'expérience"]

        # Création d'un tableau Plotly pour afficher les informations du client
        tableau_data = [go.Table(
            header=dict(
                values=['<b>Attribut</b>', "<b>Valeur</b>"],
                line_color='white', fill_color="#ef4155",
                align=['left', 'center'], font=dict(color='white', size=12)),
            cells=dict(values=[colonnes_a_afficher, df_client[colonnes_a_afficher].values[0]],
                    line_color='darkslategray',
                    fill=dict(color=['dodgerblue', 'white']),
                    align=['left', 'center'], font_size=10)
        )]

        # Ajout de conditions pour transformer les valeurs avant l'affichage
        for i, colonne in enumerate(colonnes_a_afficher):
            if colonne == 'Sexe':
                # Transformation de la colonne 'sexe' en 'M' pour masculin et 'F' pour féminin
                if df_client[colonne].values[0] == '0':
                    tableau_data[0]['cells']['values'][1][i] = 'M'
                else:
                    tableau_data[0]['cells']['values'][1][i] = 'F'
            elif colonne == 'Marié':
                # Transformation de la colonne 'Marié' en 'Oui' ou 'Non'
                if df_client[colonne].values[0] == '1':
                    tableau_data[0]['cells']['values'][1][i] = 'Oui'
                else:
                    tableau_data[0]['cells']['values'][1][i] = 'Non'
            elif colonne == 'Véhiculé':
                # Transformation de la colonne 'Véhiculé' en 'Oui' ou 'Non'
                if df_client[colonne].values[0] == '0':
                    tableau_data[0]['cells']['values'][1][i] = 'Non'
                else:
                    tableau_data[0]['cells']['values'][1][i] = 'Oui'

        # Création de la figure Plotly avec mise en page
        figure = {
            'data': tableau_data,
            'layout': {
                'height': 300,
                'margin': dict(t=20, b=20, l=0, r=0)
            }
        }

        # Retournez la figure dans le callback
        return [dcc.Graph(figure=figure)]

# Fonction pour afficher la décision de crédit
@app.callback(
    Output('credit-decision-output', 'children'),
    [Input('client-dropdown', 'value')]
)
def generate_credit_decision(client_id):
    """
    Génère la décision de crédit en fonction de l'ID du client sélectionné.
    Affiche le score du client en pourcentage et colore la décision en vert si le crédit est accordé, en rouge sinon.
    """
    if client_id is None:
        return ""

    # Appel de l'API pour obtenir la décision de crédit
    api_url = f"http://127.0.0.1:8000/credit/{client_id}"
    response = requests.get(api_url)

    if response.status_code == 200:
        API_data = response.json()
        classe_predite = API_data['Prédiction']
        proba = 1 - API_data['Probabilité']
        client_score = round(proba * 100, 2)
        decision_color = "green" if classe_predite == 0 else "red"
        decision = "Risque d'insolvabilité : Crédit refusé" if classe_predite == 1 else "Client solvable : Crédit accordé"

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=client_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Score du client et décision de crédit", "font": {"size": 14}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "white"},
                'steps': [
                    {'range': [0, 25], 'color': "green"},
                    {'range': [25, 50], 'color': "limegreen"},
                    {'range': [50, 75], 'color': "orange"},
                    {'range': [75, 100], 'color': "red"}
                ]
            }
        ))

        # Ajoutez une annotation texte à l'intérieur de la jauge
        fig.add_annotation(
            text=decision,
            x=0.5,  # Position horizontale au centre de la jauge
            y=0.2,  # Position verticale au centre de la jauge
            showarrow=False,  # N'affiche pas de flèche
            font={'size': 12, 'color': decision_color}
        )

        # Réduisez l'espace en ajustant la marge supérieure (t) à -10 pixels
        fig.update_layout(margin=dict(t=0))

        return [
            dcc.Graph(figure=fig)
        ]

    else:
        return "Client ID non valide ou introuvable."


# Comparaison du client sélectionné aux clients similaires
@app.callback(
    Output("nearest-neighbors-plot", "figure"),
    Input("my-button", "n_clicks"),
    Input("client-dropdown", "value"),
    Input("variable-dropdown", "value"),
    Input("info-checklist", "value"),
)
def update_nearest_neighbors_plot(n_clicks, selected_client, selected_variable, selected_info):
    if n_clicks is None or not selected_client or not selected_variable or "comparison" not in selected_info:
        # Si le bouton n'a pas été cliqué ou les sélections ne sont pas complètes, retournez une figure vide
        return go.Figure()
    
    # Appeler l'API pour obtenir les données du client sélectionné
    client_data_response = requests.get(f"http://127.0.0.1:8000/client_data/{selected_client}")
    client_data = client_data_response.json()

    # Appeler l'API pour obtenir les plus proches voisins
    neighbors_data_response = requests.get(f"http://127.0.0.1:8000/nearest_neighbors/{selected_client}")
    neighbors_data = neighbors_data_response.json()
    
    # Extraire les identifiants clients et les valeurs de la variable sélectionnée pour le client sélectionné et ses voisins
    client_id = client_data[0]["SK_ID_CURR"]
    client_value = client_data[0][selected_variable]
    neighbors_ids = [data["SK_ID_CURR"] for data in neighbors_data]
    neighbors_values = [data[selected_variable] for data in neighbors_data]
    
    # Créer un displot
    fig = go.Figure()
    
    # Ajouter les valeurs du client sélectionné
    fig.add_trace(go.Bar(x=[client_id], y=[client_value], name="Client sélectionné"))
    
    # Ajouter les valeurs des voisins
    fig.add_trace(go.Bar(x=neighbors_ids, y=neighbors_values, name="Clients similaires"))
    
    # Mettre en forme le graphique
    fig.update_layout(
        title=f"Comparaison de {selected_variable} pour le client {selected_client}",
        xaxis_title="Identifiant client",
        yaxis_title=selected_variable,
        barmode="group"  # Pour afficher les barres groupées
    )
    
    return fig


@app.callback(
    Output("comparison-to-all-clients-plot", "figure"),
    Input("my-button", "n_clicks"),
    Input("client-dropdown", "value"),
    Input("variable-dropdown", "value"),
    Input("info-checklist", "value"),
)
def update_comparison_to_all_clients_plot(n_clicks, selected_client, selected_variable, selected_info):
    if n_clicks is None or not selected_client or not selected_variable or "comparison_all" not in selected_info:
        # Si le bouton n'a pas été cliqué ou les sélections ne sont pas complètes, retournez une figure vide
        return go.Figure()

    # Appeler l'API pour obtenir les données du client sélectionné
    client_data_response = requests.get(f"http://127.0.0.1:8000/client_data/{selected_client}")
    client_data = client_data_response.json()

    # Appeler l'API pour obtenir l'ensemble des données clients
    all_clients_data_response = requests.get("http://127.0.0.1:8000/all_clients_data")
    all_clients_data = all_clients_data_response.json()

    # Extraire les identifiants clients et les valeurs de la variable sélectionnée pour le client sélectionné et l'ensemble des clients
    client_id = selected_client
    client_value = client_data[0][selected_variable]
    all_clients_ids = [data["SK_ID_CURR"] for data in all_clients_data]
    all_clients_values = [data[selected_variable] for data in all_clients_data]

    # Créer un histogramme
    fig = go.Figure()

    # Ajouter l'histogramme du client sélectionné
    fig.add_trace(go.Bar(x=[client_id], y=[client_value], name="Client sélectionné"))

    # Ajouter l'histogramme de l'ensemble des clients
    fig.add_trace(go.Bar(x=all_clients_ids, y=all_clients_values, name="Tous les clients"))

    # Mettre en forme le graphique
    fig.update_layout(
        title=f"Comparaison de {selected_variable} pour le client {selected_client} avec l'ensemble des clients",
        xaxis_title="Identifiant client",
        yaxis_title=selected_variable,
        barmode="group"  # Pour afficher les barres groupées
    )

    return fig



# Ajoutez ce callback pour afficher le graphique des valeurs SHAP par client

@app.callback(
    Output('shap-client', 'figure'),
    Input('my-button', 'n_clicks'),
    Input('info-checklist', 'value'),
    Input('client-dropdown', 'value'),
    Input('variable-dropdown', 'value')
)
def update_shap_waterfall(n_clicks, info_checklist, client_id, variable):
    if 'decision' in info_checklist and n_clicks > 0:
        if client_id is not None and variable is not None:
            # Faites une requête à l'API pour récupérer les valeurs SHAP
            api_url = f"http://127.0.0.1:8000/shap_values/{client_id}"
            response = requests.get(api_url)

            if response.status_code == 200:
                shap_values_json = response.json()
                features = shap_values_json["features"]
                values = shap_values_json["values"]

                # Triez les valeurs SHAP par ordre décroissant
                sorted_shap_values = sorted(zip(features, values[0]), key=lambda x: abs(x[1]), reverse=True)


                # Sélectionnez les 10 valeurs SHAP les plus importantes
                top_10_shap_values = sorted_shap_values[:10]

                # Séparez les noms de variables et les valeurs
                variable_names, shap_scores = zip(*top_10_shap_values)

                # Créez un graphique Waterfall avec des barres rouges et bleues
                fig = go.Figure(go.Waterfall(
                    name="",
                    orientation="v",
                    measure=["relative" if score >= 0 else "total" for score in shap_scores],
                    x=variable_names,
                    text=["+" + str(round(score, 4)) if score >= 0 else str(round(score, 4)) for score in shap_scores],
                    y=shap_scores,
                    connector={"line": {"color": "blue"}},
                ))

                fig.update_layout(
                    title=f"Valeurs SHAP pour le client {client_id}",
                    font = dict(size = 12),                   
                    xaxis_title="Variables",
                    yaxis_title="SHAP Values"
                )

                return fig

    return go.Figure()


# Callback pour afficher le graphique des valeurs SHAP pour l'ensemble du jeu de données

@app.callback(
    Output('shap-values-plot', 'figure'),
    Input('my-button', 'n_clicks'),
    Input('info-checklist', 'value')
)
def update_shap_values_plot(n_clicks, info_checklist):
    if 'importance' in info_checklist and n_clicks > 0:
        # Faites une requête à l'API pour récupérer les valeurs SHAP pour l'ensemble du jeu de données
        api_url = "http://127.0.0.1:8000/shap"
        response = requests.get(api_url)

        if response.status_code == 200:
            shap_values_json_all = response.json()
            features = shap_values_json_all["features"]
            values = shap_values_json_all["values"]

            # Triez les valeurs SHAP par ordre décroissant
            sorted_shap_values = sorted(zip(features, values[0]), key=lambda x: abs(x[1]), reverse=True)

            # Sélectionnez les 10 valeurs SHAP les plus importantes
            top_10_shap_values = sorted_shap_values[:10]

            # Séparez les noms de variables et les valeurs
            variable_names, shap_scores = zip(*top_10_shap_values)

            # Créez un graphique Waterfall avec des barres rouges et bleues
            fig = go.Figure(go.Waterfall(
                name="",
                orientation="v",
                measure=["relative" if score >= 0 else "total" for score in shap_scores],
                x=variable_names,
                text=["+" + str(round(score, 4)) if score >= 0 else str(round(score, 4)) for score in shap_scores],
                y=shap_scores,
                connector={"line": {"color": "blue"}},
            ))

            fig.update_layout(
                title="Valeurs SHAP les plus importantes pour l'ensemble du jeu de données",
                xaxis_title="Variables",
                yaxis_title="SHAP Values"
            )

            return fig

    return go.Figure()

# Fonction pour analyser le data drift
@app.callback(Output('data-drift-plot', 'figure'),
              Input('my-button', 'n_clicks'),
              Input('info-checklist', 'value'))

def update_data_drift_plot(n_clicks, info_checklist):
    if "drift" in info_checklist and n_clicks > 0:
        api_url = "http://127.0.0.1:8000/data_drift"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()

            # Conversion des données en un dictionnaire Python
            data_dict = json.loads(data)

            # Extraction des informations pertinentes
            drift_data = data_dict["metrics"][1]["result"]["drift_by_columns"]

            # Création des listes pour stocker ces informations 
            column_names = []
            column_types = []
            drift_scores = []
            drift_detected = []
            stattest_names = []

            # Extraction des informations pour les ajouter dans les listes
            for column, info in drift_data.items():
                column_names.append(column)
                column_types.append(info["column_type"])
                drift_scores.append(info["drift_score"])
                drift_detected.append(info["drift_detected"])
                stattest_names.append(info["stattest_name"])

            # Création d'un dataframe pour stocker les informations
            df = pd.DataFrame({
                "column_name": column_names,
                "column_type": column_types,
                "drift_score": drift_scores,
                "drift_detected": drift_detected,
                "stattest_name": stattest_names})
            
            # Arrondir les valeurs des colonnes "drift_score" à 2 décimales
            df["drift_score"] = df["drift_score"].round(2)

            # Création d'un tableau de données drift
            # Condition basée sur dataset_drift
            dataset_drift = False  
            if dataset_drift:
                drift_status_text = "Attention : il y a dérive dans les données"
            else:
                drift_status_text = "Pas de data drift dans les données"
            
            fig = go.Figure(data=[go.Table(
                header=dict(
                    values=["<b>column_name</b>", "<b>column_type</b>", "<b>drift_score</b>", "<b>drift_detected</b>", "<b>stattest_name</b>"],
                    line_color='white', fill_color="#ef4155",
                    align='center', font=dict(color='white', size=12)),
                    cells=dict(
                        values=[df.column_name, df.column_type, df.drift_score, df.drift_detected, df.stattest_name],
                        line_color= "white", fill_color=[["white","rgb(189, 215, 231)","white", "rgb(189, 215, 231)","white"]*360],
                        align='center', font=dict(color='black', size=10),height=30))
                    ])

            # Ajouter un texte au-dessus du tableau
            fig.add_annotation(
                text=drift_status_text,
                x=0,
                y=1.1,
                showarrow=False,
                font=dict(size=12, color="blue")
                )
            fig.update_layout(width = 1300)

            return fig
        
    return go.Figure()



# Exécution de l'application si ce fichier est exécuté directement
if __name__ == "__main__":
    app.run_server(debug=True, host='127.0.0.1', port=1234)