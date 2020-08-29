def point_to_layer(feature, latlng, context):
    scale = context.props.hideout.scale
    radius_property = context.props.hideout.radius_property
    radius = feature.properties[radius_property] ** 0.5 / scale
    return L.circleMarker(latlng, dict(radius=radius))
