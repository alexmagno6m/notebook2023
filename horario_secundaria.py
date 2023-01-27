
import pandas as pd
from dash import Dash, dash_table, html, dcc, Input, Output, callback
import urllib.request
import ssl



ssl._create_default_https_context = ssl._create_unverified_context
r = urllib.request.urlopen('https://raw.githubusercontent.com/alexmagno6m/render/main/BD_SECUNDARIA_2023_CSV.csv')
df = pd.read_csv(r, sep=';')
df = df[['PROFESOR_O_CURSOS', 'DIA', '1', '2', '3', '4', '5', '6']]
app = Dash(__name__)
server = app.server
app.layout = html.Div([
    html.H2('Horario General Secundaria'),
    html.H2('Colegio Antonio Baraya IED'),
html.Div([
    "Listado de profesores inicia despues del listado de cursos",
  dcc.Dropdown([x for x in sorted(df.PROFESOR_O_CURSOS.unique())],
               id='professor_drop',
               placeholder="Seleccione/escriba un curso o profesor")
],
            style={'width':'35%'}
),
html.Div([
    "O tambien puede escoger Dia_c (curso) o Dia_p (profesor):",
    dcc.Dropdown([x for x in (df.DIA.unique())],
    id = 'dia_drop',
    placeholder="Seleccionar Dia")
],
  style={'width':'30%'}
),

    dash_table.DataTable(
        data=df.to_dict('records'),
        page_size=18,
        columns=[{'name': i, 'id': i} for i in df.columns],
        style_data_conditional=(
            [
                {
                    'if': {
                        'filter_query': '{{{}}} is blank'.format(col),
                        'column_id': col
                    },
                    'backgroundColor': 'gray',
                    'color': 'white'
                } for col in df.columns
            ]
            +
            [
                {
                   'if' : {
                        'filter_query': '{{{}}} contains "TP"'.format(col),
                        'column_id': col
                   },
                    'backgroundColor': '#b8e0d2',
                    'color': 'black'
                } for col in df.columns
            ]
        ),
        style_cell_conditional = [
            {'if': {'column_id': 'PROFESOR_O_CURSOS'},
             'width': '15%'},
            {'if': {'column_id': 'DIA'},
             'width': '10%'},

],
        id='my_table'


    ),
])

@callback(
Output('my_table', 'data'),
Input('professor_drop', 'value'),
Input('dia_drop', 'value')
)
def update_dropdown(proff_v, day_v):
    dff = df.copy()
    if proff_v:
        dff = dff[dff.PROFESOR_O_CURSOS == proff_v]

    if day_v:
        dff = dff[dff.DIA == day_v]
    return dff.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=False)
