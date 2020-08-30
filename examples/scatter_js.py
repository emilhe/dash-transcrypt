def point_to_layer(feature, latlng, context):
    radius = feature.properties.value*10
    return L.circleMarker(latlng, dict(radius=radius))
