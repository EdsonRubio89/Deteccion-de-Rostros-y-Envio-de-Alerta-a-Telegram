# Deteccion-de-Rostros-y-Envio-de-Alerta-a-Telegram

Sistema de deteccion de rostros mediante Open CV, Modelo y Envio de Alertas (Texto e Imagen) a Telegram

A continuación les comparto un programa en Python que realiza deteccion de rostros en tiempo real, al detectar un rostro se envia un mensaje de texto personalizable acompañado de la imagen detectada al momento de la detección, se puede configurar la frecuencia en la cual se envian los mensajes. Las imagenes se guardan con fecha y hora sobre la misma, asi como con el rostro encerrado dentro de un rectangulo y el % de confianza de que lo que se detecto en verdad es un rostro.

De forma paralela se guardan en la computadora las imagenes en formato .jpg obtenidas en la cerpeta "face_detected".

Para probar el programa es necesario crear un bot en telegram y agregar en el archivo data.py los valores del token y chat id correspondientes, este puede funcionar de forma independiente o agregar al bot a un grupo, esto para que las notificaciones puedan ser visualizadas por varias personas al mismo tiempo. Les comparto el link donde se explica el proceso de configuracion del bot. 
https://platzi.com/blog/bot-python/

