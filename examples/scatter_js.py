def point_to_layer(feature, latlng, context):
    radius = feature.properties.population**0.5/100
    return L.circleMarker(latlng, dict(radius=radius))
