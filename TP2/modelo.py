import numpy as np

class Habitacion:
  def __init__(self, , _tau):
    
    self.tau = _tau
    

  def f(self, _t, _tempI,_tempE, _porcentaje):
      """
      Ecuación diferencial: dy/dx = x - y
      """
      return (_tempE - _tempI)/(self.tau*(1.1 - (0.1*_porcentaje/100)))

  def runge_kutta_4(self, _tA, _tempIA, h,_tempE, _porcentaje):
      """
      Método de Runge-Kutta de cuarto orden para resolver EDOs.
      """
      k1 = h * self.f(x, y, _tempE, _porcentaje)
      k2 = h * self.f(x + h/2, y + k1/2, _tempE, _porcentaje)
      k3 = h * self.f(x + h/2, y + k2/2, _tempE, _porcentaje)
      k4 = h * self.f(x + h, y + k3, _tempE, _porcentaje)
      y_next = y + (k1 + 2*k2 + 2*k3 + k4) / 6
      return y_next

  # Valores iniciales
  y = 1
  h = 0.1  # Tamaño del paso

  # Simulación de datos en tiempo real (vector de datos)
  x_data = np.linspace(0, 10, 100)  # Ejemplo: vector de datos de x

  # Bucle para iterar sobre el vector de datos en tiempo real
  for x_new_data in x_data:
      # Actualizar y usando el método de Runge-Kutta
      y = runge_kutta_4(x_new_data, y, h)
      # Imprimir el resultado
      print(f"Valor de x: {x_new_data}, Valor de y: {y}")
      
  
 