# Teoria_de-la_informacion_Val
#ESQUEMA DE COMUNICACIÓN TELEGRÁFO 3ER PARCIAL

En el código "esquema_comunicación3er_parcial" hacemos implementación de la comunicación Morse utilizando técnicas de compresión Huffman y su transmisión a través de canales telegráficos simulados. El proceso implica la conversión de un mensaje de texto a Morse, la división de los datos en paquetes (palabras Morse) y la aplicación de compresión Huffman para optimizar la transmisión. Además, se simula un canal telegráfico para transmitir los paquetes, con la introducción de un handshake y hash para garantizar la integridad de los datos.
Primero pasamos nuestro mensaje de texto a morse para posteriormente comprimilos en Huffman, cada palabra morse se convierte en una representación binaria del mismo y se calcula su hash de cada "paquete" o en este caso de cada palabra. Uno de nuestros problemas es que trataba el mensaje como un solo elemento en vez de segmentar el contenido del mensaje, por ello introdujimos un "SALT" aleatorio para calcular el hash. Simulamos un canal telegráfico, la transmisión de datos se simula mediante la división del mensaje en segmentos, cada uno representando una palabra Morse y creamos múltiples canales telefráficos para la transmisión de esos segmentos, posteriormente se implementa una búsqueda binaria en el handshake para encontrar el valor original del hash. Algunos de los problemas que mencionamos es que repetía el valor de los hashes ya que trataba el mensaje como un solo paquete por ello modificamos el código para que segmentara cada palabra del mensaje como un paquete independiente. 


Se calcula la entropía para evaluar la eficiencia de la transmisión en cada canal telegráfico simulado.
El propósito de este esquema es explicar de manera más detallada el sistema de comunicación que vamos a desarrollar el cuál será 
un sistema de comunicación de un telegráfo.
Para ello vamos a dividir nuestro esquema de comunicacion de la siguiente forma
CARGA DE LA INFORMACIÓN: Nuestra fuente de información será un archivo .txt 
TRANSMISOR: Nuestro transmisor será el telegrafo por el cuál se enviará el mensaje
el mensaje de texto a morse
CANAL: Nuestro canal será un "cable de cobre" el cuál permite pulsaciones bajas y altas que es dónde se encripta el mensaje 
en morse y será enviado a nuestro receptor también en esta parte se le añadirá ruido al programa.
RECEPTOR: El receptor recibe el mensaje en morse con ruido 
MENSAJE: Se genera un archivo .wav, que contiene el audio del código morse


![image](https://github.com/ValeriaG29/Teoria_de-la_informacion_Val/assets/54336086/b2ba4a1a-6550-4bd9-b54f-1105fe08c716)

