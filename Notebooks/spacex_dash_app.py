# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("../Data/spacex_launch_dash.csv")
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
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div([
                                    dcc.Dropdown(id='site-dropdown',
                                                 options=[
                                                        {'label': 'All Sites', 'value': 'OPT1'},
                                                        {'label': 'CCAFS LC-40', 'value': 'OPT2'},
                                                        {'label': 'KSC LC-39A', 'value': 'OPT3'},
                                                        {'label': 'VAFB SLC-4E', 'value': 'OPT4'},
                                                        {'label': 'CCAFS SLC-40', 'value': 'OPT5'},
                                                 ],
                                                 placeholder='Select Launch Site',
                                                 searchable=True,
                                                 style={'width':'80%', 'padding':'3px', 'font-size':'20px',
                                                           'text-align-last':'center'})
                                
                                ]),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                        ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'OPT1':
        fig = px.pie(filtered_df,
                    values='class',
                    names='Launch Site',
                    title='Total success launches by Site')

    elif entered_site == 'OPT2':
        fig = px.pie(filtered_df[filtered_df['Launch Site']=='CCAFS LC-40'],
                    names='class',
                    title='Total success launches of CCAFS LC-40')
        
    elif entered_site == 'OPT3':
        fig = px.pie(filtered_df[filtered_df['Launch Site']=='KSC LC-39A'],
                    names='class',
                    title='Total success launches of KSC LC-39A')
        
    elif entered_site == 'OPT4':
        fig = px.pie(filtered_df[filtered_df['Launch Site']=='VAFB SLC-4E'],
                    names='class',
                    title='Total success launches of VAFB SLC-4E')
    elif entered_site == 'OPT5':
        fig = px.pie(filtered_df[filtered_df['Launch Site']=='CCAFS SLC-40'],
                    names='class',
                    title='Total success launches of CCAFS SLC-40')
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')])
def get_scatter_plot(entered_site, slider_range):
    filtered_df = spacex_df
    low, high = slider_range
    mask = (filtered_df["Payload Mass (kg)"] > low) & (filtered_df["Payload Mass (kg)"] < high)
    
    if entered_site == 'OPT1':
        fig = px.scatter(filtered_df[mask],
                        x="Payload Mass (kg)", y="class", color="Booster Version Category", size="Payload Mass (kg)")
        
    elif entered_site == 'OPT2':
        fig = px.scatter(filtered_df[filtered_df['Launch Site']=='CCAFS LC-40'][mask],
                        x="Payload Mass (kg)", y="class", color="Booster Version Category", size="Payload Mass (kg)")
        
    elif entered_site == 'OPT3':
        fig = px.scatter(filtered_df[filtered_df['Launch Site']=='KSC LC-39A'][mask],
                        x="Payload Mass (kg)", y="class", color="Booster Version Category", size="Payload Mass (kg)")  
        
    elif entered_site == 'OPT4':
        fig = px.scatter(filtered_df[filtered_df['Launch Site']=='VAFB SLC-4E'][mask],
                        x="Payload Mass (kg)", y="class", color="Booster Version Category", size="Payload Mass (kg)") 
        
    elif entered_site == 'OPT5':
        fig = px.scatter(filtered_df[filtered_df['Launch Site']=='CCAFS SLC-40'][mask],
                        x="Payload Mass (kg)", y="class", color="Booster Version Category", size="Payload Mass (kg)")  
    return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
