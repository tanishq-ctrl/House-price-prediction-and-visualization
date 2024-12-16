import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset
data_path = "/Users/tanishq/Desktop/Projects/home-data-for-ml-course/train.csv"
data = pd.read_csv(data_path)

# Prepare data for the visualizations
data['LotFrontageAvailable'] = data['LotFrontage'].notnull().map({True: 'Available', False: 'Missing'})
data['Renovated'] = data['YearBuilt'] != data['YearRemodAdd']

# Sample latitude and longitude data for neighborhoods (mock data for visualization purposes)
# Replace this with actual geospatial data if available
data['Latitude'] = data['Neighborhood'].map({
    'CollgCr': 42.025, 'Veenker': 42.030, 'Crawfor': 42.022,
    'NoRidge': 42.050, 'Mitchel': 42.018, 'Somerst': 42.031,
    'NWAmes': 42.040, 'OldTown': 42.016, 'BrkSide': 42.012,
    'Sawyer': 42.025, 'IDOTRR': 42.007, 'MeadowV': 42.010,
    'Edwards': 42.017, 'Timber': 42.042, 'Gilbert': 42.080,
    'StoneBr': 42.055, 'ClearCr': 42.045, 'NPkVill': 42.036,
    'Blmngtn': 42.062, 'Blueste': 42.065, 'SawyerW': 42.028,
    'SWISU': 42.013, 'NridgHt': 42.054, 'NAmes': 42.053,
    'Names': 42.050, 'Brookside': 42.015, 'Other': 42.000
})
data['Longitude'] = data['Neighborhood'].map({
    'CollgCr': -93.655, 'Veenker': -93.650, 'Crawfor': -93.670,
    'NoRidge': -93.635, 'Mitchel': -93.685, 'Somerst': -93.645,
    'NWAmes': -93.680, 'OldTown': -93.630, 'BrkSide': -93.620,
    'Sawyer': -93.625, 'IDOTRR': -93.610, 'MeadowV': -93.600,
    'Edwards': -93.640, 'Timber': -93.690, 'Gilbert': -93.750,
    'StoneBr': -93.630, 'ClearCr': -93.670, 'NPkVill': -93.665,
    'Blmngtn': -93.690, 'Blueste': -93.700, 'SawyerW': -93.645,
    'SWISU': -93.620, 'NridgHt': -93.640, 'NAmes': -93.675,
    'Names': -93.660, 'Brookside': -93.615, 'Other': -93.590
})

# Initialize the app
app = dash.Dash(__name__)
app.title = "Real Estate Dashboard"

# Layout
app.layout = html.Div([
    html.H1("Real Estate Interactive Dashboard", style={"textAlign": "center", "color": "#4B0082"}),

    # SalePrice Over Time Heatmap
    html.Div([
        html.H2("SalePrice Over Time (Year vs. Month)", style={"color": "#4B0082"}),
        dcc.Graph(id="heatmap"),
    ]),

    # Living Area vs. SalePrice
    html.Div([
        html.H2("Living Area vs. SalePrice", style={"color": "#4B0082"}),
        dcc.Dropdown(
            id="neighborhood_filter",
            options=[{"label": n, "value": n} for n in data['Neighborhood'].unique()],
            placeholder="Select a Neighborhood",
            multi=True
        ),
        dcc.Graph(id="scatter_plot"),
    ]),

    # Overall Quality vs. SalePrice
    html.Div([
        html.H2("Overall Quality vs. SalePrice", style={"color": "#4B0082"}),
        dcc.Slider(
            id="year_filter",
            min=data['YearBuilt'].min(),
            max=data['YearBuilt'].max(),
            step=1,
            value=data['YearBuilt'].max(),
            marks={str(year): str(year) for year in range(data['YearBuilt'].min(), data['YearBuilt'].max()+1, 10)},
        ),
        dcc.Graph(id="boxplot"),
    ]),

    # Average SalePrice by Neighborhood
    html.Div([
        html.H2("Average SalePrice by Neighborhood", style={"color": "#4B0082"}),
        dcc.Graph(id="neighborhood_bar_chart"),
    ]),

    # SalePrice Distribution by Garage Type
    html.Div([
        html.H2("SalePrice Distribution by Garage Type", style={"color": "#4B0082"}),
        dcc.Graph(id="garage_boxplot"),
    ]),

    # SalePrice Distribution by Building Type
    html.Div([
        html.H2("SalePrice Distribution by Building Type", style={"color": "#4B0082"}),
        dcc.Graph(id="building_type_boxplot"),
    ]),

    # SalePrice by House Style
    html.Div([
        html.H2("SalePrice by House Style", style={"color": "#4B0082"}),
        dcc.Graph(id="house_style_boxplot"),
    ]),

    # Price Impact of Renovations
    html.Div([
        html.H2("Price Impact of Renovations", style={"color": "#4B0082"}),
        dcc.Graph(id="renovation_price_impact"),
    ]),

    # Neighborhood Map
    html.Div([
        html.H2("Neighborhood Map", style={"color": "#4B0082"}),
        dcc.Graph(id="neighborhood_map"),
    ]),

    # Correlation Heatmap
    html.Div([
        html.H2("Correlation Heatmap", style={"color": "#4B0082"}),
        dcc.Graph(id="correlation_heatmap"),
    ]),

    # Number of Properties Built Per Year
    html.Div([
        html.H2("Number of Properties Built Per Year", style={"color": "#4B0082"}),
        dcc.Graph(id="year_built_histogram"),
    ]),
])

