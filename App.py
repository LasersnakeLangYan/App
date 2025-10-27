from plotly.data import gapminder
from dash import dcc, html, Dash, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css"]
app = Dash(name="Gapminder Dashboard", external_stylesheets=css)

################### DATASET ####################################
gapminder_df = gapminder(datetimes=True, centroids=True, pretty_names=True)
gapminder_df["Year"] = gapminder_df.Year.dt.year

#################### CHARTS ####################################
def create_table():
    fig = go.Figure(data=[go.Table(
        header=dict(values=gapminder_df.columns, align='left'),
        cells=dict(values=gapminder_df.values.T, align='left'))
    ])
    fig.update_layout(paper_bgcolor="#eef1f7", margin=dict(l=0, r=0, t=0, b=0), height=550)
    return fig

def create_population_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df.Continent==continent) & (gapminder_df.Year==year)]
    filtered_df = filtered_df.sort_values(by="Population", ascending=False).head(15)

    fig = px.bar(filtered_df, x="Country", y="Population", color="Country",
                 title="Top 15 Population — {} ({})".format(continent, year),
                 text_auto=True)
    fig.update_layout(paper_bgcolor="#eef1f7", height=350)
    return fig

def create_gdp_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df.Continent==continent) & (gapminder_df.Year==year)]
    filtered_df = filtered_df.sort_values(by="GDP per Capita", ascending=False).head(15)

    fig = px.bar(filtered_df, x="Country", y="GDP per Capita", color="Country",
                 title="Top 15 GDP per Capita — {} ({})".format(continent, year),
                 text_auto=True)
    fig.update_layout(paper_bgcolor="#eef1f7", height=350)
    return fig

def create_life_exp_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df.Continent==continent) & (gapminder_df.Year==year)]
    filtered_df = filtered_df.sort_values(by="Life Expectancy", ascending=False).head(15)

    fig = px.bar(filtered_df, x="Country", y="Life Expectancy", color="Country",
                 title="Top 15 Life Expectancy — {} ({})".format(continent, year),
                 text_auto=True)
    fig.update_layout(paper_bgcolor="#eef1f7", height=350)
    return fig

def create_map(variable, year):
    filtered_df = gapminder_df[gapminder_df.Year == year]
    fig = px.choropleth(filtered_df,
                        color=variable,
                        locations="ISO Alpha Country Code",
                        locationmode="ISO-3",
                        hover_data=["Country", variable],
                        color_continuous_scale="Viridis",
                        title="{} in {}".format(variable, year))
    fig.update_layout(paper_bgcolor="#eef1f7", height=550, margin=dict(l=0, r=0, t=50, b=0))
    return fig


##################### WIDGETS ###################################
continents = gapminder_df.Continent.unique()
years = gapminder_df.Year.unique()


##################### APP LAYOUT ###############################
app.layout = html.Div([
    html.H1("🌍 Gapminder Global Insights Dashboard",
            className="text-center fw-bold m-3"),

    # TABLE
    html.Div([
        dcc.Graph(id="dataset", figure=create_table(), style={"height": "500px"})
    ], className="row m-2"),

    # CHARTS + CONTROLS SECTION
    html.Div([

        # SIDEBAR
        html.Div([
            html.H5("Controls", className="fw-bold mb-3"),

            html.Label("Continent"),
            dcc.Dropdown(id="continent", options=continents,
                         value="Asia", clearable=False, className="mb-3"),

            html.Label("Year"),
            dcc.Dropdown(id="year", options=years,
                         value=1952, clearable=False, className="mb-3"),
        ], className="col-lg-2 col-md-3 col-sm-12 bg-light p-3 rounded shadow-sm"),

        # CHART PANEL
        html.Div([
            dcc.Graph(id="population", style={"height": "380px"}),
            dcc.Graph(id="gdp", style={"height": "380px"}),
            dcc.Graph(id="life_exp", style={"height": "380px"}),
        ], className="col-lg-10 col-md-9 col-sm-12"),
    ], className="row mt-3 g-3"),

    # MAP SECTION
    html.Div([
        html.Div([
            html.H5("World Map Settings", className="fw-bold mb-3"),

            html.Label("Variable"),
            dcc.Dropdown(id="var_map",
                         options=["Population", "GDP per Capita", "Life Expectancy"],
                         value="Life Expectancy", clearable=False, className="mb-3"),

            html.Label("Year"),
            dcc.Dropdown(id="year_map", options=years,
                         value=1952, clearable=False),
        ], className="col-lg-3 bg-light p-3 rounded shadow-sm"),

        html.Div([
            dcc.Graph(id="choropleth_map", style={"height": "600px"})
        ], className="col-lg-9"),

    ], className="row mt-4 g-3"),
], style={"background-color": "#eef1f7", "padding-bottom": "50px"})


##################### CALLBACKS ###############################
@callback(
    [Output("population", "figure"),
     Output("gdp", "figure"),
     Output("life_exp", "figure")],
    [Input("continent", "value"),
     Input("year", "value")]
)
def update_main_charts(continent, year):
    return (
        create_population_chart(continent, year),
        create_gdp_chart(continent, year),
        create_life_exp_chart(continent, year)
    )


@callback(
    Output("choropleth_map", "figure"),
    [Input("var_map", "value"),
     Input("year_map", "value")]
)
def update_map_output(var, year):
    return create_map(var, year)


if __name__ == "__main__":
    app.run(debug=True)
