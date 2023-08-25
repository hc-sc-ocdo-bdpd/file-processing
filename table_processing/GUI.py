from dash import Dash, DiskcacheManager, CeleryManager, Input, Output, html, callback, dcc, State 
import diskcache
import os
import datetime
from Table_processor_main import process_content
from long_callbacks import register_long_callbacks

from pathlib import Path
import logging
import base64
import webbrowser
from threading import Timer
import time

port = 8050


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

app = Dash(__name__, external_stylesheets=external_stylesheets, background_callback_manager=background_callback_manager)

app.layout = html.Div([
    dcc.Upload(
        id='upload-file',
        children=html.Div([
            'Drag and Drop a PDF file or ',
            html.A('Select PDF Files'),
            html.Br(),
            'Note: Processing takes a while. Details for where to find the output will appear when finished.'
        ]),
        style={
            'width': '60%',
            'height': '120px',
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
register_long_callbacks(app)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=False, use_reloader=False)

    # app.run(debug=True)
    