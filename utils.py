
import openrouteservice
from openrouteservice import convert

estado_coords = {'Aguascalientes': (-102.296, 21.8853), 'Baja California': (-115.4726, 30.8406), 'Baja California Sur': (-110.3005, 24.1426), 'Campeche': (-90.527, 19.8301), 'Chiapas': (-92.6376, 16.7569), 'Chihuahua': (-106.076, 28.6353), 'Ciudad de México': (-99.1332, 19.4326), 'Coahuila': (-101.0, 27.0587), 'Colima': (-103.865, 19.2452), 'Durango': (-104.656, 24.0277), 'Estado de México': (-99.667, 19.3574), 'Guanajuato': (-101.257, 21.019), 'Guerrero': (-99.9018, 17.4392), 'Hidalgo': (-98.8458, 20.0911), 'Jalisco': (-103.3496, 20.6597), 'Michoacán': (-101.7068, 19.5665), 'Morelos': (-99.2345, 18.6813), 'Nayarit': (-104.8957, 21.7514), 'Nuevo León': (-100.3161, 25.6866), 'Oaxaca': (-96.7266, 17.0732), 'Puebla': (-98.2063, 19.0414), 'Querétaro': (-100.3899, 20.5888), 'Quintana Roo': (-88.3035, 18.9712), 'San Luis Potosí': (-100.9846, 22.1565), 'Sinaloa': (-107.385, 24.8091), 'Sonora': (-110.9542, 29.0729), 'Tabasco': (-92.9635, 17.8409), 'Tamaulipas': (-98.8144, 24.2669), 'Tlaxcala': (-98.2375, 19.3182), 'Veracruz': (-96.1342, 19.1738), 'Yucatán': (-89.1212, 20.9801), 'Zacatecas': (-102.5832, 22.7709)}

client = openrouteservice.Client(key="5b3ce3597851110001cf6248a9486e7ed3c8400fa3ada5fc9ecc4546")

def calcular_ruta_y_restricciones(origen, destino, restricciones, vehiculo):
    coords = [estado_coords[origen], estado_coords[destino]]

    profile = "driving-car" if vehiculo == "Auto" else "cycling-regular" if vehiculo == "Bicicleta" else "foot-walking"

    ruta = client.directions(
        coordinates=coords,
        profile=profile,
        format='geojson'
    )

    props = ruta['features'][0]['properties']['segments'][0]
    distancia_km = props['distance'] / 1000
    duracion_hrs = props['duration'] / 3600

    rendimiento = float(restricciones.get('rendimiento', 12))
    capacidad = float(restricciones.get('tanque', 50))
    presupuesto = float(restricciones.get('presupuesto', 1000))
    temp_max = float(restricciones.get('temperatura', 50))
    tiempo_max = float(restricciones.get('tiempo', 999))
    seguro = restricciones.get('seguro', False)

    gasolina = distancia_km / rendimiento
    costo_estimado = gasolina * 23.5

    advertencias = []
    if gasolina > capacidad:
        advertencias.append("⚠️ Requiere más de un tanque de gasolina.")
    if costo_estimado > presupuesto:
        advertencias.append("⚠️ El costo excede tu presupuesto.")
    if duracion_hrs > tiempo_max:
        advertencias.append("⚠️ El tiempo estimado excede el máximo deseado.")
    if temp_max < 20:
        advertencias.append("⚠️ La temperatura máxima es muy baja, revisa clima antes de salir.")

    return ruta, {
        "distancia": round(distancia_km, 2),
        "gasolina": round(gasolina, 2),
        "costo_estimado": round(costo_estimado, 2),
        "temperatura": 27,  # valor simulado
        "tiempo_estimado": round(duracion_hrs, 2),
        "riesgo_climatico": "Bajo" if seguro else "Moderado",
        "advertencias": advertencias
    }
