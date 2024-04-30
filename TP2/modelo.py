import numpy as np

class Habitacion:
  def __init__(self, _tau):
    
    self.tau = _tau
    

  """
  Función que calcula la tasa de cambio de la temperatura interna respecto al tiempo (_t).

  Argumentos:
  _t: Tiempo.
  _tempI: Temperatura interna.
  _tempE: Temperatura externa.
  _porcentaje: Porcentaje.

  Retorna:
  Tasa de cambio de la temperatura interna respecto al tiempo (_t).
  """
  def f(self, _t, _tempI,_tempE, _porcentaje):
      """
      Ecuación diferencial: dy/dx = x - y
      """
      return (_tempE - _tempI)/(self.tau*(1.1 - (0.1*_porcentaje/100)))

  """
  Método de Runge-Kutta de cuarto orden para resolver EDOs.

  Argumentos:
  _tA: Tiempo.
  _tempIA: Temperatura inicial.
  h: Paso del tiempo.
  _tempE: Temperatura externa.
  _porcentaje: Porcentaje.

  Retorna:
  Aproximación de la temperatura siguiente utilizando el método de Runge-Kutta de cuarto orden.
  """
  def runge_kutta_4(self, _tA, _tempIA, h,_tempE, _porcentaje):
      """
      Método de Runge-Kutta de cuarto orden para resolver EDOs.
      """
      k1 = h * self.f(_tA, _tempIA, _tempE, _porcentaje)
      k2 = h * self.f(_tA + h/2, _tempIA + k1/2, _tempE, _porcentaje)
      k3 = h * self.f(_tA + h/2, _tempIA + k2/2, _tempE, _porcentaje)
      k4 = h * self.f(_tA + h, _tempIA + k3, _tempE, _porcentaje)
      tempInext = _tempIA + (k1 + 2*k2 + 2*k3 + k4) / 6
      return tempInext