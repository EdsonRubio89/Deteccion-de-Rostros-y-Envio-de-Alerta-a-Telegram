# Importamos las librerias
import cv2
from urllib.request import urlopen
import requests
import threading
from data import token
from data import chat_id
import time

def hour():#Extraemos hora que se estara mostrando en imagenes guardadas y en el frame de video
    now = time.time()
    dia=time.strftime("%d", time.localtime(now))
    mes=time.strftime("%m", time.localtime(now))
    anio=time.strftime("%Y", time.localtime(now))
    hora=time.strftime("%H", time.localtime(now))
    minuto=time.strftime("%M", time.localtime(now))
    segundo=time.strftime("%S", time.localtime(now))
    return dia+"/"+mes+"/"+anio+" "+hora+":"+minuto+":"+segundo

def alerta(img):#Funcion que envia mensaje de texto e imagen a grupo de telegram mediante bot
    text="ATENCION: Rostro Detectado"
    txt = text.replace(" ", "%20")
    r = urlopen("https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+chat_id+"&parse_mode=Markdown&text="+txt)
    r.close()# Cerrar para liberar recursos.
    print("** ALERTA DE INTRUSION ** - Rostro Detectado")
    print("Mensaje De Alerta Enviado al Celular de Edson Rubio\n")
    url = f'https://api.telegram.org/bot'+token+'/sendPhoto'
    files = {'photo': open('./face_detected/rostro_'+str(img)+'.jpg', 'rb')}
    data = {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    response.close()# Cerrar para liberar recursos.

cap = cv2.VideoCapture(0)# Realizamos VideoCaptura
net = cv2.dnn.readNetFromCaffe("opencv_face_detector.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")# Leemos el modelo

# Parametros del modelo
anchonet = 300
altonet = 300
# Valores medios de los canales de color
media = [104, 117, 123]
umbral = 0.7
y=0
img=0

# Empezamos
while True:
    # Leemos los frames
    ret, frame = cap.read()
    # Si hay error
    if not ret:
        break

    frame = cv2.flip(frame, 1) # Realizamos conversion de forma
    # Extraemos info de los frames
    altoframe = frame.shape[0]
    anchoframe = frame.shape[1]
    # Preprocesamos la imagen
    # Images - Factor de escala - tamaño - media de color - Formato de color(BGR-RGB) - Recorte
    blob = cv2.dnn.blobFromImage(frame, 1.0, (anchonet, altonet), media, swapRB = False, crop = False)
    # Corremos el modelo
    net.setInput(blob)
    detecciones = net.forward()

    # Iteramos  #8 frames x segundo 
    for i in range(detecciones.shape[2]):
        # Extraemos la confianza de esa deteccion
        conf_detect = detecciones[0,0,i,2]
        # Si superamos el umbral (70% de probabilidad de que sea un rostro)
        if conf_detect > umbral:
            # Extraemos las coordenadas
            xmin = int(detecciones[0, 0, i, 3] * anchoframe)
            ymin = int(detecciones[0, 0, i, 4] * altoframe)
            xmax = int(detecciones[0, 0, i, 5] * anchoframe)
            ymax = int(detecciones[0, 0, i, 6] * altoframe)
            # Dibujamos el rectangulo
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0,0,255), 2)
            # Texto que vamos a mostrar
            label = "ROSTRO DETECTADO: %.4f" % conf_detect
            # Tamaño del fondo del label
            label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            # Colocamos fondo al texto
            cv2.rectangle(frame, (xmin, ymin - label_size[1]), (xmin + label_size[0], ymin + base_line),(0,0,0), cv2.FILLED)
            # Colocamps el texto
            cv2.putText(frame, label, (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
            #Colocamos la hora
            cadena_hora=hour()
            cv2.putText(frame, cadena_hora, (8, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
            
            if y==0:#Guarda cada 3 segundo una imagen cuando se detecta rostro en carpeta
                cv2.imwrite(f'./face_detected/rostro_{img}.jpg', frame)
                #Se abre un hilo nuevo para ejecutar de forma paralela el envio de mensajes a telegram, esto para no afectar la velocidad del programa principal
                t=threading.Thread(target=alerta, args=(img,))
                t.start()#inicia hilo
                img+=1#contador para guardar imagnes con nombre diferente

            y=y+1#Contador de frames
            resend_alert=3#segundos de espera para reenviar nuevamente la alerta, tomando en cuenta los 8FPS

            if y==(resend_alert*8):y=0

    cv2.imshow("DETECCION DE ROSTROS", frame)#muestra frame en tiempo real

    t = cv2.waitKey(1)
    if t == 27:#Al presionar ESC sale del proceso
        break

cv2.destroyAllWindows()
cap.release()
