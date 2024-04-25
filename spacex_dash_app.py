# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                        dcc.Dropdown(id='site-dropdown',options=[
                                            {'label': 'All Sites', 'value': 'ALL'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                            ],
                                        value='ALL',
                                        placeholder="Select a Site",
                                        searchable=True
                                        ),
                                        html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                        html.Div(dcc.Graph(id='success-pie-chart')),
                                        html.Br(),

                                        html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                        dcc.RangeSlider(id='payload-slider',
                                                        min=0, max=10000, step=1000,
                                                        marks={0: '0',
                                                                100: '100'},
                                                        value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                        html.Br(),
                                        ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        data1 = spacex_df.groupby('Launch Site')['class'].count().reset_index()
        data1.columns = ['Launch Site', 'Count']
        fig = px.pie(data1, values='Count', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:
        new_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        data2 = new_df.groupby('class').count()['Launch Site'].reset_index()
        
        fig = px.pie(data2, values= 'Launch Site', 
        names='Launch Site', 
        title='Total Success Launches for Site '+ entered_site)
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart (entered_site,entered_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= entered_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= entered_range[1])]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df,y="class", x="Payload Mass (kg)", color="Booster Version Category",
        title='Correlation Between Payload And Success For All Sites',
        labels={
            "Payload Mass (kg)": "Payload Mass (kg)", 
            "class": "Launch Outcome (Success/Failure)"})
        return fig

    else:
        new_df2 = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(new_df2,y="class", x="Payload Mass (kg)", color="Booster Version Category",
        title='Correlation Between Payload And Success For Site' + entered_site,
        labels={
            "Payload Mass (kg)": "Payload Mass (kg)", 
            "class": "Launch Outcome (Success/Failure)"})
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
