import simpy
import random
import matplotlib.pyplot as plt
import statistics as stat



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
    
def ready(isReady):
  isReady.setRam(random.randint(1, 10))
  isReady.setInst(random.randint(1, 10))

def running(CPU):
  InstCant=CPU.getInst()
  if(InstCant<=6):
    CPU.setInst(0)
  else:
    CPU.setInst(CPU.getInst()-6)
    
  if(CPU.getInst()==0):
    return True
  return False

  

def Procesar(proceso, name,  RAM, CPU, cpu_time):
  global tiempo_total

  initial_time = env.now

  #obtener RAM
  yield env.timeout(random.expovariate(1.0/10))
  print('%s create at %d'%(name, env.now))
  ready(proceso)
  yield RAM.get(proceso.getRam())  
  print('%s using %d of RAM at %d'%(name,proceso.getRam(), env.now))
  finished = False
  waitingStatus=0
  while (not finished):
    print('%s is ready at %d' % (name, env.now))
    with CPU.request() as req:
      yield req
      print('%s is running at %d' % (name, env.now))
      yield env.timeout(cpu_time)
      print('%s is leaving the CPU at %d' % (name, env.now))

    finished= running(proceso)

    #Decisión de estado
    if(not finished):
      waitingStatus=random.randint(1,2)
      if(waitingStatus==1):
        print('%s is entering waiting at %d' %(name, env.now))
        yield env.timeout(1)
        print('%s is leaving waiting at %d' % (name, env.now))
    else:
      RAM.put(proceso.getRam())
      print('%s is terminated at %d' % (name, env.now))
      finish_time = env.now
      tiempo_total = tiempo_total + (finish_time - initial_time)
     

random.seed(10)
cantidad = 25
length = [25, 50, 100, 150, 200]
times = []
for cantidad in length:
  tiempo_total = 0
  env = simpy.Environment()
  RAM = simpy.Container(env,init=200,capacity=200)
  CPU = simpy.Resource(env, capacity = 2)
  for i in range(cantidad):
    proceso = Proceso()
    env.process(Procesar(proceso, 'Process %d' % i ,RAM, CPU, 1))
  
  env.run()
  times.append(tiempo_total/cantidad)


print("Tiempos", times)

print("La desviacion estandar es:", stat.stdev(times))
plt.plot(length, times)
plt.ylabel('Tiempo promedio')
plt.xlabel("Cantidad de procesos")
plt.show()