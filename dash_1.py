# Import packages
from dash import Dash, html, dash_table, dcc, callback
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

df = pd.read_csv('https://raw.githubusercontent.com/chriszapp/datasets/main/books.csv', on_bad_lines = 'skip')

df.rename (columns={'  num_pages' : "Number_pages"}, inplace= True )

df_news = df.sort_values(by="Number_pages", ascending=False).iloc[:10]

#Utilisez Plotly Express pour créer un graphique en barres des 10 premiers livres, en affichant le nombre de pages par titre.

figure_1=px.histogram(df, x='Number_pages', y='title', title='')

figure_1.update_layout(
    xaxis_title="Numbers of pages", yaxis_title="Title of book"
)
figure_1


# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


# Définition du layout
#app.layout = html.Div([
                       # html.H1("Dashboard of BOOKS")])

# Définir la mise en page
app.layout = dbc.Container([

                    dbc.Row([html.Div([
                                     # Titre principal
                                 dbc.Col(html.H1("Dashboard of THE BOOK", style={'textAlign': 'center', 'color': 'blue'})),

                                      # Dataset
                                 dbc.Col(html.H2('Book Authors Data')),
                                 dbc.Col(html.H3('Sample of Book Dataset')),
                                 dbc.Col(dash_table.DataTable(data=df_news.to_dict('records'), page_size=10)),

                                      # ajout de 2 lignes de séparations
                                      html.Br(),
                                      html.Br()
                                        ])   ]),

                                      # Dropdown
                    dbc.Row([html.Div([
                                      dbc.Col(html.H2('Book Authors Select')),
                                      dbc.Card(
                                                    dbc.CardBody(
                                                        [
                                                        html.H3('Select your Author')
                                                        ]
                                                                )
                                                    ),

                                       dbc.Col(dcc.Dropdown(options=[{'label': i, 'value': i} for i in df['authors'].unique()],
                                              placeholder="Select an Author", id='dropdown_select')),

                                      # ajout de 2 lignes de séparations
                                      html.Br(),
                                      html.Br()
                                      ])
                                      ,

                                      # My_slider
                    dbc.Row([    dbc.Col(html.H3 ('Select numbers of Pages')) ]),
                    dbc.Row([    dbc.Col(dcc.Slider(min = df['Number_pages'].min(),
                                                 max=df['Number_pages'].max(),
                                                 value=df['Number_pages'].max(),
                                                  step= 1000,
                                                 id='my-slider')),

                                      # ajout de 2 lignes de séparations
                                      html.Br(),
                                      html.Br()
                                       ])
                                       ]),


                                      # Espace de mise à jour graphique
                                      # My_histrogramme
                     dbc.Row([   dbc.Col(dcc.Graph(id ='Histogramme'))


                                      ])

                          ])



#style = { 'backgound-color': 'black', 'color' : 'white' }

# fonction de rappel
@app.callback(
    Output(component_id='Histogramme', component_property='figure'),
    [Input(component_id='dropdown_select', component_property='value'),
    Input(component_id='my-slider', component_property='value')])


def update_graph(auteur, nb_de_pages):

    #Filtrage des données:
    filtered_data = df[(df['authors'] == auteur) & (df['Number_pages'] <= nb_de_pages)]

    # creation of graph
    fig = px.bar(filtered_data, x= 'Number_pages', y="title")
    fig.update_layout(title = f'You have selected the book of {auteur}', xaxis_title='Number of pages', yaxis_title= 'Book title' )
    return fig


# Exécution de l'application
if __name__ == '__main__':
    app.run_server(debug=True)
