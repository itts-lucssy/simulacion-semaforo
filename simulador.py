import simpy
import random
def pedir_dato(mensaje, valor_por_defecto):
    """Pide un número al usuario; si no escribe nada, usa el valor por defecto"""
    entrada = input(f"{mensaje} [Enter para usar {valor_por_defecto}]: ")
    if entrada.strip() == "":
        return valor_por_defecto
    return float(entrada)
 
 
print("SIMULACIÓN DE SEMÁFORO")
print("Ingresa los datos recabados en campo (o presiona Enter para usar los valores observados)\n")
 
t_rojo = pedir_dato("Duración de la fase ROJA para nuestro sentido (segundos)", 47)
t_verde = pedir_dato("Duración de la fase VERDE para nuestro sentido (segundos)", 20)
t_amarillo = pedir_dato("Duración de la fase AMARILLA (segundos)", 3)
 
t_entre_llegadas = pedir_dato(
    "Tiempo promedio entre llegadas de vehículos (segundos)", 4)
t_cruce = pedir_dato(
    "Tiempo promedio que tarda un vehículo en cruzar la intersección (segundos)", 2)
num_ciclos = int(pedir_dato("Número de ciclos completos a simular", 5))

estado_semaforo = {"color": "rojo"}  
fila_espera = []                       
tiempos_espera = []                    
vehiculos_cruzados_por_ciclo = []      
longitud_maxima_fila = 0              
contador_vehiculos = 0                 
 
def semaforo(env):
    """Controla el ciclo repetitivo: rojo, verde, amarillo, rojo ..."""
    global longitud_maxima_fila
 
    for ciclo in range(num_ciclos):
        estado_semaforo["color"] = "rojo"
        print(f"\n[{env.now:6.1f}s] Ciclo {ciclo + 1}: ROJO (los vehículos esperan)")
        yield env.timeout(t_rojo)
 
        if len(fila_espera) > longitud_maxima_fila:
            longitud_maxima_fila = len(fila_espera)

        estado_semaforo["color"] = "verde"
        print(f"[{env.now:6.1f}s] Ciclo {ciclo + 1}: VERDE (los vehículos cruzan)")
 
        tiempo_fin_verde = env.now + t_verde
        cruzados_este_ciclo = 0

        while env.now < tiempo_fin_verde and len(fila_espera) > 0:
            hora_llegada = fila_espera.pop(0)
            espera = env.now - hora_llegada
            tiempos_espera.append(espera)
            cruzados_este_ciclo += 1
            print(f" vehículo cruza (esperó {espera:.1f}s)")
            yield env.timeout(t_cruce)
 
        vehiculos_cruzados_por_ciclo.append(cruzados_este_ciclo)
 
        tiempo_restante = tiempo_fin_verde - env.now
        if tiempo_restante > 0:
            yield env.timeout(tiempo_restante)

        estado_semaforo["color"] = "amarillo"
        print(f"[{env.now:6.1f}s] Ciclo {ciclo + 1}: AMARILLO (precaución)")
        yield env.timeout(t_amarillo)
 
def generador_vehiculos(env):
    """Genera vehículos que llegan a la intersección y se forman en la fila."""
    global contador_vehiculos
    while True:
        yield env.timeout(random.expovariate(1.0 / t_entre_llegadas))
        contador_vehiculos += 1
        fila_espera.append(env.now)
 
env = simpy.Environment()
env.process(semaforo(env))
env.process(generador_vehiculos(env))
env.run()
 
print("\n" + "=" * 50)
print("RESULTADOS DE LA SIMULACIÓN")
print("=" * 50)
print(f"Vehículos generados en total:      {contador_vehiculos}")
print(f"Vehículos que lograron cruzar:     {len(tiempos_espera)}")
print(f"Vehículos que quedaron en fila:    {len(fila_espera)}")
 
if tiempos_espera:
    promedio_espera = sum(tiempos_espera) / len(tiempos_espera)
    print(f"Tiempo de espera promedio:         {promedio_espera:.2f} s")
    print(f"Tiempo de espera máximo:           {max(tiempos_espera):.2f} s")
 
print(f"Longitud máxima de la fila:        {longitud_maxima_fila} vehículos")
print(f"Vehículos cruzados por ciclo:      {vehiculos_cruzados_por_ciclo}")
if vehiculos_cruzados_por_ciclo:
    promedio_ciclo = sum(vehiculos_cruzados_por_ciclo) / len(vehiculos_cruzados_por_ciclo)
    print(f"Promedio de vehículos por ciclo:   {promedio_ciclo:.1f}")