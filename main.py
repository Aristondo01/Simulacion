import simpy
import random
#import matplotlib.pyplot as plt
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
    
  

