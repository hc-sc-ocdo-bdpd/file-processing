from dash import Dash, DiskcacheManager, CeleryManager, Input, Output, html, callback, dcc, State 
import os
import datetime
from Table_processor_main import process_content
from pathlib import Path
import logging
import base64
import webbrowser
from threading import Timer
import time

def register_long_callbacks(app, background_callback_manager):
    @app.callback(Output('output-result', 'children'),
              Input('upload-file', 'contents'),
              State('upload-file', 'filename'),
              State('upload-file', 'last_modified'),
              background = True,
              manager = background_callback_manager)
    
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