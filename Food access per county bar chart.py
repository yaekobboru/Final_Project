import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import dash_table 
from dash.dependencies import Input, Output
from config import password
import plotly.graph_objs as go
from sqlalchemy import create_engine
import pandas.io.sql as psql

app = dash.Dash(__name__)
#-----------------------------------------------------------------------------------------

# connection string
DATABASE_URI = f'postgresql://postgres:{password}@localhost:5432/FoodAccess'
# create engine 
db = create_engine(DATABASE_URI)
# Connect to PostgreSQL server
dbConnection = db.connect()
df = psql.read_sql('SELECT sc.state, sc.county, fam.urban, fam.pop2010, fam.ohu2010, fam.povertyrate,\
                           fam.medianfamilyincome, fam.tractlowi, fam.la1and10 as low_access \
                    FROM food_access_main fam LEFT JOIN state_county sc ON fam.statecountyid = sc.statecountyid ', dbConnection);

#-------------------------------------------------------------------------------------------

application = app.server
app.layout = html.Div([
# dropdown = html.Div([
html.Div([
    html.Div([    
        html.Div([   
                html.H1("Food Access across the states", style={'text-align': 'center'})
                ])
                 ], className='six column', id = 'title')
                       ], id = 'header', className='row flex-display', style={'margin-botttom': '25px'}),
html.Div([               
html.Div([ 
    html.P('State:'),
             dcc.Dropdown(id='dropdown_s'
                        , searchable= True
                        , options=[{'label': i, 'value': i} for i in df["state"].unique()]
                        , value='Alabama')
                        # , html.Br()
                    ,html.P('County:'),
             dcc.Dropdown(id='dropdown_c'
                        , searchable= True
                        , options=[]
                        , value='Jackson County'
                        
                        ),
                        # , html.Br()]) 
                        # , style={'width': '15%'})
                        
html.Br()], style={'width': '15%'}, className='three columns'),                          
html.Div( [

html.Div([dcc.Graph(id = 'bar_chart' 
, style={
            'height': 500,
            'width':700,
            "display": "block",
            "margin-left": "auto",
            "margin-right": "auto",
            }

 )], 
className='three columns')


 ], className='row flex-display')

,], className='row flex-display')], id = 'mainContainer', style={'display': 'flex', 'flex-direction': 'column'})


@app.callback(Output('dropdown_c', 'options'),
              [Input('dropdown_s','value')])


def update_country(dropdown_s):
    terr3 = df[df['state'] == dropdown_s]
    return [{'label': i, 'value': i} for i in terr3['county'].unique()]

@app.callback(Output('dropdown_c', 'value'),
              [Input('dropdown_c', 'options')])

def update_country(dropdown_c):
    return [k['value'] for k in dropdown_c][0]


@app.callback(Output('bar_chart', 'figure'),
              [Input('dropdown_s','value')],
              [Input('dropdown_c','value')])
def update_graph(dropdown_s, dropdown_c):
    terr5 = df.groupby(['state', 'county', 'urban','low_access']).agg(counts=('low_access','count')).reset_index()
    terr6 = terr5[(terr5['state'] == dropdown_s) &
                 (terr5['county'] == dropdown_c) ]

    return {
        'data': [
            go.Bar(

                x=terr6[terr6['low_access']==1].urban.unique(),
                y=terr6[terr6['low_access']==1].counts,
                text = terr6[terr6['low_access']==1].counts,
                texttemplate='%{text:,.0f}',
                textposition='auto',
                name='Low Access',
                marker=dict(color='#9C0C38'),
                hoverinfo='text',
                hovertext=
                '<b>Region</b>: ' + terr6['state'].astype(str) + '<br>' +
                '<b>County</b>: ' + terr6['county'].astype(str) + '<br>' 
             
            ),
            go.Bar(
                x=terr6[terr6['low_access']==0].urban.unique(),
                y=terr6[terr6['low_access']==0].counts,
                text=terr6[terr6['low_access']==0].counts,
                texttemplate='%{text:,.0f}',
                textposition='auto',
                name='Access',
                marker=dict(color='orange'),
                hoverinfo='text',
                hovertext=
                '<b>Region</b>: ' + terr6['state'].astype(str) + '<br>' +
                '<b>Country</b>: ' + terr6['county'].astype(str) + '<br>' 
        
            )
        ],


        'layout': go.Layout(
            barmode = 'stack',
            title={'text': 'Food access count: ' + (dropdown_c) + ' ' + '<br>'
                  ,
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'black',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='black',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#eeedee',
            plot_bgcolor='#aad4e6',
            legend={'orientation': 'h',
                    'bgcolor': 'white',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(r=0),
            xaxis=dict(title='<b>Urban</b>',
                       tick0 = 'Rural',
                       dtick = 'Urban',
                       color = 'black',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='grey',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='black',
                           size=12
                       )),
            yaxis=dict(title='<b>counts of records for access</b>',
                       color='black',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='black',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='black',
                           size=12
                       )
                       )


        )
    }



    
#--------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)