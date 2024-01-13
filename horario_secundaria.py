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
''' For input field
                     id='professor_drop',
                     type="text",
                     autoComplete=False,
                     placeholder="Seleccione un curso o profesor"
'''
app.layout = html.Div([
    html.H2('Horario General Secundaria'),
    html.H2('Colegio Antonio Baraya IED'),
    html.Div([
        "Consulte el horario individual "
        "por curso o profesor",
        dcc.Dropdown([x for x in sorted(df.PROFESOR_O_CURSOS.unique())],
                     id='professor_drop',
                     searchable=False,
                     placeholder="Seleccione un curso o profesor")
    ],
        style={'width': '40%'}
    ),
    html.Div([
        "o puede Consultar el horario global por dias, seleccione: "
        "Dia_p (profesor) o Dia_c (curso):",
        dcc.Dropdown([x for x in (df.DIA.unique())],
                     id='dia_drop',
                     searchable=False,
                     placeholder="Seleccionar Dia")
    ],
        style={'width': '40%'}
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
                        'if': {
                            'filter_query': '{{{}}} contains "TP"'.format(col),
                            'column_id': col
                        },
                        'backgroundColor': '#b8e0d2',
                        'color': 'black'
                    } for col in df.columns
                ]
                +
                [
                    {
                        'if': {
                            'filter_query': '{{{}}} = "RA"'.format(col),
                            'column_id': col
                        },
                        'backgroundColor': '#c1fba4',
                        'color': 'black'
                    } for col in df.columns
                ]
                +
                [
                    {
                        'if': {
                            'filter_query': '{{{}}} = "RC"'.format(col),
                            'column_id': col
                        },
                        'backgroundColor': '#c1fba4',
                        'color': 'black'
                    } for col in df.columns
                ]
        ),
        style_cell_conditional=[
            {'if': {'column_id': 'PROFESOR_O_CURSOS'},
             'width': '15%'},
            {'if': {'column_id': 'DIA'},
             'width': '10%'},

        ],
        id='my_table'

    ),
    html.Div([
        html.H3('Powered by BitSmart | Alexander Acevedo')
    ])

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
        return dff.to_dict('records')
    if day_v:
        dff = dff[dff.DIA == day_v]
        return dff.to_dict('records')


# un solo return al mismo nivel del if muestra toda la tabla
if __name__ == '__main__':
    app.run_server(debug=False)
