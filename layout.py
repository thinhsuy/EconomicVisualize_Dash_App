from preprocessing import *

def getLayout(app):
    app.layout = html.Div(
        [
            html.H1("Countries Economic in Glance", style={"textAlign":"center"}),
            html.Div(
                [
                    html.Div("Country: ", style={"textAlign":"center"}),
                    dcc.Dropdown(
                        id="country_dropdown",
                        multi=True,
                        style={"display": "block", "margin-left": "auto",
                                "margin-right": "auto", "width": "300px"},
                        options= country_list,
                        value=['Vietnam'] # Value as default
                    ),
                    html.Br(),
                    html.Div("Feature to compare: ", style={"textAlign":"center"}),
                    dcc.Dropdown(
                        id="feature_dropdown",
                        style={"display": "block", "margin-left": "auto",
                                "margin-right": "auto", "width": "300px"},
                        options= feature_list,
                        value= feature_list[0]['value']
                    ),
                    html.Br(),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Span('From Year:'),
                                    dcc.Dropdown(id='from_year',
                                                style={"display": "block", "margin-left": "auto",
                                                        "margin-right": "auto", "width": "150px"},
                                                value=min_year,
                                                options=year_list)
                                ], style={"textAlign": "center", "width": "150px"}
                            ),
                            html.Div(
                                [
                                    html.Span('To Year:'),
                                    dcc.Dropdown(id='to_year',
                                                style={"display": "block", "margin-left": "auto",
                                                        "margin-right": "auto", "width": "150px"},
                                                value=max_year,
                                                options=year_list)
                                ], style={"textAlign": "center", "width": "150px"}
                            )
                        ], style={"position": "relative", "display": "flex", "flex-wrap": "wrap", "justify-content": "center", "align-items": "center", "width": "100%"}
                    ),
                    html.Div(
                        [
                            dcc.Graph(id="bar_chart", style={"width":"500px", "height":"80%"}),
                            dcc.Graph(id="pie_chart"),
                        ],
                        style={"display": "flex", "flex-wrap": "wrap", "justify-content": "center", "align-items": "center"}
                    ),
                    html.Div(
                        [
                            dcc.Graph(id="line_chart", style={"width":"650px"}),
                            dcc.Graph(id="linear_chart", style={"width": "650px"})
                        ],
                        style={"position": "relative", "width": "100%", "display": "flex", "flex-wrap": "wrap", "justify-content": "center", "align-items": "center"}
                    ),
                ]
            ), 
            html.Br(),
            html.Div([
                html.H1("Regions Economic in Glance", style={"textAlign":"center"}),
                html.Div("Region: ", style={"textAlign":"center"}),
                dcc.Dropdown(
                    id="region_dropdown",
                    style={"display": "block", "margin-left": "auto",
                            "margin-right": "auto", "width": "300px"},
                    options= region_list,
                    value='North America'
                ),
                html.Br(),
                html.Div("Feature to view: ", style={"textAlign":"center"}),
                dcc.Dropdown(
                    id="geo_feature_dropdown",
                    style={"display": "block", "margin-left": "auto",
                            "margin-right": "auto", "width": "300px"},
                    options=feature_list,
                    value=feature_list[0]['value']
                ),
                html.Br(),
                html.Div("Group of Income: ", style={"textAlign":"center"}),
                dcc.RadioItems(
                    id='incomegroup_radio', 
                    options=incomegroup_list,
                    value="All",
                    inline=True,
                    style={"textAlign":"center"}
                ),
                dcc.Graph(id="geo_graph", style={"width": "800px", "height":"600px"}),
            ]),
            html.Br(),
            html.Div(
                [
                    html.H1("Statistic and Machine Learning View", style={"textAlign":"center"}),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Span('X value:'),
                                    dcc.Dropdown(id='x_dropdown',
                                                style={"display": "block", "margin-left": "auto",
                                                    "margin-right": "auto", "width": "250px"},
                                                value=x_list[0]['value'],
                                                options=x_list)
                                ], style={"textAlign": "center", "width": "250px"}
                            ),
                            html.Div(
                                [
                                    html.Span('Y value:'),
                                    dcc.Dropdown(id='y_dropdown',
                                                style={"display": "block", "margin-left": "auto",
                                                    "margin-right": "auto", "width": "250px"},
                                                value=y_list[1]['value'],
                                                options=y_list)
                                ], style={"textAlign": "center", "width": "250px"}
                            ),
                            html.Div(
                                [
                                    html.Span('Label:'),
                                    dcc.Dropdown(id='label_dropdown',
                                                    style={"display": "block", "margin-left": "auto",
                                                        "margin-right": "auto", "width": "150px"},
                                                value="IncomeGroup",
                                                options=[{"label": "IncomeGroup", "value": "IncomeGroup"}])
                                ], style={"textAlign": "center", "width": "150px"}
                            )
                        ], style={"position": "relative", "display": "flex", "flex-wrap": "wrap", "justify-content": "center", "align-items": "center", "width": "100%"}
                    ),
                    dcc.Graph(id="knn_graph"),
                    html.P("Select number of neighbors:"),
                    dcc.Slider(
                        id='slider-neighbors',
                        min=5, max=20, step=1, value=12,
                        marks={i: str(i) for i in range(5,21,5)})
                ]
            )
        ],
        style={"position":"relative", "width": "100%", "display": "flex", "flex-direction": "column", "justify-content": "center", "align-items": "center", "overflow":"hidden"}
    )