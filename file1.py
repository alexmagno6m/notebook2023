
import pandas as pd
from dash import Dash, dash_table
import urllib.request
import ssl


ssl._create_default_https_context = ssl._create_unverified_context
r = urllib.request.urlopen('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
df = pd.read_csv(r)
app = Dash(__name__)
app.layout = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])

if __name__ == '__main__':
    app.run_server(debug=True)
