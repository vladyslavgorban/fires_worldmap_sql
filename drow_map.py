import plotly.graph_objs  as go
import plotly.express as px
import math 

# https://plotly.github.io/plotly.py-docs/generated/plotly.express.scatter_mapbox.html
# https://plotly.com/python/scatter-plots-on-maps/ 
# https://plotly.com/python/reference/


def draw_fire_map(name, dates, lons, lats, frps):
    """drow fires with fire radiative power on the map"""
    chart_title = name
    
    # draw data on map
    data = [{
        'type': 'scattergeo',
        'lon': lons,
        'lat': lats,
        'text': dates,
        'marker': {
            'size': [frp ** (0.37) for frp in frps],
            'color': frps,
            'colorscale': 'Portland',
            'reversescale': False,
            'colorbar': {'title': 'fire radiative power'},
        },
    }]

    my_layout = go.Layout(title=chart_title)
    fig = go.Figure(data=data, layout=my_layout)

    fig.show()
