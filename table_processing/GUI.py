from dash import Dash, dcc, html, Input, Output, callback
from Table_processor_main import process_pdf
from pathlib import Path

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.I("To extract tables from a file, please type in the file name and press Enter"),
        html.Br(),
        dcc.Input(id="filename", type="text", placeholder="", debounce=True),
        html.Div(id="output"),
    ]
)


@callback(
    Output("output", "children"),
    Input("filename", "value"),
)
def call_processing_fn(filename:str):
    path = Path(filename)
    if path.exists() and path.suffix == ".pdf":
        output_file = process_pdf(filename)
        return f'Processing completed.  Extracted tables can be found in {output_file}'
    else:
        return f''



if __name__ == "__main__":
    app.run(debug=True)