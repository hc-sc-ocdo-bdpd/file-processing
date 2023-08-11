from dash import Dash, DiskcacheManager, CeleryManager, Input, Output, html, callback, dcc, State 

import datetime
from Table_processor_main import process_content
from pathlib import Path
import logging
import base64


logging.basicConfig(filename='table_detection_gui.log', filemode='a', datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s\n')

if 'REDIS_URL' in os.environ:
    # Use Redis & Celery if REDIS_URL set as an env variable
    from celery import Celery
    celery_app = Celery(__name__, broker=os.environ['REDIS_URL'], backend=os.environ['REDIS_URL'])
    background_callback_manager = CeleryManager(celery_app)

else:
    # Diskcache for non-production apps when developing locally
    import diskcache
    cache = diskcache.Cache("./cache")
    background_callback_manager = DiskcacheManager(cache)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-file',
        children=html.Div([
            'Drag and Drop a PDF file or ',
            html.A('Select PDF Files')
        ]),
        style={
            'width': '60%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        
        multiple=False  # Don't allow multiple files to be uploaded - need to handle naming the output files
    ),
    html.Div(id='output-result'),
])


def parse_contents(contents, filename, date):
    logging.info("Processing " + str(filename))
    logging.info("Contents type: " + str(type(contents)))
    content_type, content_string = contents.split(',')
    contents = base64.b64decode(content_string)
    logging.info("Contents type: " + str(type(contents)))

    try:
        output_filename = process_content(contents)
    except Exception as e:
        logging.error("Error occured: " + str(e))
        return html.Div([
            html.H5("Input filename: " + str(filename)),
            html.H5("Error Occured: " + str(e)),
            html.H6(datetime.datetime.fromtimestamp(date))
        ])

    output_filename = Path(output_filename)
    logging.info("Output file: " + str(output_filename.absolute()))
    logging.info("Processing complete. Updating GUI.")
    return html.Div([
        html.H5("Input filename: " + str(filename)),
        html.H5("Output filename: " + str(output_filename.absolute())),
        html.H6(datetime.datetime.fromtimestamp(date))
    ])


@callback(Output('output-result', 'children'),
              Input('upload-file', 'contents'),
              State('upload-file', 'filename'),
              State('upload-file', 'last_modified'),
              background = True,
              manager = background_callback_manager)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if isinstance(list_of_contents, list):
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children
    else:
        if list_of_contents is not None:
            children = [parse_contents(list_of_contents, list_of_names, list_of_dates)]
            return children

if __name__ == '__main__':
    app.run(debug=True)
