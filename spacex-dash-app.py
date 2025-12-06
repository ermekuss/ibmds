# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# список launch sites из данных
launch_sites = spacex_df['Launch Site'].unique().tolist()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center',
                   'color': '#503D36',
                   'font-size': 40}),
    # ===== TASK 1: dropdown =====
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': site, 'value': site} for site in launch_sites],
        value='ALL',  # значение по умолчанию
        placeholder='Select a Launch Site here',
        searchable=True
    ),
    html.Br(),

    # ===== TASK 2: pie chart =====
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # ===== TASK 3: payload slider =====
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        value=[min_payload, max_payload],
        marks={
            int(min_payload): str(int(min_payload)),
            int(max_payload): str(int(max_payload))
        },
    ),
    html.Br(),

    # ===== TASK 4: scatter chart =====
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# ===== TASK 2 =====
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie(selected_site):
    if selected_site == 'ALL':
        
        df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(
            df,
            names='Launch Site',
            title='Total Successful Launches by Site'
        )
    else:
        
        df = spacex_df[spacex_df['Launch Site'] == selected_site]
        counts = df['class'].value_counts().reset_index()
        counts.columns = ['class', 'count']
        fig = px.pie(
            counts,
            names='class',
            values='count',
            title=f'Total Launch Outcomes for site {selected_site}'
        )
    return fig

# ===== TASK 4 =====
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter(selected_site, payload_range):
    low, high = payload_range

    df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if selected_site != 'ALL':
        df = df[df['Launch Site'] == selected_site]

    fig = px.scatter(
        df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Correlation between Payload and Success{}'.format(
            '' if selected_site == 'ALL' else f' for site {selected_site}'
        )
    )
    return fig


    # Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8051, debug=False)