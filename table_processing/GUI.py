from dash import Dash, dcc, html, Input, Output, callback

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.I("Try typing in input 1 & 2, and observe how debounce is impacting the callbacks. Press Enter and/or Tab key in Input 2 to cancel the delay"),
        html.Br(),
        dcc.Input(id="input1", type="text", placeholder="", style={'marginRight':'10px'}),
        dcc.Input(id="input2", type="text", placeholder="", debounce=True),
        html.Div(id="output"),
    ]
)


@callback(
    Output("output", "children"),
    Input("input1", "value"),
    Input("input2", "value"),
)
def update_output(input1, input2):
    return f'Input 1 {input1} and Input 2 {input2}'


if __name__ == "__main__":
    app.run(debug=True)
