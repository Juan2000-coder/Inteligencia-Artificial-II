Los nombres siguen este orden
[Funcion a aproximar]_[Funcion de activacion]_[Learning rate utilizado]_[Epochs]_[N de neuronas en la capa oculta]

El panchotron solo puede tener una capa, con las neuronas que se quieran.

El excel del seno es para la grafica que dice "menos_dispersion"

En la carpeta "Relu" hay graficas para distintos n de neuronas. Observar como se va quebrando más a medida que aumentan.

Para la cuadratica, a 50 iteraciones, la mejor funcion es swish. Puede ser que a mas iteraciones esto cambie, pero no lo hice porque iba a estar 1000 años.

Para la seno, con mucha dispersion, ninguna se ajusta muy bien (underfitting). Con menos dispersion, la tanh es la mejor. Es posible que para ajustar con mas dispersion haya que hacer mas capas. El panchotron3 era para eso pero no me salio xd.


