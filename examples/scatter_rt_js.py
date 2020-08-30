def point_to_layer(feature, latlng, context):
    scale = context.props.hideout.scale
    radius = feature.properties.value * scale
    return L.circleMarker(latlng, dict(radius=radius))
