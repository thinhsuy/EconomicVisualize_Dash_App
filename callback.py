from preprocessing import * 

@app.callback(
    Output('to_year', 'options'),
    Output('to_year', 'value'),
    Input('from_year', 'value')
)

def year_change(from_year):
    new_list_year = [year for year in range(min_year, max_year+1) if year>from_year]
    return new_list_year, new_list_year[-1]


@app.callback(
    Output('incomegroup_radio', 'options'),
    Output('incomegroup_radio', 'value'),
    Input('region_dropdown', 'value')
)

def region_vs_groupincome(region_dropdown):
    new_list_option = df.loc[df["Region"]==region_dropdown]["IncomeGroup"].value_counts().keys()
    return ["All"]+list(new_list_option), "All"


# Callback
@app.callback(
    Output('bar_chart', 'figure'), 
    Output('line_chart', 'figure'), 
    Output('pie_chart', 'figure'),
    Output('linear_chart', 'figure'), # output that need to change when callback
    Input('country_dropdown','value'), 
    Input('feature_dropdown','value'), 
    Input('from_year','value'), 
    Input('to_year','value') # input that would affect to the change of callback
)

# the order of parameters must match with the input order
def update_charts(country_dropdown, feature_dropdown, from_year, to_year):
    if len(country_dropdown) > 0:
        f_df = df[df['Country Name'].isin(country_dropdown)]
    else:
        f_df = df[df['Country Name']=='Vietnam']

    # Plot bar chart
    bar_data = {
        'Country Name': [name for name in country_dropdown],
        feature_dropdown: [f_df.loc[f_df['Country Name']==name, feature_dropdown].max() for name in country_dropdown]
    }
    fig_bar = px.bar(bar_data, 
                    x='Country Name', 
                    y=feature_dropdown, 
                    title=f'Maximum of {feature_dropdown}')
    
    # Plot line chart
    unique_years = [year for year in f_df["Year"].unique() if (int(year)>=int(from_year) and int(year)<=int(to_year))]
    line_data = {'Years': unique_years}
    for country in country_dropdown:
        line_data[country] = [df.loc[((df["Year"]==year) & (df["Country Name"]==country)), feature_dropdown].max() for year in unique_years]
    newdf = pd.DataFrame(line_data)
    fig_line = px.line(newdf, 
                       x='Years', 
                       y=country_dropdown,
                       color_discrete_sequence=px.colors.qualitative.Safe,
                       title=f'{feature_dropdown} between {from_year} and {to_year}')
    fig_line.update_traces(line=dict(width=5))
    fig_line.update_xaxes(title_text='Years')
    fig_line.update_yaxes(title_text=feature_dropdown)

    # Plot pie chart
    g_df = f_df[["Country Name", feature_dropdown]].groupby("Country Name").mean().reset_index("Country Name")
    fig_pie = px.pie(g_df, 
                    values=feature_dropdown, 
                    names='Country Name', 
                    title=f"Total portion of countries in {feature_dropdown}")
    

    # Plot linear regression chart
    fig_lr = go.Figure()
    color_list = px.colors.qualitative.Safe[:len(country_dropdown)]
    traces = []
    for country, color in zip(country_dropdown, color_list):
        lr_line_data={
            'Years':  unique_years,
            'Country': [df.loc[((df["Year"]==year) & (df["Country Name"]==country)), feature_dropdown].max() for year in unique_years]
        }
        tmp_df = pd.DataFrame(lr_line_data).dropna()
        x = np.array(tmp_df['Years']).astype(np.int64)
        y = np.array(tmp_df['Country']).astype(np.float32)
        scat_trace = go.Scatter(x=x, 
                                y=y, 
                                mode='markers', 
                                name=country,
                                showlegend=True,
                                marker=dict(color=color,size=10))
        
        lr = LinearRegression()
        lr.fit(x.reshape(-1, 1), y)
        x_line = np.linspace(x.min(), x.max(), 100).reshape(-1, 1)
        y_line = lr.predict(x_line)
        line_trace = go.Scatter(x=x_line.reshape(-1),
                                y=y_line,
                                mode='lines',
                                name=f'{country} linear',
                                showlegend=True,
                                line=dict(color=color, width=2))
        traces.append(scat_trace)
        traces.append(line_trace)

    layout = go.Layout(
        title=f'Linear Regression on {feature_dropdown}',
        xaxis=dict(title='Years'),
        yaxis=dict(title=feature_dropdown)
    )
    fig_lr = go.Figure(data=traces, layout=layout)
    return fig_bar, fig_line, fig_pie, fig_lr


