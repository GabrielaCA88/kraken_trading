import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from miner import Tradedata
from datetime import date,datetime
from dash.dependencies import Input, Output
import time


app = dash.Dash (__name__,meta_tags=[{"name": "viewport", "content": "width=device-width"}], external_stylesheets=['assets/bootstrap.css'])
server= app.server

app.title = "UNAV Web Trader"

app.layout = dbc.Container ([
    html.H1('UNAV Exchange'),
    html.Div(
        className="three columns div-left-panel",
        children=[
            # Div for Left Panel App Info
            html.Div(
                className="div-info",
                children=[
                    html.A(
                        html.Img(
                            className="logo",
                            src='/assets/unavlogo.png', style={'height':'5%', 'width':'5%'},
                    ),
                        href="https://www.unav.edu/",
                    ),
                    dcc.Markdown(
                        """
                        Please select: 1. a pair of currencies, 2. origin date and 3. data interval.    
                        This is a beta development. Please invest at your risk. [Source Code](https://github.com/GabrielaCA88) |
                        """
                    ),
                ],
            )]),
    dcc.Dropdown(
            id='pair_chosen',
            options=[
                {'label': 'Bitcoin - USD', 'value': 'BTCUSD'},
                {'label': 'Ether - USD', 'value': 'ETHUSD'},
                {'label': 'ADA-USD', 'value': 'ADAUSD'}],
            value='BTCUSD',
            style={'width': '40%'}
        ),
    dcc.DatePickerSingle(
            id='since_when',
            min_date_allowed=date(2020, 8, 5),
            initial_visible_month=date(2021, 12, 10),
            date=date(2020, 12, 10)
        ),
    html.Div(
        [
            dbc.Label("Choose one"),
            dbc.RadioItems(
                options=[
                {'label': 'Minuto', 'value': 1},
                {'label': 'Diario', 'value': 1440},
                {'label': 'Semanal', 'value': 10080}],
                value=1440,
                id="interval_chosen",
                inline=True,
            ),
        ]
    ),
    html.Br(),
    dcc.Graph(
        id='example-graph', figure={}),
html.Div(
    [
        dbc.Button("Crypto News", size="lg", color="primary", href='https://cryptopanic.com/'),
        dbc.Button("Coin360", size="lg", color="success", href='https://coin360.com/'),
        dbc.Button("Coin market Cap", size="lg", color="info", href='https://coinmarketcap.com/'),
    ])
])

@app.callback(
    Output(component_id='example-graph', component_property= 'figure'),
    [Input(component_id='pair_chosen', component_property= 'value'),
    Input(component_id='since_when', component_property='date'),
    Input(component_id='interval_chosen', component_property= 'value')])

def update_my_graph (pair_chosen, since_when, interval_chosen):

    d = datetime.strptime(since_when, '%Y-%m-%d')
    since = time.mktime(d.timetuple())

    d = Tradedata(pair=pair_chosen, since=since, interval=interval_chosen)
    df = d.get_data()

    fig = go.Figure()
    # declare subplots
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            vertical_spacing=0.01,
                            row_heights=[0.5, 0.1])

    fig.add_trace(go.Candlestick(x=df.index,
                                    open=df[('open')],
                                    high=df[('high')],
                                    low=df[('low')],
                                    close=df[('close')],
                                    showlegend=False))
    # set up the vwap line
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['vwap'],
        mode='lines',
        name='vwap',
        line=dict(color='royalblue', width=2),
        showlegend=False
    ))

    # include a volume bar
    colors = ['green' if row['open'] - row['close'] >= 0
            else 'red' for index, row in df.iterrows()]
    fig.add_trace(go.Bar(x=df.index,
                            y=df['volume'],
                            marker_color=colors,
                            showlegend=False
                            ), row=2, col=1)

    # remove rangeslider
    fig.update_layout(xaxis_rangeslider_visible=False, transition_duration=500)

    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)