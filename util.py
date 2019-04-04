

def gps_to_feet(lat, lon):
	scaling_factor = 10000 / 90 * 3280.4
	return (scaling_factor * lat, scaling_factor * lon)

def feet_to_gps(feet):
	scaling_factor = (90 / 10000) / 3280.4
	return scaling_factor * feet