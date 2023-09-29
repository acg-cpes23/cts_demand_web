from dash import Dash, html, dcc, callback, Output, Input,dash_table
import plotly.express as px
import pandas as pd
#
url = 'https://raw.githubusercontent.com/acg-cpes23/dash-app-deploy/main/demand.csv'
demand_df2 = pd.read_csv(url,index_col = 0)

demand_df2_aux = {}
#---------
demand_df2_aux = demand_df2.copy()
demand_df2_aux['Date'] = list(demand_df2.index)
#-
columnsTitles = [ demand_df2_aux.columns[-1]]+[demand_df2_aux.columns[x] for x in range(0, len(demand_df2_aux.columns)-1) ]
demand_df2_aux = demand_df2_aux.reindex(columns=columnsTitles)
#----------
#
app = Dash(__name__)
server = app.server
#
app.layout = html.Div([
    html.H1(children='Hourly Demand', style={'textAlign':'center'}),
    #---------
    html.Hr(),
    html.H2(children='Temporal Series', style={'textAlign':'center'}),
    html.H5(children='Select the asset type'),
    dcc.Dropdown(['OPS', 'Cranes', 'Reefers', 'Total'], value = 'Total',  id='dropdown-asset-selection'),
    dcc.Graph(id='graph-asset-content'),
    #---------
    html.Hr(),
    html.H2(children='Hourly Data', style={'textAlign':'center'}),
    dash_table.DataTable(demand_df2_aux.to_dict('records'), [{"name": i, "id": i} for i in demand_df2_aux.columns], page_size=6),
    html.Hr(),
    html.H5(children='Select the date'),
    dcc.Dropdown(demand_df2.index  ,  id='dropdown-date-selection'),
    dcc.Graph(id='graph-date-content')
    
        
])

@callback(
    Output('graph-asset-content', 'figure'),
    Input('dropdown-asset-selection', 'value')
)
def update_graph(value):
    #
    if value == 'OPS':
        fig = px.line( demand_df2['Demand_Vessel'],\
                     labels = dict(x = 'Date', y = 'Power [kW]')
                    )
    if value == 'Cranes':
        fig = px.line( demand_df2['Demand_Cranes'],\
                     labels = dict(x = 'Date', y = 'Power [kW]')
                    )
    if value == 'Reefers':
        fig = px.line( demand_df2['Demand_Reefers'],\
                     labels = dict(x = 'Date', y = 'Power [kW]')
                    )
    if value == 'Total':
        fig = px.line(demand_df2,y=demand_df2.columns,\
                     labels = dict(x = 'Date', y = 'Power [kW]')
                    )
    return fig

@callback(
    Output('graph-date-content', 'figure'),
    Input('dropdown-date-selection', 'value')
)
def update_graph(value):
    dff = demand_df2.loc[value]
    fig = px.scatter( x = ['OPS','Cranes','Reefers','Total'], y= [dff['Demand_Vessel'],dff['Demand_Cranes'],\
                                       dff['Demand_Reefers'],dff['Demand_Total']],\
                     labels = dict(x = 'Assets', y = 'Power [kW]')
                    )
    return fig








if __name__ == '__main__':
    app.run(debug=False)