# Callbacks
@app.callback(
    Output("heatmap", "figure"),
    Input("heatmap", "id")
)
def update_heatmap(_):
    avg_price_by_year_month = data.groupby(['YrSold', 'MoSold'])['SalePrice'].mean().reset_index()
    avg_price_by_year_month_pivot = avg_price_by_year_month.pivot(index='YrSold', columns='MoSold', values='SalePrice')
    fig = px.imshow(
        avg_price_by_year_month_pivot,
        color_continuous_scale="Spectral",
        labels={"color": "Average SalePrice"},
        title="Average SalePrice by Year and Month"
    )
    fig.update_layout(plot_bgcolor="#F5F5DC", title_font_color="#4B0082")
    return fig

@app.callback(
    Output("scatter_plot", "figure"),
    Input("neighborhood_filter", "value")
)
def update_scatter(neighborhoods):
    filtered_data = data if not neighborhoods else data[data['Neighborhood'].isin(neighborhoods)]
    fig = px.scatter(
        filtered_data, x="GrLivArea", y="SalePrice", color="SalePrice",
        color_continuous_scale="Spectral", title="Living Area vs. SalePrice",
        labels={"GrLivArea": "Living Area (sqft)", "SalePrice": "Sale Price"}
    )
    fig.update_layout(plot_bgcolor="#F5F5DC", title_font_color="#4B0082")
    return fig

@app.callback(
    Output("boxplot", "figure"),
    Input("year_filter", "value")
)
def update_boxplot(year):
    filtered_data = data[data['YearBuilt'] <= year]
    fig = px.box(
        filtered_data, x="OverallQual", y="SalePrice", points="all", color_discrete_sequence=px.colors.qualitative.Set2, title="SalePrice by Overall Quality",
        labels={"OverallQual": "Overall Quality", "SalePrice": "Sale Price"}
    )
    fig.update_layout(plot_bgcolor="#F5F5DC", title_font_color="#4B0082")
    return fig

@app.callback(
    Output("neighborhood_bar_chart", "figure"),
    Input("neighborhood_bar_chart", "id")
)
def update_neighborhood_chart(_):
    avg_price_by_neighborhood = data.groupby('Neighborhood')['SalePrice'].mean().sort_values(ascending=False)
    fig = px.bar(
        avg_price_by_neighborhood,
        orientation="h",
        labels={"value": "Average SalePrice", "index": "Neighborhood"},
        title="Average SalePrice by Neighborhood",
        color=avg_price_by_neighborhood.values,
        color_continuous_scale="Spectral"
    )
    fig.update_layout(plot_bgcolor="#F5F5DC", title_font_color="#4B0082", yaxis=dict(autorange="reversed"))
    return fig

@app.callback(
    Output("garage_boxplot", "figure"),
    Input("garage_boxplot", "id")
)
def update_garage_boxplot(_):
    fig = px.box(
        data, x="GarageType", y="SalePrice", color="GarageType",
        title="SalePrice by Garage Type",
        labels={"GarageType": "Garage Type", "SalePrice": "Sale Price"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(plot_bgcolor="#F5F5DC", title_font_color="#4B0082")
    return fig

@app.callback(
    Output("building_type_boxplot", "figure"),
    Input("building_type_boxplot", "id")
)
def update_building_type_boxplot(_):
    fig = px.box(
        data, x="BldgType", y="SalePrice", color="BldgType",
        title="SalePrice by Building Type",
        labels={"BldgType": "Building Type", "SalePrice": "Sale Price"},
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_layout(plot_bgcolor="#F5F5DC", title_font_color="#4B0082")
    return fig

@app.callback(
    Output("house_style_boxplot", "figure"),
    Input("house_style_boxplot", "id")
)
def update_house_style_boxplot(_):
    fig = px.box(
        data, x="HouseStyle", y="SalePrice", color="HouseStyle",
        title="SalePrice by House Style",
        labels={"HouseStyle": "House Style", "SalePrice": "Sale Price"},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(plot_bgcolor="#F5F5DC", title_font_color="#4B0082")
    return fig

@app.callback(
    Output("renovation_price_impact", "figure"),
    Input("renovation_price_impact", "id")
)
def update_renovation_price_impact(_):
    fig = px.box(
        data, x="Renovated", y="SalePrice", color="Renovated",
        title="Price Impact of Renovations",
        labels={"Renovated": "Renovated", "SalePrice": "Sale Price"},
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig.update_layout(plot_bgcolor="#F5F5DC", title_font_color="#4B0082")
    return fig

@app.callback(
    Output("neighborhood_map", "figure"),
    Input("neighborhood_map", "id")
)
def update_neighborhood_map(_):
    fig = px.scatter_mapbox(
        data, lat="Latitude", lon="Longitude", size="SalePrice", color="SalePrice",
        hover_name="Neighborhood", zoom=10,
        title="Neighborhood Map: SalePrice Distribution",
        color_continuous_scale="Viridis"
    )
    fig.update_layout(
        mapbox_style="open-street-map",
        plot_bgcolor="#F5F5DC",
        title_font_color="#4B0082"
    )
    return fig

@app.callback(
    Output("correlation_heatmap", "figure"),
    Input("correlation_heatmap", "id")
)
def update_correlation_heatmap(_):
    numeric_data = data.select_dtypes(include=['float64', 'int64'])
    corr_matrix = numeric_data.corr()
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="Spectral",
        title="Feature Correlation Heatmap"
    )
    fig.update_layout(plot_bgcolor="#F5F5DC", title_font_color="#4B0082")
    return fig

@app.callback(
    Output("year_built_histogram", "figure"),
    Input("year_built_histogram", "id")
)
def update_year_built_histogram(_):
    fig = px.histogram(
        data, x="YearBuilt", nbins=30, color_discrete_sequence=["#2E8B57"],
        title="Number of Properties Built Per Year",
        labels={"YearBuilt": "Year Built", "count": "Number of Properties"}
    )
    fig.update_layout(plot_bgcolor="#F5F5DC", title_font_color="#4B0082")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
