
import pandas as pd
from dash import Dash, dash_table, html, dcc, Input, Output, callback
import urllib.request
import ssl



ssl._create_default_https_context = ssl._create_unverified_context
r = urllib.request.urlopen('https://raw.githubusercontent.com/alexmagno6m/render/main/BD_SECUNDARIA_2023_CSV.csv')
df = pd.read_csv(r, sep=';')
df = df[['PROFESOR_O_CURSOS', 'DIA', '1', '2', '3', '4', '5', '6']]
app = Dash(__name__)
app.layout = html.Div([
html.Div([
  professor_drop := dcc.Dropdown([x for x in sorted(df.PROFESOR_O_CURSOS.unique())])
]),
    my_table := dash_table.DataTable(
        data=df.to_dict('records'),
        filter_action='native',
        page_size=10,
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
        )
    ),
])

@callback(
Output(my_table, 'data'),
Input(professor_drop, 'value'),
)
def update_dropdown(proff_v):
    dff = df.copy()
    if proff_v:
        dff = dff[dff.PROFESOR_O_CURSOS==proff_v]
        return dff.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
