scale = 100  # <kwarg>
radius_property = "population"  # <kwarg>

def point_to_layer(feature, latlng, context):
    radius = feature.properties[radius_property] ** 0.5 / scale
    return L.circleMarker(latlng, dict(radius=radius))
