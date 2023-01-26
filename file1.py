
import pandas as pd
from dash import Dash, dash_table, html, dcc
import urllib.request
import ssl



ssl._create_default_https_context = ssl._create_unverified_context
r = urllib.request.urlopen('https://raw.githubusercontent.com/alexmagno6m/render/main/BD_SECUNDARIA_2023_CSV.csv')
df = pd.read_csv(r, sep=';')

app = Dash(__name__)
app.layout = html.Div([
    dash_table.DataTable(
        data=df.to_dict('records'),
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

if __name__ == '__main__':
    app.run_server(debug=True)
