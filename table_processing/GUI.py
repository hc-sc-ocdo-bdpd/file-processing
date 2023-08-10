from dash import Dash, dcc, html, Input, Output, State, callback

import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-image-upload'),
])

def parse_contents(contents, filename, date):
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents),
        html.Hr()#,
#        html.Div('Raw Content'),
#        html.Pre(contents[0:200] + '...', style={
#            'whiteSpace': 'pre-wrap',
#            'wordBreak': 'break-all'
#        })
    ])

@callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

if __name__ == '__main__':
    app.run(debug=True)



'''
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
def call_processing_fn(filename):
    if type("asdf") == type(filename):
        path = Path(filename)
        if path.exists() and path.suffix == ".pdf":
            output_file = process_pdf(filename)
            return f'Processing completed.  Extracted tables can be found in {output_file}'
        else:
            return f''
    else:
        return f''


if __name__ == "__main__":
    app.run(debug=True)
'''
