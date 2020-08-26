# dash-transcrypt

Dash transcrypt translates Python code into JavaScript using the [transcrypt](https://www.transcrypt.org/) library. 

## Clientside callbacks

One of the main use cases for transpiling is clientside callbacks (which are usually written in JavaScript). The functions to be transpiled must be placed in a separate module (file), say `logic.py`. In this example, we will consider a simple `add` function,

    def add(a, b):
        return a + b
        
Before the `add` function can be used as a clientside callback, the `logic` module must be passed through the `to_clientside_functions` function. In addition to transpiling the module into JavaScript, it replaces the functional attributes of the module with appropriate `ClientsideFunction` objects so that they can be used in clientside callbacks,

    from dash_transcrypt import module_to_clientside_functions, inject_js
    ...
    inject_js(app, module_to_clientside_functions(logic))  # this is where the magic happens
    app.clientside_callback(logic.add, ...)

The `to_clientside_functions` returns the path to a JavaScript index file, which must be made available by the app (that's what `inject_js` does). For completeness, here is the full example app,

    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    import logic
    
    from dash.dependencies import Output, Input
    from dash_transcrypt import module_to_clientside_functions, inject_js
    
    # Create example app.
    app = dash.Dash()
    app.layout = html.Div([
        dcc.Input(id="a", value=2, type="number"), html.Div("+"),
        dcc.Input(id="b", value=2, type="number"), html.Div("="), html.Div(id="c"),
    ])
    # Create clientside callback.
    inject_js(app, module_to_clientside_functions(logic))
    app.clientside_callback(logic.add, Output("c", "children"), [Input("a", "value"), Input("b", "value")])
    
    if __name__ == '__main__':
        app.run_server()

## Functional properties

The other main use case for the `transpile` module is for passing function handles as Dash properties. Again, the functions to be transpiled must be placed in a separate module (file), say `styles.py`,
 
    marks = [0, 10, 20, 50, 100, 200, 500, 1000]
    colorscale = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026']
    
    def style(feature):
        color = None
        for i, item in enumerate(marks):
            if feature["properties"]["density"] > item:
                color = colorscale[i]
        return dict(fillColor=color, weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)
    
    def hover_style(feature):
        return dict(weight=5, color='#666', dashArray='')

The style function above was designed to match the signature of the `style` option of the [Leaflet GeoJSON object](https://leafletjs.com/reference-0.7.7.html#geojson-style). Before the functions can be used as properties, the module must be passed through the `to_js_functions` function. In addition to transpiling the module into JavaScript, it replaces the functional attributes of the module with strings that are translated into functions in the JavaScript layer,

    from dash_transcrypt import module_to_props, inject_js
    ...
    index = module_to_props(styles) 
    geojson = dl.GeoJSON(data=data, id="geojson", options=dict(style=styles.style), hoverStyle=styles.hover_style)
    ...
    inject_js(app, index)

For completeness, here is the full example app (tested with dash-leaflet==0.0.23),

    import dash
    import dash_html_components as html
    import json
    import dash_leaflet as dl
    import styles
    
    from dash_extensions.transpile import to_js_functions, inject_js
    
    # Create geojson.
    with open("assets/us-states.json", 'r') as f:
        data = json.load(f)
    index = module_to_props(styles) 
    geojson = dl.GeoJSON(data=data, id="geojson", options=dict(style=styles.style), hoverStyle=styles.hover_style)
    # Create app.
    app = dash.Dash(prevent_initial_callbacks=True)
    app.layout = html.Div([dl.Map(children=[dl.TileLayer(), geojson], center=[39, -98], zoom=4, id="map")],
                          style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"})
    # Inject transcrypted JavaScript.
    inject_js(app, index)
    
    
    if __name__ == '__main__':
        app.run_server()
