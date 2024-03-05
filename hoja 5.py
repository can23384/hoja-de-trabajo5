import simpy
import random

# Semilla para la generación de números aleatorios
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# Definición de la función del proceso
def proceso(env, nombre, RAM, CPU):
    # El proceso llega al sistema operativo y solicita memoria RAM
    memoria_necesaria = random.randint(1, 10)
    yield RAM.get(memoria_necesaria)
    print(f"{nombre} solicita {memoria_necesaria} de memoria RAM en el tiempo {env.now}")
    
    # El proceso pasa al estado de listo (ready)
    instrucciones_totales = random.randint(1, 10)
    instrucciones_pendientes = instrucciones_totales
    print(f"{nombre} está listo para ejecutar con {instrucciones_totales} instrucciones pendientes en el tiempo {env.now}")
    
    # Ejecución del proceso
    while instrucciones_pendientes > 0:
        # Se ejecutan hasta un máximo de 3 instrucciones
        instrucciones_a_ejecutar = min(3, instrucciones_pendientes)
        with CPU.request() as req:
            yield req
            print(f"{nombre} empieza a ejecutar en el CPU en el tiempo {env.now}")
            yield env.timeout(1)  # Simulamos que el CPU ejecuta 3 instrucciones en 1 unidad de tiempo
            instrucciones_pendientes -= instrucciones_a_ejecutar
            print(f"{nombre} ejecuta {instrucciones_a_ejecutar} instrucciones. {instrucciones_pendientes} instrucciones pendientes en el tiempo {env.now}")
            
            # Verificamos si el proceso ha terminado o si debe esperar por I/O
            if instrucciones_pendientes <= 0:
                print(f"{nombre} ha terminado en el tiempo {env.now}")
                break
            else:
                # Determinamos si el proceso espera por I/O
                io_event = random.randint(1, 21)
                if io_event == 1:
                    print(f"{nombre} debe esperar por I/O en el tiempo {env.now}")
                    yield env.timeout(1)  # Simulamos el tiempo de espera por I/O
                    print(f"{nombre} ha regresado de I/O en el tiempo {env.now}")
                elif io_event == 2:
                    print(f"{nombre} vuelve a la cola de ready en el tiempo {env.now}")

    # Se devuelve la memoria RAM utilizada al finalizar el proceso
    yield RAM.put(memoria_necesaria)
    print(f"{nombre} devuelve {memoria_necesaria} de memoria RAM en el tiempo {env.now}")

# Configuración de la simulación
env = simpy.Environment()

# Memoria RAM
RAM = simpy.Container(env, init=100, capacity=100)

# CPU
CPU = simpy.Resource(env, capacity=1)

# Creamos procesos de forma exponencial con intervalo de 10
intervalo_llegada = 10
env.process(proceso(env, "Proceso-1", RAM, CPU))
env.process(proceso(env, "Proceso-2", RAM, CPU))
env.process(proceso(env, "Proceso-3", RAM, CPU))

# Ejecutamos la simulación
env.run(until=50)  # Simulamos hasta el tiempo 50