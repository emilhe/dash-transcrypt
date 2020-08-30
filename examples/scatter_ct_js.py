scale = 10  # <kwarg>

def point_to_layer(feature, latlng, context):
    radius = feature.properties.value * scale
    return L.circleMarker(latlng, dict(radius=radius))
