import pandas as pd
import plotly.graph_objects as go
import numpy as np
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
server = app.server

imf = pd.read_csv('imf_clean.csv')
imf = imf.set_index('Date')
imf = imf.drop('Euro (EUR)', axis = 1)
imf = imf.fillna(0)

cia = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')

countries = ['Australia', 'Botswana', 'Brazil', 'Brunei', 'Canada', 'Chile', 'China', 'Colombia',
             'Denmark', 'India', 'Japan', 'Korea, South', 'Kuwait', 'Malaysia', 'New Zealand', 
             'Norway', 'Oman', 'Poland', 'Qatar', 'Saudi Arabia', 'Singapore', 'South Africa',
             'Sweden', 'Switzerland', 'Thailand', 'Trinidad and Tobago', 'United Arab Emirates', 'United Kingdom',
             'United States']

codes = cia[cia['COUNTRY'].isin(countries)]['CODE'].to_list()



df = pd.read_csv('clean_combined_data.csv')
df = df.drop_duplicates(subset=None, keep='first', inplace=False)
df = df.set_index(['Country Name', 'Series Name']).transpose()
countries = ['China', 'India', 'Brazil', 'Russian Federation', 'Japan', 
             'Mexico', 'Spain', 'Saudi Arabia', 'Poland', 'Canada']
metric_list = ['Population growth (annual %)', 'GDP growth (annual %)', 
               'Inflation, consumer prices (annual %)', 
               'Exports of goods and services (% of GDP)', 
               'Imports of goods and services (% of GDP)']


def make_video():
    years = df.index.to_list()[1:]
    fig_dict = {
    "data": [],
    "layout": {},
    "frames": []}

    fig_dict["layout"]["xaxis"] = {"range": [-20, 100], "title": "Inflation Rate"}
    fig_dict["layout"]["yaxis"] = {"range": [-20, 25], "title": "GDP Growth Rate"}
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["sliders"] = {
        "args": [
            "transition", {
                "duration": 500,
                "easing": "cubic-in-out"
            }
        ],
        "initialValue": "1995",
        "plotlycommand": "animate",
        "values": years,
        "visible": True
    }
    fig_dict["layout"]["updatemenus"] = [
        {"buttons": [
                {"args": [None, {"frame": {"duration": 700, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 600,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "Play",
                "method": "animate"
                },
                {"args": [[None], {"frame": {"duration": 0, "redraw": False},
                                "mode": "immediate",
                                "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
                }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
        }]

    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Year:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 450, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []}

    year = '1995'
    for country in countries:
        data_dict = {
            "x": pd.Series(df.loc[year, country]['Inflation, consumer prices (annual %)']),
            "y": pd.Series(df.loc[year, country]['GDP growth (annual %)']),
            "mode": "markers",
            "text": country,
            "marker": {
                "sizemode": "area",
                "sizeref": 200000,
                "size": 17, #int(df.loc[year, country]['Exchange Rate']),
                "opacity": 0.65
            },
            "name": country
        }
        fig_dict["data"].append(data_dict)
    # make frames
    for year in years:
        frame = {"data": [], "name": str(year)}
        for country in countries:

            data_dict = {
                "x": pd.Series(df.loc[year, country]['Inflation, consumer prices (annual %)']),
                "y": pd.Series(df.loc[year, country]['GDP growth (annual %)']),
                "mode": "markers",
                "text": country,
                "marker": {
                    "sizemode": "area",
                    "sizeref": 200000,
                    "size": 17, #int(df.loc[year, country]['Exchange Rate']),
                    "opacity": 0.65
                },
                "name": country
            }
            frame["data"].append(data_dict)

        fig_dict["frames"].append(frame)
        slider_step = {"args": [[year],
            {"frame": {"duration": 600, "redraw": False},
            "mode": "immediate",
            "transition": {"duration": 300}}],
            "label": year,
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)


    fig_dict["layout"]["sliders"] = [sliders_dict]
    return fig_dict


app.layout = html.Div([dbc.Container([

dbc.Row([
    dbc.Col([html.H1('Global Financial Dashboard'), html.H6('Exploring global exchange rates and other financial metrics')], md=12)
]),

html.Br(),
html.Br(),



dbc.Row([
    dbc.Col(
        dcc.Markdown("""The following visualizations were generated by Hunter Kuffel, Peter Nincich and Jeremy Moskowitz 
        as part of project during the Columbia Engineering Data Analytics Bootcamp. The data used comes from two sources: 
        the International Monetary Fund (IMF) and WorldBank. For a more detailed breakdown of the data cleaning and visualization
        proces, feel free to check out the [Gitlab repository](https://columbia.bootcampcontent.com/hunter.kuffel/project-1/blob/master/data-cleaning.ipynb)."""),
    md=12)
]),



html.Br(),
html.Br(),

dbc.Row(
    [dbc.Col(
        [html.H2('GDP Growth vs. Inflation Rate 1995-2016')], md=4),
    dbc.Col([
        dcc.Graph(
            id='video',
            figure=make_video()
        )
], md=8)]
),

html.Br(),
html.Br(),
html.Br(),

dbc.Row([
    dbc.Col([html.H2('Key Metrics 1995-2016'),
    html.Label('Select a Metric'),
    dcc.Dropdown(
    id='metric-dropdown',
    options=[{'label': str(m), 'value': str(m)} for m in metric_list],
    value='Population growth (annual %)')], md=4),
    dbc.Col([dcc.Graph(id='metric-lines')], md=8)
]),

html.Br(),
html.Br(),
html.Br(),

dbc.Row([
    dbc.Col([html.H2('Exchange Rate Chloropleth'),
    html.Label('Select a Date'),
    dcc.Dropdown(
    id='date-dropdown',
    options=[{'label': str(date), 'value': str(date)} for date in imf.index.to_list()],
    value='3-Jan-1994')], md=4),
    dbc.Col([dcc.Graph(id='chloropleth')], md=8)
])])])


@app.callback(
    Output('metric-lines', 'figure'),
    [Input('metric-dropdown', 'value')]
)
def update_lines(metric):
    traces = []
    x = np.arange(1996,2019,1)
    for country in countries:
        traces.append(go.Scatter(x=x, y=df[country][metric][2:], mode = "lines", name = country))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Time'},
            yaxis={'title': f'{metric}'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1, 'orientation': 'h'},
            hovermode='closest'
        )
    }

@app.callback(
    Output('chloropleth', 'figure'), 
    [Input('date-dropdown', 'value')]
)
def update_chloro(date):
    return {
        'data': [go.Choropleth(locations = codes, z = list(imf.loc[date]), colorscale = 'Greens', autocolorscale=False, reversescale=True,
        marker_line_color='white', marker_line_width=0.5, colorbar_title = 'Exchange Rate')],
        'layout': go.Layout(
            title = f'Exchange Rate Relative to USD, {date}'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)