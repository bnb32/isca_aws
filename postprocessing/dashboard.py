import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import time
import sys
sys.path.insert(0,'../')
import environment

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)


animation_directory = os.path.join(os.environ.get('ISCA_REPO_DIR'),'postprocessing/anims/')

files = [f for f in os.listdir(animation_directory)]

app.layout = html.Div([
    html.Div(
        [html.H2('Choose Animation:',style={'textAlign':'center'})]
    ),
    dcc.Dropdown(id='filename',
                 options=[
                     {'label': i, 'value': i} for i in files
                 ],
                 multi=False,
                 placeholder='Select an animation',
                 style={'width':'100%','font-size':'20px','align-items':'center','justify-content':'center'}
                 ),
    html.Div([
        html.Div([],id='animation'),
    ], style={'textAlign':'center'})
    
])


@app.callback(
    [dash.dependencies.Output(component_id='animation',component_property='children')],
    [dash.dependencies.Input(component_id='filename', component_property='value')],
    [dash.dependencies.State('animation','children')])

def update_output(filename,children):
    
    path = f'{animation_directory}/{filename}'
    while filename == None:
        time.sleep(0.1)
    
    return [html.Video(src=path, controls=True)]

@server.route(f'{animation_directory}/<path:path>')
def serve_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(os.path.join(root_dir, 'anims'), path)

app.run_server(debug=False, use_reloader=False,port=8050)
#app.run_server(debug=True, host='localhost', port=8050, use_reloader=False)
