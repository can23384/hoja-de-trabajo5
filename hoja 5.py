import simpy
import random
import statistics
import matplotlib.pyplot as plt

# Semilla para la generación de números aleatorios
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# Definición de la función del proceso
def generador_procesos(env, RAM, CPU, cantidad_procesos, tiempos_ejecucion):
    for proceso_id in range(1, cantidad_procesos + 1):
        # Generamos el intervalo entre llegadas de procesos
        yield env.timeout(random.expovariate(1.0 / 10))
        # Generamos valores únicos de memoria RAM e instrucciones para cada proceso
        memoria_necesaria = random.randint(1, 10)
        instrucciones_totales = random.randint(1, 10)
        # Creamos un nuevo proceso
        env.process(proceso(env, f"Proceso-{proceso_id}", RAM, CPU, memoria_necesaria, instrucciones_totales, tiempos_ejecucion))

# Definición de la función del proceso
def proceso(env, nombre, RAM, CPU, memoria_necesaria, instrucciones_totales, tiempos_ejecucion):
    # El proceso llega al sistema operativo y solicita memoria RAM
    yield RAM.get(memoria_necesaria)
    tiempo_inicio = env.now  # Registro del tiempo de inicio
    
    # El proceso pasa al estado de listo (ready)
    instrucciones_pendientes = instrucciones_totales
    
    # Ejecución del proceso
    while instrucciones_pendientes > 0:
        # Se ejecutan hasta un máximo de 3 instrucciones
        instrucciones_a_ejecutar = min(3, instrucciones_pendientes)
        with CPU.request() as req:
            yield req
            yield env.timeout(1)  # Simulamos que el CPU ejecuta 3 instrucciones en 1 unidad de tiempo
            instrucciones_pendientes -= instrucciones_a_ejecutar
            
            # Verificamos si el proceso ha terminado
            if instrucciones_pendientes <= 0:
                tiempo_fin = env.now  # Registro del tiempo de finalización
                tiempos_ejecucion.append(tiempo_fin - tiempo_inicio)  # Calculamos el tiempo de ejecución y lo añadimos a la lista
                break

    # Se devuelve la memoria RAM utilizada al finalizar el proceso
    yield RAM.put(memoria_necesaria)

# Función para ejecutar la simulación con una cantidad específica de procesos
def ejecutar_simulacion(cantidad_procesos):
    # Configuración de la simulación
    env = simpy.Environment()
    RAM = simpy.Container(env, init=100, capacity=100)
    CPU = simpy.Resource(env, capacity=1)
    tiempos_ejecucion = []

    # Ejecutamos el generador de procesos con la cantidad deseada
    env.process(generador_procesos(env, RAM, CPU, cantidad_procesos, tiempos_ejecucion))

    # Ejecutamos la simulación sin límite de tiempo
    env.run(until=1000)  # Simulamos durante un tiempo largo para recopilar suficientes datos

    # Calculamos el promedio y la desviación estándar del tiempo de ejecución
    promedio = statistics.mean(tiempos_ejecucion)
    desviacion_estandar = statistics.stdev(tiempos_ejecucion)
    
    print(f"Tiempo promedio con {cantidad_procesos} procesos: {promedio:.2f}")
    print(f"Desviación estándar con {cantidad_procesos} procesos: {desviacion_estandar:.2f}")
    
    return promedio, desviacion_estandar

# Lista para almacenar los resultados
resultados_promedio = []
resultados_desviacion = []
cantidades_procesos = [25, 50, 100, 150, 200]

# Ejecutamos la simulación para diferentes cantidades de procesos
for cantidad_procesos in cantidades_procesos:
    promedio, desviacion = ejecutar_simulacion(cantidad_procesos)
    resultados_promedio.append(promedio)
    resultados_desviacion.append(desviacion)

# Graficamos los resultados
plt.plot(cantidades_procesos, resultados_promedio, marker='o', linestyle='-', color='b', label='Promedio de tiempo')
plt.xlabel('Número de Procesos')
plt.ylabel('Tiempo Promedio')
plt.title('Tiempo Promedio de Ejecución en función del Número de Procesos')
plt.legend()
plt.grid(True)
plt.show()