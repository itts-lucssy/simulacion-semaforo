Este programa simula el funcionamiento de un semáforo en una intersección vehicular, basado en un análisis teórico y datos recabados mediante observación de campo (video con temporizador de cuenta regresiva).

El sistema modela el comportamiento cíclico del semáforo (rojo → verde → amarillo) mientras los vehículos llegan de forma aleatoria, se acumulan en una fila durante la fase roja, y cruzan la intersección durante la fase verde.

¿Cómo funciona el programa?
Entrada de datos: al ejecutarse, el programa pregunta al usuario los tiempos de cada fase y los datos de llegada de vehículos. Si el usuario no escribe nada y solo presiona Enter, se usan los valores observados en campo.
Simulación: usando la librería SimPy, se crean dos procesos que corren en paralelo:
El semáforo, que cicla entre rojo, verde y amarillo.
El generador de vehículos, que hace llegar autos a la intersección en tiempos aleatorios (distribución exponencial), simulando el tráfico real.
Salida: al terminar la simulación, el programa muestra:
Total de vehículos generados y cuántos lograron cruzar
Tiempo de espera promedio y máximo por vehículo
Longitud máxima que alcanzó la fila
Vehículos que cruzaron en cada ciclo de verde
