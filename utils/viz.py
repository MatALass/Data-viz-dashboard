import plotly.express as px

def bar(df, x, y, title, color=None, text_auto=True):
    fig = px.bar(df, x=x, y=y, color=color, text_auto=text_auto, title=title)
    fig.update_layout(xaxis_title=x, yaxis_title=y)
    return fig

def pie(df, names, title):
    return px.pie(df, names=names, title=title)

def hist(df, x, title, nbins=15, color=None):
    return px.histogram(df, x=x, nbins=nbins, color=color, title=title)

def scatter(df, x, y, color, title):
    return px.scatter(df, x=x, y=y, color=color, title=title)

def choropleth(df, geo_col, value_col, title):
    import geopandas as gpd
    import json
    from urllib.request import urlopen

    url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions.geojson"
    geojson = json.load(urlopen(url))
    fig = px.choropleth(
        df, geojson=geojson,
        locations=geo_col, featureidkey="properties.nom",
        color=value_col,
        title=title,
        color_continuous_scale="Blues"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    return fig

def count_df(df, column_name, new_name=None):
    """Return a clean DataFrame with columns [Label, Count] for Plotly charts."""
    new_name = new_name or column_name
    counts = df[column_name].value_counts(dropna=False).reset_index()
    counts.columns = [new_name, 'Count']
    return counts