@app.callback(
    Output("geo_graph", "figure"), 
    Input("region_dropdown", "value"),
    Input("geo_feature_dropdown", "value"),
    Input("incomegroup_radio", "value")
)

def display_choropleth(region_dropdown, geo_feature_dropdown, incomegroup_radio):
    if (incomegroup_radio!='All'):
        f_df = df.loc[((df['Region']==region_dropdown) & (df['IncomeGroup']==incomegroup_radio))]
    else: f_df = df.loc[df['Region']==region_dropdown]
    f_df = f_df[['Country Code', geo_feature_dropdown]].groupby('Country Code').mean().reset_index('Country Code')
    country_names = [pycountry.countries.get(alpha_3=code).name for code in f_df['Country Code']]

    choropleth_trace = go.Choropleth(
        locations=country_names,
        z=f_df[geo_feature_dropdown],
        locationmode='country names',
        colorscale='Viridis',
        colorbar_title='Unit(s)'
    )

    # Create the layout
    layout = go.Layout(
        title=f'The average distribution of {geo_feature_dropdown} in {region_dropdown}'
    )

    # Create the figure
    figure = go.Figure(data=[choropleth_trace], layout=layout)

    return figure


@app.callback(
    Output("knn_graph", "figure"), 
    Input("slider-neighbors", "value"))

def train_and_display_model(k):
    X, y = make_moons(noise=0.3, random_state=0) # replace with your own data source
    xrange, yrange = build_range(X, y)
    xx, yy = np.meshgrid(xrange, yrange)
    test_input = np.c_[xx.ravel(), yy.ravel()]

    clf = KNeighborsClassifier(k, weights='uniform')
    clf.fit(X, y)
    Z = clf.predict_proba(test_input)[:, 1]
    Z = Z.reshape(xx.shape)
    fig = build_figure(X, y, Z, xrange, yrange)

    return fig


# ############ HELPER FUNCTIONS ############
def build_range(X, y, mesh_size=.02, margin=.25):
    """
    Create an x range and a y range for building meshgrid
    """
    x_min = X[:, 0].min() - margin
    x_max = X[:, 0].max() + margin
    y_min = X[:, 1].min() - margin
    y_max = X[:, 1].max() + margin

    xrange = np.arange(x_min, x_max, mesh_size)
    yrange = np.arange(y_min, y_max, mesh_size)
    return xrange, yrange


def build_figure(X, y, Z, xrange, yrange):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y.astype(str), test_size=0.25, random_state=0)

    trace_specs = [
        [X_train, y_train, '0', 'Train', 'square'],
        [X_train, y_train, '1', 'Train', 'circle'],
        [X_test, y_test, '0', 'Test', 'square-dot'],
        [X_test, y_test, '1', 'Test', 'circle-dot']
    ]

    fig = go.Figure(data=[
        go.Scatter(
            x=X[y==label, 0], y=X[y==label, 1],
            name=f'{split}, y={label}',
            mode='markers', marker_symbol=marker
        )
        for X, y, label, split, marker in trace_specs
    ])
    fig.update_traces(
        marker_size=12, marker_line_width=1.5,
        marker_color="lightyellow"
    )

    fig.add_trace(
        go.Contour(
            x=xrange, y=yrange, z=Z,
            showscale=False, colorscale='RdBu',
            opacity=0.4, name='Score', hoverinfo='skip'
        )
    )

    return fig