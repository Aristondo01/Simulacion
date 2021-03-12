"""
Sebastian Aristondo 20880
Daniel Gonzalez Carrillo 20293

Modificacion: 12/03/2021

Descripcion:
  Programa que realiza una simulacion de la ejecucion
  de instrucciones por parte de un sistema operativo.
"""



import simpy
import random
import matplotlib.pyplot as plt
import statistics as stat


#Clase que permite instancias de procesos que
#ingresan en la simulacion.
class Proceso():

  def __init__(self):
    self.Ram = 0
    self.Instrucciones = 0

  def setRam(self,valor):
    self.Ram=valor

  def getRam(self):
    return self.Ram
  
  def setInst(self, valor):
    self.Instrucciones=valor

  def getInst(self):
    return self.Instrucciones  

#Metodo que permite definir la cantidad de RAM y de instrucciones de cada proceso.
def ready(isReady):
  isReady.setRam(random.randint(1, 10))
  isReady.setInst(random.randint(1, 10))

#Metodo que permite restar instrucciones faltantes a los procesos.
def running(CPU):
  InstCant=CPU.getInst()
  if(InstCant<=6):
    CPU.setInst(0)
  else:
    CPU.setInst(CPU.getInst()-6)
    
  if(CPU.getInst()==0):
    return True
  return False

  
#Metodo que permite realizar la simulacion.
def Procesar(proceso, name,  RAM, CPU, cpu_time):
  global tiempo_total

  initial_time = env.now

  #Se espera un tiempo para generar el proceso.
  yield env.timeout(random.expovariate(1.0/10))
  print('%s create at %d'%(name, env.now))
  ready(proceso)

  #Se asigna RAM al proceso.
  yield RAM.get(proceso.getRam())  
  print('%s using %d of RAM at %d'%(name,proceso.getRam(), env.now))
  finished = False
  waitingStatus=0
  while (not finished):
    print('%s is ready at %d' % (name, env.now))
    #Se ingresa al CPU.
    with CPU.request() as req:
      yield req
      print('%s is running at %d' % (name, env.now))
      yield env.timeout(cpu_time)
      print('%s is leaving the CPU at %d' % (name, env.now))

    finished= running(proceso)

    #Decisión de estado
    if(not finished):
      waitingStatus=random.randint(1,2)
      #Se ingresa a Waiting
      if(waitingStatus==1):
        print('%s is entering waiting at %d' %(name, env.now))
        yield env.timeout(1)
        print('%s is leaving waiting at %d' % (name, env.now))
    else:
      #Se termina el proceso cuando no quedan instrucciones y se devuelve la RAM.
      RAM.put(proceso.getRam())
      print('%s is terminated at %d' % (name, env.now))
      finish_time = env.now
      tiempo_total = tiempo_total + (finish_time - initial_time)
     

random.seed(10)
cantidad = 25
length = [25, 50, 100, 150, 200]
times = []

#Se realiza un ciclo para crear una simulacion para cierta cantidad de procesos.
for cantidad in length:
  tiempo_total = 0
  #Se definen los recursos a usar.
  env = simpy.Environment()
  RAM = simpy.Container(env,init=200,capacity=200)
  CPU = simpy.Resource(env, capacity = 2)
  for i in range(cantidad):
    proceso = Proceso()
    env.process(Procesar(proceso, 'Process %d' % i ,RAM, CPU, 1))
  
  #Se corre la simulacion
  env.run()
  times.append(tiempo_total/cantidad)

#Tiempos promedio
for i in range(len(times)):
  print("Tiempo promedio de %s procesos %s" % (length[i], round(times[i], 2)))

#Desviacion estandar de tiempos.
print("La desviacion estandar es:", stat.stdev(times))

#Grafica de los tiempos promedio.
plt.plot(length, times)
plt.ylabel('Tiempo promedio')
plt.xlabel("Cantidad de procesos")
plt.show()