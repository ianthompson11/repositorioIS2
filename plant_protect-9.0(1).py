import os
import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import cv2
import pyodbc
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import serial
import time
import threading
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import matplotlib.pyplot as plt
import pandas as pd
import pyodbc
import os
import socket

# Define la carpeta y el nombre del archivo *************MODIFICACIONES PARA QUE GUARDE DETECCIONES
 
print("esto es un cambio")
verificador = 0
screen_size = "1200x600"
#verde_oliva = '#6b8e23'
verde_oliva = '#DAD420'
marron_siena = '#8b4513'
verde_claro = '#F8F497'
verde_letras = '#5D740E'
boton_width = 20
boton_height = 1
width_principal = 636
height_principal = 387
chocolate = "#241E1F"
print("Nueva Version")
cam_running = False
cap = None  # Añadido para manejar la captura globalmente




numero_planta = 0
port = 'COM4'
hostname = socket.gethostname()

local_path = os.getcwd()
actividades_path = os.path.join(local_path, 'actividades')

def get_screen_params():
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Ajuste automático de dimensiones en función del tamaño de la pantalla
    screen_size = f"{screen_width}x{screen_height}"
    desired_width = int(screen_width )  # 75% del ancho de la pantalla
    desired_height = int(screen_height)  # 75% de la altura de la pantalla
    width_principal = int(desired_width * 0.4)  # 40% del ancho deseado
    height_principal = int(desired_height * 0.4)  # 40% de la altura deseada

    # Definir el servidor en función de la pantalla o cualquier otra lógica
    root.destroy()
    
    return screen_size, desired_width, desired_height, width_principal, height_principal


# Llamar a la función para obtener los parámetros
screen_size, desired_width, desired_height, width_principal, height_principal = get_screen_params()

print(screen_size, desired_width, desired_height, width_principal, height_principal)



server = server = hostname + '\\SQLEXPRESS'
'''if(pc == 1):
    server = 'MrT\\SQLEXPRESS'
elif(pc == 2):
    server = 'Ianth11\\SQLEXPRESS'
else:
    server = 'MRTHOMPSON\\SQLEXPRESS'
'''


detecciones_path = os.path.join(actividades_path, 'detecciones')
web_images_path = os.path.join(actividades_path, 'web_images')
fotos_path = os.path.join(actividades_path, 'Fotos')
ventana_secundaria_1_path = os.path.join(actividades_path, 'ventana_secundaria_1')
graficas_path = os.path.join(actividades_path, 'graficas')
ventana_inicial_path = os.path.join(actividades_path, 'ventana_inicial')


# Variable global para controlar el estado de la cámara
OUTPUT_FOLDER = os.path.join(actividades_path, 'Fotos')
# Asegúrate de que la carpeta exista
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)


  # Reemplaza con la ruta de tu carpeta
if not os.path.exists(actividades_path):
    os.makedirs(detecciones_path, web_images_path, fotos_path)  # Crea la carpeta si no existe

file_path = os.path.join(detecciones_path, 'detections.jpg')

# Configura el puerto serie
arduino_port = "COM4"  # Cambia esto al puerto que utiliza tu Arduino
baudrate = 9600

# Variables globales
current_photo_path = None
max_score_class_name = '' #variable que da el nombre de la deteccion en perform_detections



class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Plant Protect")
        self.geometry(screen_size)

        self.attributes("-fullscreen", True)  # substitute `Tk` for whatever your `Tk()` object is called

        self.bind("<Escape>", self.end_fullscreen)

        self.ventana_actual = None
        self.mostrar_ventana_inicial()

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)
        return "break"

    def mostrar_ventana_inicial(self):
        if self.ventana_actual:
            self.ventana_actual.destroy()

        self.ventana_actual = VentanaInicial(self)
        self.ventana_actual.pack(fill=tk.BOTH, expand=True)

    def mostrar_ventana_secundaria(self):
        if self.ventana_actual:
            self.ventana_actual.destroy()

        self.ventana_actual = VentanaSecundaria(self)
        self.ventana_actual.pack(fill=tk.BOTH, expand=True)

    def mostrar_ventana_terciaria(self):
        if self.ventana_actual:
            self.ventana_actual.destroy()

        self.ventana_actual = VentanaTerciaria(self)
        self.ventana_actual.pack(fill=tk.BOTH, expand=True)

    def mostrar_ventana_terciaria_alternativa(self):
        if self.ventana_actual:
            self.ventana_actual.destroy()

        self.ventana_actual = VentanaTerciariaAlternativa(self)
        self.ventana_actual.pack(fill=tk.BOTH, expand=True)    

 
    def mostrar_ventana_secundaria_1(self):
        if self.ventana_actual:
            self.ventana_actual.destroy()

        self.ventana_actual = ventana_secundaria_1(self)
        self.ventana_actual.pack(fill=tk.BOTH, expand=True)

    def mostrar_ventana_secundaria_2(self):

        if self.ventana_actual:
            self.ventana_actual.destroy()

        self.ventana_actual = ventana_secundaria_2(self)
        self.ventana_actual.pack(fill=tk.BOTH, expand=True)

    def mostrar_ventana_botones_plantas(self):

        if self.ventana_actual:
            self.ventana_actual.destroy()

        self.ventana_actual = ventana_botones_plantas(self)
        self.ventana_actual.pack(fill=tk.BOTH, expand=True)

    def mostrar_ventana_datos_plantas(self):

        if self.ventana_actual:
            self.ventana_actual.destroy()

        self.ventana_actual = Ventana_datos_plantas(self)
        self.ventana_actual.pack(fill=tk.BOTH, expand=True)

    def mostrar_ventana_cuidado_plantas(self):
        

        if self.ventana_actual:
            self.ventana_actual.destroy()

        self.ventana_actual = Ventana_cuidado_plantas(self)
        self.ventana_actual.pack(fill=tk.BOTH, expand=True)

    def mostrar_ventana_detecciones(self):

        if self.ventana_actual:
            self.ventana_actual.destroy()

        self.ventana_actual = Ventana_detecciones(self)
        self.ventana_actual.pack(fill=tk.BOTH, expand=True)


    def mostrar_ventana_graficas(self):

        if self.ventana_actual:
            self.ventana_actual.destroy()

        self.ventana_actual = Ventana_Graficas(self)
        self.ventana_actual.pack(fill=tk.BOTH, expand=True)

class VentanaInicial(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent  # Guarda la referencia al padre
        print("Ventana inicial")

        # Font styles
        font_style_titulo = ("Aptos (Body)", 25, "bold")
        font_style_boton = ("Aptos (Body)", 18, "bold")

        image1_path = os.path.join(ventana_inicial_path, 'image1.jpg')

        # Carga las imágenes redimensionadas
        img2 = self.load_image(image1_path, desired_width, desired_height)

        # Crea widgets de etiqueta para mostrar las imágenes y guarda la referencia de la imagen
        self.label1 = tk.Label(self, image=img2, bd=0)
        self.label1.image = img2  # Mantén una referencia a la imagen
        self.label1.grid(row=0, column=0)  # Coloca la primera imagen en la fila 0, columna 0

        self.frame_principal = tk.Frame(self, width=width_principal, height=height_principal, bg=verde_oliva)
        self.frame_principal.grid(row=0, column=0)  # Colocar el frame en la ventana principal usando grid

        self.frame_principal.grid_propagate(False)
        width, height, radius = 300, 50, 25 #actualmente es 25

        rounded_button_image = self.create_rounded_button_image(width, height, radius, verde_claro)
        button_image_tk = ImageTk.PhotoImage(rounded_button_image)

        # Definir el layout del frame
        self.frame_principal.grid_rowconfigure(0, weight=1)
        self.frame_principal.grid_columnconfigure(0, weight=1)

        self.label = tk.Label(self.frame_principal, text="PLANT PROTECT", font=font_style_titulo, bg=verde_oliva, fg=verde_letras, compound = "center")
        self.label.grid(row=0, column=0, pady=10)  # Ajustar el sticky a 'n' para que se alinee arriba

        # Crear botón con la imagen de fondo
        boton_ir_secundaria = tk.Button(self.frame_principal, activebackground=verde_oliva , image=button_image_tk, text="CUIDADO DE PLANTAS", compound="center", fg=verde_letras, font=font_style_boton, borderwidth=0, highlightthickness=0, command=parent.mostrar_ventana_secundaria, bg = verde_oliva)
        boton_ir_secundaria.grid(row=1, column=0, pady=10, sticky='n')
        boton_ir_secundaria.image = button_image_tk  # Mantener la referencia a la imagen


        boton_adicional_inicial = tk.Button(self.frame_principal,activebackground=verde_oliva , image=button_image_tk, text="DATOS DE PLANTAS", compound="center", fg=verde_letras, font=font_style_boton, borderwidth=0, highlightthickness=0, command=parent.mostrar_ventana_botones_plantas, bg = verde_oliva)
        boton_adicional_inicial.grid(row=2, column=0, pady=10, sticky='n')
        boton_adicional_inicial.image = button_image_tk  # Mantener la referencia a la imagen

        boton_deteccion = tk.Button(self.frame_principal,activebackground=verde_oliva , image=button_image_tk, text="DETECCION", compound="center", fg=verde_letras, font=font_style_boton, borderwidth=0, highlightthickness=0, command=parent.mostrar_ventana_detecciones, bg = verde_oliva)
        boton_deteccion.grid(row=3, column=0, pady=10, sticky='n')
        boton_deteccion.image = button_image_tk  # Mantener la referencia a la imagen

        boton_ver_sensores = tk.Button(self.frame_principal, activebackground=verde_oliva ,image=button_image_tk, text="VER SENSORES", compound="center", fg=verde_letras, font=font_style_boton, borderwidth=0, highlightthickness=0, command=parent.mostrar_ventana_secundaria_1, bg = verde_oliva)
        boton_ver_sensores.grid(row=4, column=0, pady=10, sticky='n')
        boton_ver_sensores.image = button_image_tk  # Mantener la referencia a la imagen

    def load_image(self, path, width, height):
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el archivo: {path}")
        image = Image.open(path)
        image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    def create_rounded_button_image(self, width, height, radius, color):
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Dibuja un rectángulo redondeado
        draw.rounded_rectangle((0, 0, width, height), radius, fill=color)

        return image
    
class Ventana_detecciones(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.cap = None
        self.cam_running = False
        print("Ventana detecciones")

        # Font styles
        font_style_titulo = ("Aptos (Body)", 25, "bold")
        font_style_boton = ("Aptos (Body)", 18, "bold")

        image4_path = os.path.join(ventana_inicial_path, 'image4.jpg')

        width, height, radius = 300, 50, 25 #actualmente es 25

        rounded_button_image = self.create_rounded_button_image(width, height, radius, verde_claro)
        button_image_tk = ImageTk.PhotoImage(rounded_button_image)


        # Carga las imágenes redimensionadas
        img2 = self.load_image(image4_path, desired_width, desired_height)

        # Crea widgets de etiqueta para mostrar las imágenes y guarda la referencia de la imagen
        self.label1 = tk.Label(self, image=img2, bd=0)
        self.label1.image = img2  # Mantén una referencia a la imagen
        self.label1.grid(row=0, column=0)  # Coloca la primera imagen en la fila 0, columna 0

        self.video_frame = tk.Frame(self, width=700, height=700, bg=chocolate)
        self.video_frame.grid(row=0, column=0)  # Colocar el frame en la ventana principal usando grid

        self.video_frame.grid_propagate(False)

        # Definir el layout del frame
        self.video_frame.grid_rowconfigure(0, weight=1)
        self.video_frame.grid_columnconfigure(0, weight=1)

        # Create a label to display the video feed
        self.video_label = tk.Label(self.video_frame,compound="center", bg =chocolate)
        self.video_label.grid(row=0, column=0)  # Colocar el frame en la ventana principal usando grid
        
        start_button = tk.Button(self.video_frame, activebackground=chocolate, image=button_image_tk, text="Start Camera", compound="center", fg=chocolate, font=font_style_boton, borderwidth=0, highlightthickness=0, command=self.start_cam, bg = chocolate)
        start_button.grid(row=1, column=0, pady=10, sticky='n')
        start_button.image = button_image_tk  # Mantener la referencia a la imagen

        stop_button = tk.Button(self.video_frame,activebackground=chocolate, image=button_image_tk, text="Stop Camera", compound="center", fg=chocolate, font=font_style_boton, borderwidth=0, highlightthickness=0, command=self.stop_cam, bg = chocolate)
        stop_button.grid(row=2, column=0, pady=10, sticky='n')
        stop_button.image = button_image_tk  # Mantener la referencia a la imagen

        back_button = tk.Button(self.video_frame,activebackground=chocolate, image=button_image_tk, text="Atras", compound="center", fg=chocolate, font=font_style_boton, borderwidth=0, highlightthickness=0, command=parent.mostrar_ventana_inicial, bg = chocolate)
        back_button.grid(row=3, column=0, pady=10, sticky='n')
        back_button.image = button_image_tk  # Mantener la referencia a la imagen

    def load_image(self, path, width, height):
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el archivo: {path}")
        image = Image.open(path)
        image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    
    def create_rounded_button_image(self, width, height, radius, color):
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Dibuja un rectángulo redondeado
        draw.rounded_rectangle((0, 0, width, height), radius, fill=color)

        return image

    def start_cam(self):
        if self.cam_running:
            return

        self.cam_running = True
        self.cap = cv2.VideoCapture(0)
        self.show_frame()

    def show_frame(self):
        global detect_fn, category_index

        if not self.cam_running or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        image_np = np.array(frame)

        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
        detections = detect_fn(input_tensor)

        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
        detections['num_detections'] = num_detections

        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        label_id_offset = 1
        image_np_with_detections = image_np.copy()

        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'],
            detections['detection_classes'] + label_id_offset,
            detections['detection_scores'],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=5,
            min_score_thresh=.8,
            agnostic_mode=False
        )

        # Convert the image from OpenCV format to PIL format
        image_pil = Image.fromarray(cv2.cvtColor(image_np_with_detections, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=image_pil)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        # Schedule the next frame
        self.video_label.after(10, self.show_frame)

    def stop_cam(self):
        self.cam_running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

class VentanaSecundaria(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent  # Guarda la referencia al padre
        print("Ventana secundaria")


        font_style_titulo = ("Helvetica", 20, "bold")
        font_style_boton = ("Helvetica", 15, "bold")

        image1_path = os.path.join(ventana_inicial_path, 'image1.jpg')

        # Carga las imágenes redimensionadas
        img2 = self.load_image(image1_path, desired_width, desired_height)

        # Crea widgets de etiqueta para mostrar las imágenes y guarda la referencia de la imagen
        self.label1 = tk.Label(self, image=img2, bd=0)
        self.label1.image = img2  # Mantén una referencia a la imagen
        self.label1.grid(row=0, column=0)  # Coloca la primera imagen en la fila 0, columna 0

        #verde_oliva = "#808000"  # Definir el color verde oliva
        self.frame_principal = tk.Frame(self, width=width_principal, height=height_principal, bg=verde_oliva)
        self.frame_principal.grid(row=0, column=0)  # Colocar el frame en la ventana principal usando grid

        self.frame_principal.grid_propagate(False)

        # Definir el layout del frame
        self.frame_principal.grid_rowconfigure(0, weight=1)
        self.frame_principal.grid_rowconfigure(0, weight=0)  # Eliminar el peso en la fila 0
        self.frame_principal.grid_columnconfigure(0, weight=1)

        self.label = tk.Label(self.frame_principal, text="¿Desea tomar foto?", font=font_style_titulo, bg=verde_oliva, fg=verde_letras)
        self.label.grid(row=0, column=0, pady=10, sticky='n')  # Ajustar el sticky a 'n' para que se alinee arriba

        width, height, radius = 300, 50, 25 #actualmente es 25

        rounded_button_image = self.create_rounded_button_image(width, height, radius, verde_claro)
        button_image_tk = ImageTk.PhotoImage(rounded_button_image)

        boton_seleccionar = tk.Button(
            self.frame_principal,
            image=button_image_tk,
            activebackground=verde_oliva,
            text="Buscar Foto",
            compound="center",
            fg=verde_letras,
            font=font_style_boton,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.seleccionar_imagen(parent),  # Pasa la función como referencia con lambda
            bg=verde_oliva
        )
        
        boton_seleccionar.grid(row=2, column=0, pady=10, sticky='n')
        boton_seleccionar.image = button_image_tk  # Mantener la referencia a la imagen


        boton_atras = tk.Button(self.frame_principal,activebackground=verde_oliva, image=button_image_tk, text="Atras", compound="center", fg=verde_letras, font=font_style_boton, borderwidth=0, highlightthickness=0, command=parent.mostrar_ventana_inicial, bg = verde_oliva)
        boton_atras.grid(row=3, column=0, pady=10, sticky='n')
        boton_atras.image = button_image_tk  # Mantener la referencia a la imagen

    def seleccionar_imagen(self, parent):

        ruta_imagen = filedialog.askopenfilename(
        
            initialdir=local_path,
            title="Seleccionar imagen",
            filetypes=(("Archivos de imagen", "*.jpg *.jpeg *.png *.gif"), ("todos los archivos", "*.*"))
        )

        if ruta_imagen:
            # Cargar la imagen con Pillow
            imagen_seleccionada = Image.open(ruta_imagen)
            extension = os.path.splitext(ruta_imagen)[1]  # Obtener la extensión del archivo original
            nueva_ruta = os.path.join(fotos_path, "foto" + extension)          
            imagen_seleccionada.save(nueva_ruta)

            # Convertir a formato compatible con Tkinter
            imagen_tk = ImageTk.PhotoImage(imagen_seleccionada)
            parent.mostrar_ventana_terciaria_alternativa()


    def create_rounded_button_image(self, width, height, radius, color):
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Dibuja un rectángulo redondeado
        draw.rounded_rectangle((0, 0, width, height), radius, fill=color)

        return image

    def load_image(self, path, width, height):
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el archivo: {path}")
        image = Image.open(path)
        image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)


class VentanaTerciaria(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent  # Guarda la referencia al padre
        print("Ventana terciaria")

        font_style_titulo = ("Helvetica", 20, "bold")
        font_style_boton = ("Helvetica", 15, "bold")

        image4_path = os.path.join(ventana_inicial_path, 'image4.jpg')



        # Carga las imágenes redimensionadas
        img2 = self.load_image(image4_path, desired_width, desired_height)
        

        # Crea widgets de etiqueta para mostrar las imágenes y guarda la referencia de la imagen
        self.label1 = tk.Label(self, image=img2, bd=0)
        self.label1.image = img2  # Mantén una referencia a la imagen
        self.label1.grid(row=0, column=0)  # Coloca la primera imagen en la fila 0, columna 0

        
        self.frame_principal = tk.Frame(self, width=700, height=700, bg=chocolate)
        self.frame_principal.grid(row=0, column=0)  # Colocar el frame en la ventana principal usando grid

        self.frame_principal.grid_propagate(False)

        # Definir el layout del frame
        self.frame_principal.grid_rowconfigure(0, weight=1)
        self.frame_principal.grid_rowconfigure(0, weight=0)  # Eliminar el peso en la fila 0
        self.frame_principal.grid_columnconfigure(0, weight=1)


        self.label = tk.Label(self.frame_principal, text="¿Desea usar esta Foto?", font=font_style_titulo, bg=chocolate, fg=verde_claro)
        self.label.grid(row=0, column=0, pady=10, sticky='n')  # Ajustar el sticky a 'n' para que se alinee arriba


        width, height, radius = 300, 50, 25 #actualmente es 25

        rounded_button_image = self.create_rounded_button_image(width, height, radius, verde_claro)
        button_image_tk = ImageTk.PhotoImage(rounded_button_image)

        boton_cuarta_ventana = tk.Button(self.frame_principal,activebackground=chocolate, image=button_image_tk, text="Si", compound="center", fg=chocolate, font=font_style_boton, borderwidth=0, highlightthickness=0, command=parent.mostrar_ventana_cuidado_plantas, bg = chocolate)
        boton_cuarta_ventana.grid(row=1, column=0, pady=10, sticky='n')
        boton_cuarta_ventana.image = button_image_tk  # Mantener la referencia a la imagen  
        
        
        boton_regresar_secundaria = tk.Button(self.frame_principal,activebackground=chocolate, image=button_image_tk, text="No", compound="center", fg=chocolate, font=font_style_boton, borderwidth=0, highlightthickness=0, command=parent.mostrar_ventana_secundaria, bg = chocolate)
        boton_regresar_secundaria.grid(row=2, column=0, pady=10, sticky='n')
        boton_regresar_secundaria.image = button_image_tk  # Mantener la referencia a la imagen 

        self.photo_label = tk.Label(self.frame_principal)
        self.photo_label.grid(row=3, column=0, pady=10, sticky='n')

        self.take_photo()


    def create_rounded_button_image(self, width, height, radius, color):
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Dibuja un rectángulo redondeado
        draw.rounded_rectangle((0, 0, width, height), radius, fill=color)

        return image


    def load_image(self, path, width, height):
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el archivo: {path}")
        image = Image.open(path)
        image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    def take_photo(self):
        global current_photo_path
        
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        ret, frame = cap.read()

        if ret:
            current_photo_path = os.path.join(OUTPUT_FOLDER, "foto.jpg")
            cv2.imwrite(current_photo_path, frame)
            self.show_photo(current_photo_path)
        
        cap.release()

    def show_photo(self, photo_path):
        image = Image.open(photo_path)
        image = ImageTk.PhotoImage(image)
        self.photo_label.config(image=image)
        self.photo_label.image = image

class VentanaTerciariaAlternativa(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        print("Ventana terciariaAlternativa")

        self.parent = parent  # Guarda la referencia al padre

        font_style_titulo = ("Helvetica", 20, "bold")
        font_style_boton = ("Helvetica", 15, "bold")

        image4_path = os.path.join(ventana_inicial_path, 'image4.jpg')


        # Carga las imágenes redimensionadas
        img2 = self.load_image(image4_path, desired_width, desired_height)
        

        # Crea widgets de etiqueta para mostrar las imágenes y guarda la referencia de la imagen
        self.label1 = tk.Label(self, image=img2, bd=0)
        self.label1.image = img2  # Mantén una referencia a la imagen
        self.label1.grid(row=0, column=0)  # Coloca la primera imagen en la fila 0, columna 0

        
        self.frame_principal = tk.Frame(self, width=700, height=700, bg=chocolate)
        self.frame_principal.grid(row=0, column=0)  # Colocar el frame en la ventana principal usando grid

        self.frame_principal.grid_propagate(False)

        # Definir el layout del frame
        self.frame_principal.grid_rowconfigure(0, weight=1)
        self.frame_principal.grid_rowconfigure(0, weight=0)  # Eliminar el peso en la fila 0
        self.frame_principal.grid_columnconfigure(0, weight=1)


        self.label = tk.Label(self.frame_principal, text="¿Desea usar esta Foto?", font=font_style_titulo, bg=chocolate, fg=verde_claro)
        self.label.grid(row=0, column=0, pady=10, sticky='n')  # Ajustar el sticky a 'n' para que se alinee arriba


        width, height, radius = 300, 50, 25 #actualmente es 25

        rounded_button_image = self.create_rounded_button_image(width, height, radius, verde_claro)
        button_image_tk = ImageTk.PhotoImage(rounded_button_image)

        boton_cuarta_ventana = tk.Button(self.frame_principal, activebackground=chocolate,image=button_image_tk, text="Si", compound="center", fg=chocolate, font=font_style_boton, borderwidth=0, highlightthickness=0, command=parent.mostrar_ventana_cuidado_plantas, bg = chocolate)
        boton_cuarta_ventana.grid(row=1, column=0, pady=10, sticky='n')
        boton_cuarta_ventana.image = button_image_tk  # Mantener la referencia a la imagen  
        
        
        boton_regresar_secundaria = tk.Button(self.frame_principal,activebackground=chocolate, image=button_image_tk, text="No", compound="center", fg=chocolate, font=font_style_boton, borderwidth=0, highlightthickness=0, command=parent.mostrar_ventana_secundaria, bg = chocolate)
        boton_regresar_secundaria.grid(row=2, column=0, pady=10, sticky='n')
        boton_regresar_secundaria.image = button_image_tk  # Mantener la referencia a la imagen 


        self.prepara_imagenes()


        desired_width_2 = 600
        desired_height_2 = 480

        imagen2_path = os.path.join(fotos_path, "foto.jpg")

        # Carga las imágenes redimensionadas
        img3 = self.load_image(imagen2_path, desired_width_2, desired_height_2)
        

        # Crea widgets de etiqueta para mostrar las imágenes y guarda la referencia de la imagen
        self.photo_label= tk.Label(self.frame_principal, image=img3, bd=0)
        self.photo_label.image = img3  # Mantén una referencia a la imagen
        self.photo_label.grid(row=3, column=0)  # Coloca la primera imagen en la fila 0, columna 0





    def prepara_imagenes(self):


        # Tamaño objetivo
        target_width = 640
        target_height = 480

        # Recorrer todos los archivos en la carpeta actual
        for filename in os.listdir(fotos_path):
            # Verificar si es un archivo de imagen
            if filename.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
            #if filename.lower().endswith((".jpg", ".png", ".jpeg", ".avif", ".webp")):
                # Abrir la imagen
                img_path = os.path.join(fotos_path, filename)
                img = Image.open(img_path)

                # Obtener las dimensiones de la imagen
                width, height = img.size

                # Calcular las coordenadas de recorte para mantener la relación de aspecto
                if width / height > target_width / target_height:
                    # Si la imagen es más ancha que alta, ajustar la altura
                    new_height = height
                    new_width = int(height * target_width / target_height)
                    left = (width - new_width) / 2
                    top = 0
                    right = (width + new_width) / 2
                    bottom = height
                else:
                    # Si la imagen es más alta que ancha, ajustar la anchura
                    new_width = width
                    new_height = int(width * target_height / target_width)
                    left = 0
                    top = (height - new_height) / 2
                    right = width
                    bottom = (height + new_height) / 2

                # Recortar la imagen
                img = img.crop((left, top, right, bottom))

                # Redimensionar la imagen al tamaño objetivo
                img = img.resize((target_width, target_height))

                # Convertir la imagen a RGB (esto es necesario para asegurar que se guarda como JPG)
                img = img.convert("RGB")

                # Guardar la imagen recortada en la misma carpeta con la extensión .jpg
                base_filename = os.path.splitext(filename)[0]
                new_filename = f"{base_filename}.jpg"
                img.save(os.path.join(fotos_path, new_filename), format="JPEG")

        print("Proceso completado.")

        
        
   

    def create_rounded_button_image(self, width, height, radius, color):
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Dibuja un rectángulo redondeado
        draw.rounded_rectangle((0, 0, width, height), radius, fill=color)

        return image


    def load_image(self, path, width, height):
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el archivo: {path}")
        image = Image.open(path)
        image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    def take_photo(self):
        global current_photo_path
        
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        ret, frame = cap.read()

        if ret:
            current_photo_path = os.path.join(OUTPUT_FOLDER, "foto.jpg")
            cv2.imwrite(current_photo_path, frame)
            self.show_photo(current_photo_path)
        
        cap.release()

    def show_photo(self, photo_path):
        image = Image.open(photo_path)
        image = ImageTk.PhotoImage(image)
        self.photo_label.config(image=image)
        self.photo_label.image = image


class Ventana_Graficas(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        print("Ventana secundaria_1")

        font_style = ("Helvetica", 20, "bold")
        font_style_boton = ("Helvetica", 10, "bold")

        self.parent = parent  # Guarda la referencia al padre


        image_path = os.path.join(ventana_secundaria_1_path, 'fondo_ventana_secundaria_1.jpg')

        # Carga las imágenes redimensionadas
        img2 = self.load_image(image_path, desired_width, desired_height)

        # Crea widgets de etiqueta para mostrar las imágenes y guarda la referencia de la imagen
        self.label1 = tk.Label(self, image=img2, bd= 0)
        self.label1.image = img2  # Mantén una referencia a la imagen
        self.label1.grid(row=0, column=0)  # Coloca la primera imagen en la fila 0, columna 0

        self.frame_arduino = tk.Frame(self, width=1200, height=720, bg=chocolate)
        self.frame_arduino.grid(row=0, column=0)  # Colocar el frame en la ventana principal usando grid

        self.frame_arduino.grid_propagate(False)

        # Definir el layout del frame
        self.frame_arduino.grid_rowconfigure(0, weight=1)
        self.frame_arduino.grid_columnconfigure(0, weight=1)

        self.frame_arduino.grid_propagate(False)

        #IMAGENES DE GRAFICAS********************************************************

        image_path_humedad = os.path.join(graficas_path, 'grafica_humedad.jpg')
        image_path_humedad_suelo = os.path.join(graficas_path, 'grafica_HumedadSuelo.jpg')  
        image_path_luminosidad = os.path.join(graficas_path, 'grafica_luminosidad.jpg') 
        image_path_temperatura = os.path.join(graficas_path, 'grafica_Temperatura.jpg')            

        desired_width1 = 600
        desired_height1 = 360

        # Carga las imágenes redimensionadas
        img3 = self.load_image(image_path_humedad, desired_width1, desired_height1)

        # Crea widgets de etiqueta para mostrar las imágenes y guarda la referencia de la imagen
        self.label2 = tk.Label(self.frame_arduino, image=img3, bd= 0)
        self.label2.image = img3  # Mantén una referencia a la imagen
        self.label2.grid(row=0, column=0)  # Coloca la primera imagen en la fila 0, columna 0

        # Carga las imágenes redimensionadas
        img4 = self.load_image(image_path_humedad_suelo, desired_width1, desired_height1)

        # Crea widgets de etiqueta para mostrar las imágenes y guarda la referencia de la imagen
        self.label3 = tk.Label(self.frame_arduino, image=img4, bd= 0)
        self.label3.image = img4  # Mantén una referencia a la imagen
        self.label3.grid(row=0, column=1)  # Coloca la primera imagen en la fila 0, columna 0

        # Carga las imágenes redimensionadas
        img5 = self.load_image(image_path_luminosidad, desired_width1, desired_height1)

        # Crea widgets de etiqueta para mostrar las imágenes y guarda la referencia de la imagen
        self.label4 = tk.Label(self.frame_arduino, image=img5, bd= 0)
        self.label4.image = img5  # Mantén una referencia a la imagen
        self.label4.grid(row=1, column=0)  # Coloca la primera imagen en la fila 0, columna 0


        img6 = self.load_image(image_path_temperatura, desired_width1, desired_height1)

        # Crea widgets de etiqueta para mostrar las imágenes y guarda la referencia de la imagen
        self.label5 = tk.Label(self.frame_arduino, image=img6, bd= 0)
        self.label5.image = img6  # Mantén una referencia a la imagen
        self.label5.grid(row=1, column=1)  # Coloca la primera imagen en la fila 0, columna 0


        #FIN DE IMAGENES GRAFICAS****************************************************

        width, height, radius = 250, 40, 25 #actualmente es 25

        rounded_button_image = self.create_rounded_button_image(width, height, radius, verde_claro)
        button_image_tk = ImageTk.PhotoImage(rounded_button_image)

        boton_atras = tk.Button(self,activebackground=chocolate, image=button_image_tk, text="Atras", compound="center", fg=chocolate, font=font_style_boton, borderwidth=0, highlightthickness=0, command=self.volver_atras, bg = verde_claro)
        boton_atras.grid(row=0, column=0, padx = 50, pady=25, sticky='se')
        boton_atras.image = button_image_tk  # Mantener la referencia a la imagen

    def volver_atras(self):
        if verificador == 1:
            self.parent.mostrar_ventana_secundaria_1()  # Corrección aquí
            
        else:
            self.parent.mostrar_ventana_cuidado_plantas()


    def create_rounded_button_image(self, width, height, radius, color):
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Dibuja un rectángulo redondeado
        draw.rounded_rectangle((0, 0, width, height), radius, fill=color)

        return image


    def load_image(self, path, width, height):
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el archivo: {path}")
        image = Image.open(path)
        image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)


    def on_closing(self):
        self.stop_event.set()
        self.thread.join()
        self.destroy()    





class Ventana_cuidado_plantas(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent # Guarda la referencia al padre
        print("Ventana cuidado_plantas")
        font_style = ("Helvetica", 20, "bold")
        font_style_boton = ("Helvetica", 20, "bold")

        global verificador

        verificador = 0

        deteccion = perform_detection() 

        #***************************PARTE DESECHABLE *******************************
        #deteccion = 'hoja_tomate' #BORRAR O COMENTAR
        
        #*****************************FIN, DE PARTE DESECHABLE**********************

        i = 0
        print("Aqui esta lo del max score", deteccion)
        if (deteccion == 'hoja_sandia'):

            image1_name = 'sandia.jpg'
            i = 5
            image_path = os.path.join(ventana_inicial_path, 'sandia_fondo_2.jpg')

        elif (deteccion == 'hoja_nabo'):

            image1_name = 'nabo.jpg'
            i = 2
            image_path = os.path.join(ventana_inicial_path, 'nabo_fondo_2.jpg')

        elif (deteccion == 'hoja_poroto'):

            image1_name = 'poroto.jpg'
            i = 1
            image_path = os.path.join(ventana_inicial_path, 'poroto_fondo_2.jpg')
            

        elif (deteccion == 'hoja_tomate'):

            image1_name = 'tomate.jpg'
            i = 4
            image_path = os.path.join(ventana_inicial_path, 'tomate_fondo_2.jpg')

        elif (deteccion == 'hoja_culantro'):

            image1_name='culantro.jpg'
            i=6
            image_path = os.path.join(ventana_inicial_path, 'culantro_fondo_2.jpg')

        else:
            image1_name = 'lechuga.jpg'
            i = 3
            image_path = os.path.join(ventana_inicial_path, 'lechuga_fondo_2.jpg')
        

        img2 = self.load_image(image_path, desired_width, desired_height)

        self.label1 = tk.Label(self, image=img2, bd= 0)
        self.label1.image = img2  # Mantén una referencia a la imagen
        self.label1.grid(row=0, column=0)  # Coloca la primera imagen en la fila 0, columna 0
        
        self.frame_principal = tk.Frame(self, width=700, height=700, bg=verde_oliva)
        self.frame_principal.grid(row=0, column=0, sticky='w', padx = 75)  # Colocar el frame en la ventana principal usando grid
        self.frame_principal.grid_propagate(False)

        # Definir el layout del frame
        self.frame_principal.grid_rowconfigure(0, weight=1)
        self.frame_principal.grid_columnconfigure(0, weight=1)

        self.frame_principal.grid_propagate(False)

        #DATOS ARDUINO *****************************************

        self.frame_arduino = tk.Frame(self.frame_principal, width=300, height=300, bg=verde_claro)
        self.frame_arduino.grid(row=0, column=0, sticky='ne')  # Colocar el frame en la ventana principal usando grid
        self.frame_arduino.grid_propagate(False)

        self.frame_arduino.grid_rowconfigure(0, weight=1)
        self.frame_arduino.grid_columnconfigure(0, weight=1)

        self.frame_arduino.grid_propagate(False)

        self.label_datos_serial = tk.Label(self.frame_arduino, text="", font=("Helvetica", 16), bg = verde_claro, fg = verde_letras)
        self.label_datos_serial.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        
        width1, height1, radius1 = 245, 40, 25 #actualmente es 25
        rounded_button_image = self.create_rounded_button_image(width1, height1, radius1, chocolate)
        button_image_tk = ImageTk.PhotoImage(rounded_button_image)

        boton_grafica = tk.Button(self.frame_arduino, activebackground=verde_claro,image = button_image_tk, text="Graficas", compound="center", fg=verde_claro, font=font_style_boton, borderwidth=0, highlightthickness=0, command=self.preparar_ventana_graficas, bg = verde_claro)
        boton_grafica.grid(row=1, column=0, sticky="n")
        boton_grafica.image = button_image_tk  # Mantener la referencia a la imagen

                
        self.stop_event = threading.Event() # Iniciar la lectura del puerto serial en un hilo separado
        self.thread = threading.Thread(target=self.read_from_serial)
        self.thread.start()
        #FIN FRAME ARDUINO*****************************************



        #DATOS CIENTIFICOS*****************************************

        
        self.frame_cientifico = tk.Frame(self.frame_principal, width=700, height=125, bg=verde_letras)
        self.frame_cientifico.grid(row= 1, column=0)

        self.frame_cientifico.grid_propagate(False)

        # Definir el layout del frame
        self.frame_cientifico.grid_rowconfigure(0, weight=1)
        self.frame_cientifico.grid_columnconfigure(0, weight=1)

        font_style_cientifico = ("Helvetica", 10, "bold")

        self.nombre_cientifico = tk.Label(self.frame_cientifico, text="", bg= verde_letras, fg = verde_claro, font=font_style_cientifico)
        self.nombre_cientifico.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.mostrar_cientifico(self.nombre_cientifico, i) 


        #FIN DATOS CIENTIFICOS*************************************

        #DATOS PLANTAS*********************************************

        self.frame_datos_plantas = tk.Frame(self.frame_principal, width=700, height=275, bg=verde_oliva)
        self.frame_datos_plantas.grid(row=2, column=0)

        self.frame_datos_plantas.grid_propagate(False)

        # Definir el layout del frame
        self.frame_datos_plantas.grid_rowconfigure(0, weight=1)
        self.frame_datos_plantas.grid_columnconfigure(0, weight=1)

        #self.datos_plantas = tk.Label(self.frame_datos_plantas, bg="olive", fg="chocolate", justify=tk.LEFT, anchor='nw', wraplength=580)
        #self.datos_plantas.pack(fill=tk.BOTH, expand=True)

        self.datos_plantas = tk.Label(self.frame_datos_plantas, text="", bg=verde_oliva, fg = chocolate, font=font_style_cientifico)
        self.datos_plantas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.mostrar_cultivo(self.datos_plantas, i)



        #FIN DATOS PLANTAS*****************************************

        #IMAGEN DE LA DETECCION************************************

        self.frame_imagen_deteccion = tk.Frame(self.frame_principal, width=300, height=300, bg=verde_claro)
        self.frame_imagen_deteccion.grid(row=0, column=0, sticky='nw')  # Colocar el frame en la ventana principal usando grid
        self.frame_imagen_deteccion.grid_propagate(False)

        image_path = os.path.join(detecciones_path, "detections.jpg")

        # Llamada inicial para cargar la imagen al inicio
        self.cargar_imagen(image_path)

        # Vincular la función cargar_imagen a eventos de redimensionamiento del frame
        self.frame_imagen_deteccion.bind("<Configure>", lambda event: self.cargar_imagen(image_path))



        #FIN DE IMAGEN*********************************************



        width, height, radius = 300, 50, 25 #actualmente es 25

        rounded_button_image = self.create_rounded_button_image(width, height, radius, chocolate)
        button_image_tk = ImageTk.PhotoImage(rounded_button_image)

        boton_regresar_inicial = tk.Button(self, activebackground=chocolate,image = button_image_tk, text="Inicio", compound="center", fg=verde_claro, font=font_style_boton, borderwidth=0, highlightthickness=0, command=self.on_back_button, bg = chocolate)
        boton_regresar_inicial.grid(row=0, column=0, pady=50, padx = 30, sticky='se')
        boton_regresar_inicial.image = button_image_tk  # Mantener la referencia a la imagen

        ruta_guardado = graficas_path

        database = 'Plant_protect' 
        tabla = 'SensorData'
        columnas = ['FechaHora', 'Luz', 'Humedad', 'HumedadSuelo', 'Temperatura']

        '''grafica tendra preferiblemente valores de 1 a 3 representando 'Luz', 'Humedad', 'HumedadSuelo', Temperatura respectivamente '''
        for grafica in range(1, 5):  # Iterar sobre los valores de gráfica
        # Llama a la función para generar cada gráfica
        #objeto_tu_clase.generar_grafica_desde_bd(server, database, tabla, columnas, grafica, ruta_guardado)
            self.generar_grafica_desde_bd(server, database, tabla, columnas, grafica, ruta_guardado=ruta_guardado)

    def preparar_ventana_graficas(self):
        # Señalar que se debe detener el hilo de lectura del puerto serial
        self.stop_event.set()
        # Esperar a que el hilo termine
        self.thread.join()
        # Cerrar la conexión serial si está abierta
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.close()

        self.parent.mostrar_ventana_graficas()

    def on_back_button(self):
        # Señalar que se debe detener el hilo de lectura del puerto serial
        self.stop_event.set()
        # Esperar a que el hilo termine
        self.thread.join()
        # Cerrar la conexión serial si está abierta
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.close()
        # Cambiar de ventana (aquí debes añadir el código para cambiar a la ventana anterior)
        
        '''if(botonpresionado == 1):
            self.parent.mostrar_ventana_graficas()
        else:'''
        # Cambiar de ventana (aquí debes añadir el código para cambiar a la ventana anterior)
        self.parent.mostrar_ventana_inicial()


    def cargar_imagen(self, image_path):
        # Cargar y redimensionar la imagen
        imagen = Image.open(image_path)

        # Obtener las dimensiones del frame
        ancho_frame = self.frame_imagen_deteccion.winfo_width()
        alto_frame = self.frame_imagen_deteccion.winfo_height()

        # Redimensionar la imagen manteniendo la relación de aspecto
        imagen.thumbnail((ancho_frame, alto_frame), Image.LANCZOS) 
        photo = ImageTk.PhotoImage(imagen)

        # Crear (o actualizar si ya existe) el Label para la imagen
        if hasattr(self, 'label_imagen'):
            self.label_imagen.config(image=photo)
            self.label_imagen.image = photo  # Mantener una referencia para evitar que la imagen sea eliminada
        else:
            self.label_imagen = tk.Label(self.frame_imagen_deteccion, image=photo)
            self.label_imagen.pack()

    def create_rounded_button_image(self, width, height, radius, color):
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Dibuja un rectángulo redondeado
        draw.rounded_rectangle((0, 0, width, height), radius, fill=color)

        return image

    def load_image(self, path, width, height):
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el archivo: {path}")
        image = Image.open(path)
        image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)
        
    def show_photo(self, photo_path):
        image = Image.open(photo_path)
        image = ImageTk.PhotoImage(image)
        self.photo_label.config(image=image)
        self.photo_label.image = image

    def read_from_serial(self):
        try:
            self.ser = serial.Serial(port, 9600, timeout=1)  # Ajusta el puerto y la velocidad según sea necesario
            print(f"Conectado al puerto: COM4")
        except serial.SerialException as e:
            print(f"No se pudo conectar al puerto serie: {e}")
            return

        def read_and_update():
            if self.ser.in_waiting > 0:
                try:
                    line = self.ser.readline().decode('utf-8').rstrip()
                    self.update_labels(line)
                except Exception as e:
                    print(f"Error leyendo el puerto serie: {e}")
            if not self.stop_event.is_set():
                # Programar la próxima lectura después de 1 segundo
                self.after(1000, read_and_update)

                # Iniciar la lectura y actualización de forma recursiva
        read_and_update()

    def update_labels(self, values):
        if values.strip() == "":
            return

        # Dividir los datos recibidos por comas
        sensor_data = values.split(",")

        # Verificar si hay suficientes datos
        if len(sensor_data) != 4:
            print("Error: Se esperaban 4 datos de sensor, pero se recibieron menos")
            return

        try:
            # Convertir los datos a tipos numéricos
            humidity = float(sensor_data[0])
            temperature = float(sensor_data[1])
            soil_humidity = float(sensor_data[2])
            light = float(sensor_data[3])
        except ValueError as e:
            print(f"Error al convertir datos a números: {e}")
            return

        # Agregar el encabezado 'Datos de Sensores' antes de los datos
        formatted_data = "Datos de Sensores:\n \n"
        formatted_data += f"- Humedad: {humidity}%\n"
        formatted_data += f"- Temperatura: {temperature} C\n"
        formatted_data += f"- Humedad en Suelo: {soil_humidity}%\n"
        formatted_data += f"- Luz: {light}%"

        self.label_datos_serial.config(text=formatted_data, anchor='w', justify='left')
        
        # Actualizar el label en el hilo principal
        self.label_datos_serial.config(text=formatted_data)

        # Almacenar los datos en la base de datos
        self.store_data_in_db(humidity, temperature, soil_humidity, light)

    def store_data_in_db(self, Humedad, Temperatura, HumedadSuelo, Luz):
        # Detalles de la conexión
    
        database = 'Plant_protect'  

        # Cadena de conexión
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'

        try:
            # Establecer la conexión
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

            # Consulta SQL para insertar los datos
            sql = """
            INSERT INTO SensorData (Humedad, Temperatura, HumedadSuelo, Luz)
            VALUES (?, ?, ?, ?)
            """

            cursor.execute(sql, (Humedad, Temperatura, HumedadSuelo, Luz))
            conn.commit()

            # Cerrar la conexión
            conn.close()

        except Exception as e:
            print("Error al almacenar los datos en la base de datos:", e)


    def generar_grafica_desde_bd(self, server, database, tabla, columnas, grafica, ruta_guardado):
        """
        Genera una gráfica a partir de datos de una base de datos SQL Server y la guarda como imagen.

        Args:
            server (str): Nombre del servidor SQL Server.
            database (str): Nombre de la base de datos.
            tabla (str): Nombre de la tabla de la que se extraerán los datos.
            columnas (list): Lista con los nombres de las columnas a graficar (eje X, eje Y).
            nombre_archivo (str, optional): Nombre del archivo de imagen (sin extensión). Por defecto, "grafica_desde_bd".
        """


        try:
            conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes"
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            '''grafica tendra preferiblemente valores de 1 a 4 representando 'Luz', 'Humedad', 'HumedadSuelo', Temperatura respectivamente '''
            #BORRAR 

            query = f"SELECT {columnas[0]}, {columnas[grafica]} FROM {tabla}"
            cursor.execute(query)

            datos = cursor.fetchall()
            columna_x = [fila[0] for fila in datos]
            columna_y = [fila[1] for fila in datos]

            plt.figure(figsize=(10, 6))
            
            
            if (grafica == 1):
                plt.title('Gráfica de Luminosidad')
                nombre_archivo="grafica_luminosidad"
                color1 = 'red'
            elif(grafica == 2):
                plt.title('Gráfica de Humedad')
                nombre_archivo="grafica_humedad"
                color1 = 'skyblue'
            elif(grafica == 3):
                plt.title('Gráfica de HumedadSuelo')
                nombre_archivo="grafica_HumedadSuelo"
                color1 = 'blue'
            elif(grafica == 4):
                plt.title('Gráfica de Temperatura')
                nombre_archivo="grafica_Temperatura"
                color1 = 'orange'


            plt.plot(columna_x, columna_y, marker='o', linestyle='-', color=color1)

            plt.xlabel(columnas[0])
            plt.ylabel(columnas[grafica])
            plt.grid(axis='y', alpha=0.75)
            plt.xticks(rotation=45, ha="right")

            # Guardar la imagen en la ruta especificada
            ruta_completa_png = os.path.join(ruta_guardado, f"{nombre_archivo}.png")
            plt.savefig(ruta_completa_png)

            ruta_completa_jpg = os.path.join(ruta_guardado, f"{nombre_archivo}.jpg")
            img = Image.open(ruta_completa_png)
            img = img.convert('RGB')
            img.save(ruta_completa_jpg)

        except pyodbc.Error as err:
            print(f"Error en la base de datos: {err}")
        finally:
            conn.close()


    def on_closing(self):
        self.stop_event.set()
        self.thread.join()
        self.destroy()

    def mostrar_cientifico(self, etiqueta, cultivo_id):
        # Detalles de la conexión

        database = 'Plant_protect'  

        # Cadena de conexión
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'

        try:
            # Establecer la conexión
            conn = pyodbc.connect(conn_str)

            # Operaciones con la base de datos
            cursor = conn.cursor()

            # Ejecutar la consulta SQL para obtener la fila correspondiente al cultivo_id
            cursor.execute("SELECT * FROM datos_cientificos WHERE CultivoID = ?", (cultivo_id,))

            # Obtener la fila
            fila = cursor.fetchone()

            # Verificar si se encontró una fila
            if fila:
                # Convertir los valores de la fila en una cadena con texto adicional
                texto_etiqueta = ""
                for indice, valor in enumerate(fila):
                    if indice == 5:

                        texto_etiqueta += "Nombre Comun: " + str(valor) + "\n"

                    elif indice == 0:
                        texto_etiqueta += "Nombre Científico: " + str(valor) + "\n"
                    elif indice == 1:
                        texto_etiqueta += "Familia: " + str(valor) + "\n"
                    elif indice == 2:
                        texto_etiqueta += "Variedades: " + str(valor) + "\n"
                    elif indice == 3:
                        # Aquí puedes agregar más líneas con el formato deseado según las columnas de tu tabla
                        texto_etiqueta += "Origen: " + str(valor) + "\n"
                    else:
                        texto_etiqueta += ""

                # Actualizar el texto del label con la información de la fila

                # Actualizar el texto del label con la información de la fila y alinear hacia la izquierda
                etiqueta.config(text=texto_etiqueta, anchor='w', justify='left')
                #etiqueta.config(text=texto_etiqueta)
            else:
                # Si no se encontró ninguna fila, actualizar el texto del label con un mensaje de error
                etiqueta.config(text="No se encontró información para el cultivo ID especificado")

            # Cerrar la conexión
            conn.close()

        except Exception as e:
            print("Error de conexión:", e)


    def mostrar_cultivo(self, etiqueta, cultivo_id):

        database = 'Plant_protect'

        # Cadena de conexión
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'

        try:
            # Establecer la conexión
            conn = pyodbc.connect(conn_str)

            # Operaciones con la base de datos
            cursor = conn.cursor()

            consulta_sql = """
                SELECT c.planta, c.ciclo, c.epoca, c.distancia, c.suelos, 
                    p.ph_minimo, p.ph_maximo, t.temperatura_min, t.temperatura_max
                FROM cultivos c
                INNER JOIN ph p ON c.id = p.fk_cultivos1
                INNER JOIN temperatura t ON c.id = t.fk_cultivos1
                WHERE c.id = ?  -- Filtrar por el cultivo_id
            """

            # Ejecutar la consulta SQL para obtener la fila correspondiente al cultivo_id
            cursor.execute(consulta_sql, (cultivo_id,))

            # Obtener la fila
            fila = cursor.fetchone()

            # Verificar si se encontró una fila
            if fila:
                # Formatear la información para mostrarla en el label
                texto_etiqueta = f"Ciclo del cultivo: {fila.ciclo}\n\n"
                texto_etiqueta += f"Época de Siembra: {fila.epoca}\n\n"
                texto_etiqueta += f"Distancia de Siembra: {fila.distancia}\n\n"
                texto_etiqueta += "Exigencias Edafoclimáticas:\n\n"
                texto_etiqueta += f"  - Suelos: {fila.suelos}\n"
                texto_etiqueta += f"  - pH: {fila.ph_minimo} a {fila.ph_maximo}\n"
                texto_etiqueta += f"  - Temperatura: {fila.temperatura_min} a {fila.temperatura_max}\n"

                # Actualizar el texto del label con la información de la fila
                etiqueta.config(text=texto_etiqueta, anchor='w', justify='left')
            else:
                # Si no se encontró ninguna fila, actualizar el texto del label con un mensaje de error
                etiqueta.config(text="No se encontró información para el cultivo ID especificado")

            # Cerrar la conexión
            conn.close()

        except Exception as e:
            print("Error de conexión:", e)

class ventana_secundaria_1(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        print("Ventana secundaria_1")

        font_style = ("Helvetica", 20, "bold")
        font_style_boton = ("Helvetica", 10, "bold")
        

        self.parent = parent  # Guarda la referencia al padre

        global verificador
        verificador = 1


        image_path = os.path.join(ventana_secundaria_1_path, 'fondo_ventana_secundaria_1.jpg')

        #color_negro_translucido = "#00000080"  # El valor '80' representa la opacidad (en hexadecimal)

        # Agregar el encabezado 'Datos de Sensores' antes de los datos
        formatted_data_1 = "Datos de Sensores\n \n"
        formatted_data_1 += f"Humedad: \n"
        formatted_data_1 += f"Temperatura: \n"
        formatted_data_1 += f"Humedad en Suelo: \n"
        formatted_data_1 += f"Luz: "

        


        # Carga las imágenes redimensionadas
        img2 = self.load_image(image_path, desired_width, desired_height)

        # Crea widgets de etiqueta para mostrar las imágenes y guarda la referencia de la imagen
        self.label1 = tk.Label(self, image=img2, bd= 0)
        self.label1.image = img2  # Mantén una referencia a la imagen
        self.label1.grid(row=0, column=0)  # Coloca la primera imagen en la fila 0, columna 0

        fondo_datos_arduino = verde_oliva

        self.frame_arduino = tk.Frame(self, width=450, height=375, bg=chocolate)
        self.frame_arduino.grid(row=0, column=0)  # Colocar el frame en la ventana principal usando grid

        self.frame_arduino.grid_propagate(False)

        # Definir el layout del frame
        self.frame_arduino.grid_rowconfigure(0, weight=1)
        self.frame_arduino.grid_columnconfigure(0, weight=1)

        
        self.frame_arduino.grid_propagate(False)

        # Iniciar la lectura del puerto serial en un hilo separado
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.read_from_serial())
        self.thread.start()

        self.label = tk.Label(self.frame_arduino, text=formatted_data_1, bd=0, highlightthickness=0, bg = chocolate, font = font_style, fg = verde_claro)
        self.label.grid(row=0, column=0)

        #self.boton_regresar_inicial = tk.Button(self.frame_arduino, text="Atras", command= self.on_back_button, bg = verde_claro, fg =chocolate, font = font_style_boton)
        #self.boton_regresar_inicial.grid(row=1, column=0)

        width, height, radius = 300, 50, 25 #actualmente es 25

        rounded_button_image = self.create_rounded_button_image(width, height, radius, verde_claro)
        button_image_tk = ImageTk.PhotoImage(rounded_button_image)

        boton_graficas = tk.Button(self.frame_arduino,activebackground=chocolate, image=button_image_tk, text="Graficas", compound="center", fg=chocolate, font=font_style_boton, borderwidth=0, highlightthickness=0, command=self.preparar_ventana_graficas, bg = chocolate)
        boton_graficas.grid(row=1, column=0, pady=10, sticky='n')
        boton_graficas.image = button_image_tk  # Mantener la referencia a la imagen



        rounded_button_image = self.create_rounded_button_image(width, height, radius, verde_claro)
        button_image_tk = ImageTk.PhotoImage(rounded_button_image)

        boton_regresar_inicial = tk.Button(self.frame_arduino,activebackground=chocolate, image=button_image_tk, text="Atras", compound="center", fg=chocolate, font=font_style_boton, borderwidth=0, highlightthickness=0, command=self.on_back_button, bg = chocolate)
        boton_regresar_inicial.grid(row=2, column=0, pady=10, sticky='n')
        boton_regresar_inicial.image = button_image_tk  # Mantener la referencia a la imagen

        ruta_guardado = graficas_path

        database = 'Plant_protect' 
        tabla = 'SensorData'
        columnas = ['FechaHora', 'Luz', 'Humedad', 'HumedadSuelo', 'Temperatura']
        grafica = 1

        '''grafica tendra preferiblemente valores de 1 a 3 representando 'Luz', 'Humedad', 'HumedadSuelo', Temperatura respectivamente '''

        for grafica in range(1, 5):  # Iterar sobre los valores de gráfica
        # Llama a la función para generar cada gráfica
        #objeto_tu_clase.generar_grafica_desde_bd(server, database, tabla, columnas, grafica, ruta_guardado)
            self.generar_grafica_desde_bd(server, database, tabla, columnas, grafica, ruta_guardado=ruta_guardado)

    def preparar_ventana_graficas(self):
        # Señalar que se debe detener el hilo de lectura del puerto serial
        self.stop_event.set()
        # Esperar a que el hilo termine
        self.thread.join()
        # Cerrar la conexión serial si está abierta
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.close()

        self.parent.mostrar_ventana_graficas()

    def create_rounded_button_image(self, width, height, radius, color):
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Dibuja un rectángulo redondeado
        draw.rounded_rectangle((0, 0, width, height), radius, fill=color)

        return image

    def on_back_button(self):
        # Señalar que se debe detener el hilo de lectura del puerto serial
        self.stop_event.set()
        # Esperar a que el hilo termine
        self.thread.join()
        # Cerrar la conexión serial si está abierta
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.close()

        '''if(botonpresionado == 1):
            self.parent.mostrar_ventana_graficas()
        else:
        # Cambiar de ventana (aquí debes añadir el código para cambiar a la ventana anterior)'''
        self.parent.mostrar_ventana_inicial()  # Suponiendo que tienes un método para esto en el padre

    def read_from_serial(self):
        try:
            self.ser = serial.Serial(port, 9600, timeout=1)  # Ajusta el puerto y la velocidad según sea necesario
            print(f"Conectado al puerto: COM3")
        except serial.SerialException as e:
            print(f"No se pudo conectar al puerto serie: {e}")
            return

        def read_and_update():
            if self.ser.in_waiting > 0:
                try:
                    line = self.ser.readline().decode('utf-8').rstrip()
                    self.update_labels(line)
                except Exception as e:
                    print(f"Error leyendo el puerto serie: {e}")
            if not self.stop_event.is_set():
                # Programar la próxima lectura después de 1 segundo
                self.after(1000, read_and_update)

                # Iniciar la lectura y actualización de forma recursiva
        read_and_update()

    def update_labels(self, values):
        if values.strip() == "":
            return

        # Dividir los datos recibidos por comas
        sensor_data = values.split(",")

        # Verificar si hay suficientes datos
        if len(sensor_data) != 4:
            print("Error: Se esperaban 4 datos de sensor, pero se recibieron menos")
            return

        try:
            # Convertir los datos a tipos numéricos
            humidity = float(sensor_data[0])
            temperature = float(sensor_data[1])
            soil_humidity = float(sensor_data[2])
            light = float(sensor_data[3])
        except ValueError as e:
            print(f"Error al convertir datos a números: {e}")
            return

        # Agregar el encabezado 'Datos de Sensores' antes de los datos
        formatted_data = "Datos de Sensores:\n \n"
        formatted_data += f"- Humedad: {humidity}%\n"
        formatted_data += f"- Temperatura: {temperature} C\n"
        formatted_data += f"- Humedad en Suelo: {soil_humidity}%\n"
        formatted_data += f"- Luz: {light}%"

        
        # Actualizar el label en el hilo principal
        self.label.config(text=formatted_data)
        self.store_data_in_db(humidity, temperature, soil_humidity, light)

    def store_data_in_db(self, Humedad, Temperatura, HumedadSuelo, Luz):
        # Detalles de la conexión
    
        database = 'Plant_protect'  

        # Cadena de conexión
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'

        try:
            # Establecer la conexión
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

            # Consulta SQL para insertar los datos
            sql = """
            INSERT INTO SensorData (Humedad, Temperatura, HumedadSuelo, Luz)
            VALUES (?, ?, ?, ?)
            """

            cursor.execute(sql, (Humedad, Temperatura, HumedadSuelo, Luz))
            conn.commit()

            # Cerrar la conexión
            conn.close()

        except Exception as e:
            print("Error al almacenar los datos en la base de datos:", e)


    def generar_grafica_desde_bd(self, server, database, tabla, columnas, grafica, ruta_guardado):
        """
        Genera una gráfica a partir de datos de una base de datos SQL Server y la guarda como imagen.

        Args:
            server (str): Nombre del servidor SQL Server.
            database (str): Nombre de la base de datos.
            tabla (str): Nombre de la tabla de la que se extraerán los datos.
            columnas (list): Lista con los nombres de las columnas a graficar (eje X, eje Y).
            nombre_archivo (str, optional): Nombre del archivo de imagen (sin extensión). Por defecto, "grafica_desde_bd".
        """


        try:
            conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes"
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            '''grafica tendra preferiblemente valores de 1 a 4 representando 'Luz', 'Humedad', 'HumedadSuelo', Temperatura respectivamente '''
            #BORRAR 
           
            query = f"SELECT {columnas[0]}, {columnas[grafica]} FROM {tabla}"
            cursor.execute(query)

            datos = cursor.fetchall()
            columna_x = [fila[0] for fila in datos]
            columna_y = [fila[1] for fila in datos]

            plt.figure(figsize=(10, 6))
            
            
            if (grafica == 1):
                plt.title('Gráfica de Luminosidad')
                nombre_archivo="grafica_luminosidad"
                color1 = 'red'
            elif(grafica == 2):
                plt.title('Gráfica de Humedad')
                nombre_archivo="grafica_humedad"
                color1 = 'skyblue'
            elif(grafica == 3):
                plt.title('Gráfica de HumedadSuelo')
                nombre_archivo="grafica_HumedadSuelo"
                color1 = 'blue'
            elif(grafica == 4):
                plt.title('Gráfica de Temperatura')
                nombre_archivo="grafica_Temperatura"
                color1 = 'orange'


            plt.plot(columna_x, columna_y, marker='o', linestyle='-', color=color1)

            plt.xlabel(columnas[0])
            plt.ylabel(columnas[grafica])
            plt.grid(axis='y', alpha=0.75)
            plt.xticks(rotation=45, ha="right")

            # Guardar la imagen en la ruta especificada
            ruta_completa_png = os.path.join(ruta_guardado, f"{nombre_archivo}.png")
            plt.savefig(ruta_completa_png)

            ruta_completa_jpg = os.path.join(ruta_guardado, f"{nombre_archivo}.jpg")
            img = Image.open(ruta_completa_png)
            img = img.convert('RGB')
            img.save(ruta_completa_jpg)

        except pyodbc.Error as err:
            print(f"Error en la base de datos: {err}")
        finally:
            conn.close()

    def load_image(self, path, width, height):
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el archivo: {path}")
        image = Image.open(path)
        image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)


    def on_closing(self):
        self.stop_event.set()
        self.thread.join()
        self.destroy()    




class ventana_secundaria_2(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
                         
        print("Ventana secundaria_2")



        self.parent = parent  # Guarda la referencia al padre

        row_images = 0
        column_image_1 = 0
        boton_width = 20
        boton_height = 1

        font_style_boton = ("Helvetica", 15, "bold")

        if (self.parent.numero_planta == 5):

            image1_name = 'sandia.jpg'
            image_path = os.path.join(ventana_inicial_path, 'sandia_fondo.jpg')
             

        elif (self.parent.numero_planta == 2):

            image1_name = 'nabo.jpg'
            image_path = os.path.join(ventana_inicial_path, 'image.jpg')

        elif (self.parent.numero_planta == 1):

            image1_name = 'poroto.jpg'
            image_path = os.path.join(ventana_inicial_path, 'image.jpg')

        elif (self.parent.numero_planta == 4):

            image1_name = 'tomate.jpg'
            image_path = os.path.join(ventana_inicial_path, 'image.jpg')

        elif(self.parent.numero_planta == 6):

            image1_name = 'culantro.jpg'
            image_path = os.path.join(ventana_inicial_path, 'image.jpg')

        else:
            image1_name = 'lechuga.jpg'
            image_path = os.path.join(ventana_inicial_path, 'image.jpg')


        #image_path = os.path.join(ventana_inicial_path, 'image.jpg')



        # Carga las imágenes redimensionadas
        img3 = self.load_image(image_path, desired_width, desired_height)

        # Crea widgets de etiqueta para mostrar las imágenes y guarda la referencia de la imagen
        self.label1 = tk.Label(self, image=img3, bd=0)
        self.label1.image = img3  # Mantén una referencia a la imagen
        self.label1.grid(row=0, column=0)  # Coloca la primera imagen en la fila 0, columna         


        beige = '#f5f5dc'

        fondo_cientifico = verde_oliva
        fondo_datos_plantas = marron_siena

        self.frame_todo = tk.Frame(self, width=1200, height=425, bg=beige)
        self.frame_todo.grid(row=0, column=0)

        self.frame_principal1 = tk.Frame(self.frame_todo, width=600, height=425, bg=beige)
        self.frame_principal1.grid(row=0, column=1)

        self.frame_cientifico = tk.Frame(self.frame_principal1, width=600, height=125, bg=fondo_cientifico)
        self.frame_cientifico.grid(row= 0, column=0, sticky='nw')

        self.frame_datos_plantas = tk.Frame(self.frame_principal1, width=600, height=300, bg=fondo_datos_plantas)
        self.frame_datos_plantas.grid(row=1, column=0, sticky='nw')

        self.frame_todo.grid_propagate(False)

        # Definir el layout del frame
        self.frame_todo.grid_rowconfigure(0, weight=1)
        self.frame_todo.grid_columnconfigure(0, weight=1)


        self.frame_principal1.grid_propagate(False)

        # Definir el layout del frame
        self.frame_principal1.grid_rowconfigure(0, weight=1)
        self.frame_principal1.grid_columnconfigure(0, weight=1)

        self.frame_cientifico.grid_propagate(False)

        # Definir el layout del frame
        self.frame_cientifico.grid_rowconfigure(0, weight=1)
        self.frame_cientifico.grid_columnconfigure(0, weight=1)

        self.frame_datos_plantas.grid_propagate(False)

        # Definir el layout del frame
        self.frame_datos_plantas.grid_rowconfigure(0, weight=1)
        self.frame_datos_plantas.grid_columnconfigure(0, weight=1)

        font_style_cientifico = ("Helvetica", 10, "bold")
        font_style_titulo = ("Helvetica", 20, "bold")

        self.nombre_cientifico = tk.Label(self.frame_cientifico, text="", bg= fondo_cientifico, fg = "white", font=font_style_cientifico)
        #self.nombre_cientifico.grid(row=row_label_cientifico, column=0, padx=50, pady=10, sticky='nw')  
        self.nombre_cientifico.grid(row=0, column=0, padx=10, pady=10, sticky='nw')


        self.datos_plantas = tk.Label(self.frame_datos_plantas, text="", bg=fondo_datos_plantas, fg = "white", font=font_style_cientifico)
        self.datos_plantas.grid(row=0, column=0, padx=10, pady=10, sticky='nw')


        self.boton_atras = tk.Button(self.frame_datos_plantas, text="atras", command=parent.mostrar_ventana_botones_plantas, bg= marron_siena, fg='white', font=font_style_boton, width=boton_width, height=boton_height)
        self.boton_atras.grid(row=1, column=0)

        # Define el tamaño deseado para las imágenes
        desired_width = 600
        desired_height = 400


        #Ruta Completa a imagen de los cultivos
        image1_path = os.path.join(web_images_path, image1_name)

        # Carga las imágen de los cultivos redimencionadas
        img1 = self.load_image(image1_path, desired_width, desired_height)

        # Crea widgets de etiqueta para mostrar las imágenes y guarda la referencia de la imagen
        self.label1 = tk.Label(self.frame_todo, image=img1)
        self.label1.image = img1  # Mantén una referencia a la imagen
        self.label1.grid(row=row_images, column=column_image_1, padx=10, pady=10, sticky='nw')  # Coloca la primera imagen en la fila 0, columna 0

        print('Numero planta es:' + str(self.parent.numero_planta))

        self.mostrar_cientifico(self.nombre_cientifico, self.parent.numero_planta) 
        self.mostrar_cultivo(self.datos_plantas, self.parent.numero_planta)


    def on_back_button(self):
            # Señalar que se debe detener el hilo de lectura del puerto serial
            self.stop_event.set()
            # Esperar a que el hilo termine
            self.thread.join()
            # Cerrar la conexión serial si está abierta
            if hasattr(self, 'ser') and self.ser.is_open:
                self.ser.close()
            # Cambiar de ventana (aquí debes añadir el código para cambiar a la ventana anterior)
            self.parent.mostrar_ventana_secundaria()  # Suponiendo que tienes un método para esto en el padre


    def load_image(self, path, width, height):
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el archivo: {path}")
        image = Image.open(path)
        image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    
    def mostrar_cientifico(self, etiqueta, cultivo_id):


        database = 'Plant_protect'  

        # Cadena de conexión
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'

        try:
            # Establecer la conexión
            conn = pyodbc.connect(conn_str)

            # Operaciones con la base de datos
            cursor = conn.cursor()

            # Ejecutar la consulta SQL para obtener la fila correspondiente al cultivo_id
            cursor.execute("SELECT * FROM datos_cientificos WHERE CultivoID = ?", (cultivo_id,))

            print('Cultivo id vale: ' + str(cultivo_id))  # Convertir cultivo_id a cadena

            # Obtener la fila
            fila = cursor.fetchone()

            # Verificar si se encontró una fila
            if fila:
                # Convertir los valores de la fila en una cadena con texto adicional
                texto_etiqueta = ""
                for indice, valor in enumerate(fila):
                    if indice == 5:
                        texto_etiqueta += "Nombre Comun: " + str(valor) + "\n"
                    elif indice == 0:
                        texto_etiqueta += "Nombre Científico: " + str(valor) + "\n"
                    elif indice == 1:
                        texto_etiqueta += "Familia: " + str(valor) + "\n"
                    elif indice == 2:
                        texto_etiqueta += "Variedades: " + str(valor) + "\n"
                    elif indice == 3:
                        # Aquí puedes agregar más líneas con el formato deseado según las columnas de tu tabla
                        texto_etiqueta += "Origen: " + str(valor) + "\n"
                    else:
                        texto_etiqueta += ""

                # Actualizar el texto del label con la información de la fila y alinear hacia la izquierda
                etiqueta.config(text=texto_etiqueta, anchor='w', justify='left')
            else:
                # Si no se encontró ninguna fila, actualizar el texto del label con un mensaje de error
                etiqueta.config(text="No se encontró información para el cultivo ID especificado")

            # Cerrar la conexión
            conn.close()

        except Exception as e:
            print("Error de conexión:", e)



    def mostrar_cultivo(self, etiqueta, cultivo_id):

        database = 'Plant_protect'

        # Cadena de conexión
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'

        try:
            # Establecer la conexión
            conn = pyodbc.connect(conn_str)

            # Operaciones con la base de datos
            cursor = conn.cursor()

            # Ejecutar la consulta SQL para obtener la fila correspondiente al cultivo_id
            cursor.execute("SELECT * FROM cultivos WHERE ID = ?", (cultivo_id,))

            # Obtener la fila
            fila = cursor.fetchone()

            # Verificar si se encontró una fila
            if fila:
                # Formatear la información para mostrarla en el label
                texto_etiqueta = f"Ciclo del cultivo: {fila.ciclo}\n\n"
                texto_etiqueta += f"Época de Siembra: {fila.epoca}\n\n"
                texto_etiqueta += f"Distancia de Siembra: {fila.distancia}\n\n"
                texto_etiqueta += "Exigencias Edafoclimáticas:\n"
                texto_etiqueta += f"  - Suelos: {fila.suelos}\n"
                texto_etiqueta += f"  - pH: {fila.ph_minimo} a {fila.ph_maximo}\n"
                texto_etiqueta += f"  - Humedad: {fila.Agua}\n"
                texto_etiqueta += f"  - Temperatura: {fila.Temperatura_min} a {fila.temperatura_max}\n"

                # Actualizar el texto del label con la información de la fila
                etiqueta.config(text=texto_etiqueta, anchor='w', justify='left')
            else:
                # Si no se encontró ninguna fila, actualizar el texto del label con un mensaje de error
                etiqueta.config(text="No se encontró información para el cultivo ID especificado")

            # Cerrar la conexión
            conn.close()

        except Exception as e:
            print("Error de conexión:", e)


class ventana_botones_plantas(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        print("Ventana botones_plantas")

        self.parent = parent  # Guarda la referencia al padre

        boton_width = 20
        boton_height = 1

        font_style_titulo = ("Helvetica", 20, "bold")
        font_style_boton = ("Helvetica", 15, "bold")

        image_path = os.path.join(ventana_inicial_path, 'image2.jpg')

        # Carga las imágenes redimensionadas
        img2 = self.load_image(image_path, desired_width, desired_height)

        # Crea widgets de etiqueta para mostrar las imágenes y guarda la referencia de la imagen
        self.label1 = tk.Label(self, image=img2, bd=0)
        self.label1.image = img2  # Mantén una referencia a la imagen
        self.label1.grid(row=0, column=0)  # Coloca la primera imagen en la fila 0, columna 0

        
        self.frame_principal = tk.Frame(self, width=600, height=425, bg=verde_oliva)
        self.frame_principal.grid(row=0, column=0)  # Colocar el frame en la ventana principal usando grid

        self.frame_principal.grid_propagate(False)

        # Definir el layout del frame
        self.frame_principal.grid_rowconfigure(0, weight=1)
        self.frame_principal.grid_rowconfigure(0, weight=0)  # Eliminar el peso en la fila 0
        self.frame_principal.grid_columnconfigure(0, weight=1)

        self.label = tk.Label(self.frame_principal, text="¿De que planta desea aprender?", font=font_style_titulo, bg=verde_oliva, fg=verde_letras)
        self.label.grid(row=0, column=0, pady=10, sticky='n')  # Ajustar el sticky a 'n' para que se alinee arriba

        width, height, radius = 300, 40, 25 #actualmente es 25

        rounded_button_image = self.create_rounded_button_image(width, height, radius, verde_claro)
        button_image_tk = ImageTk.PhotoImage(rounded_button_image)

        #boton_sandia = tk.Button(self.frame_principal, text="Sandía", command=lambda: self.selector(5), bg=verde_oliva, fg='white', font=font_style_boton, width=boton_width, height=boton_height)


        boton_poroto = tk.Button(self.frame_principal,activebackground=verde_oliva, image=button_image_tk, text="Poroto", compound="center", fg=verde_letras, font=font_style_boton, borderwidth=0, highlightthickness=0, command=lambda: self.selector(1), bg = verde_oliva)
        boton_poroto.grid(row=1, column=0, pady=5, sticky='n')
        boton_poroto.image = button_image_tk

        boton_nabo = tk.Button(self.frame_principal,activebackground=verde_oliva, image=button_image_tk, text="Nabo Blanco", compound="center", fg=verde_letras, font=font_style_boton, borderwidth=0, highlightthickness=0, command=lambda: self.selector(2), bg = verde_oliva)
        boton_nabo.grid(row=2, column=0, pady=5, sticky='n')
        boton_nabo.image = button_image_tk

        boton_lechuga = tk.Button(self.frame_principal,activebackground=verde_oliva, image=button_image_tk, text="Lechuga", compound="center", fg=verde_letras, font=font_style_boton, borderwidth=0, highlightthickness=0, command=lambda: self.selector(3), bg = verde_oliva)
        boton_lechuga.grid(row=3, column=0, pady=5, sticky='n')
        boton_lechuga.image = button_image_tk

        boton_tomate = tk.Button(self.frame_principal,activebackground=verde_oliva, image=button_image_tk, text="Tomate", compound="center", fg=verde_letras, font=font_style_boton, borderwidth=0, highlightthickness=0, command=lambda: self.selector(4), bg = verde_oliva)
        boton_tomate.grid(row=4, column=0, pady=5, sticky='n')
        boton_tomate.image = button_image_tk

        boton_sandia = tk.Button(self.frame_principal,activebackground=verde_oliva, image=button_image_tk, text="Sandía", compound="center", fg=verde_letras, font=font_style_boton, borderwidth=0, highlightthickness=0, command=lambda: self.selector(5), bg = verde_oliva)
        boton_sandia.grid(row=5, column=0, pady=5, sticky='n')
        boton_sandia.image = button_image_tk

        boton_culantro = tk.Button(self.frame_principal,activebackground=verde_oliva, image=button_image_tk, text="Culantro", compound="center", fg=verde_letras, font=font_style_boton, borderwidth=0, highlightthickness=0, command=lambda: self.selector(6), bg = verde_oliva)
        boton_culantro.grid(row=6, column=0, pady=5, sticky='n')
        boton_culantro.image = button_image_tk

        boton_atras = tk.Button(self.frame_principal, activebackground=verde_oliva,image=button_image_tk, text="Atras", compound="center", fg=verde_letras, font=font_style_boton, borderwidth=0, highlightthickness=0, command=self.parent.mostrar_ventana_inicial, bg = verde_oliva)
        boton_atras.grid(row=7, column=0, pady=5, sticky='n')
        boton_atras.image = button_image_tk




    def create_rounded_button_image(self, width, height, radius, color):
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Dibuja un rectángulo redondeado
        draw.rounded_rectangle((0, 0, width, height), radius, fill=color)

        return image



    def selector(self, planta):

        if planta == 1:
            self.parent.numero_planta = 1
        elif planta == 2:
            self.parent.numero_planta = 2
        elif planta == 3:
            self.parent.numero_planta = 3
        elif planta == 4:
            self.parent.numero_planta = 4
        elif planta == 6:
            self.parent.numero_planta = 6
        else:
           self.parent. numero_planta = 5

        self.parent.mostrar_ventana_datos_plantas()
        

    def load_image(self, path, width, height):
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el archivo: {path}")
        image = Image.open(path)
        image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    
class Ventana_datos_plantas(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        print("Ventana botones_plantas")

        self.parent = parent # Guarda la referencia al padre
        font_style = ("Helvetica", 20, "bold")
        font_style_boton = ("Helvetica", 20, "bold")
        font_titulo = ("Helvetica", 40, "bold")

        nombre = ""

        
        if (self.parent.numero_planta == 5):
            image_path = os.path.join(ventana_inicial_path, 'sandia_fondo_2.jpg')
            nombre="SANDIA"
             

        elif (self.parent.numero_planta == 2):

            image_path = os.path.join(ventana_inicial_path, 'nabo_fondo_2.jpg')
            nombre="NABO"

        elif (self.parent.numero_planta == 1):


            image_path = os.path.join(ventana_inicial_path, 'poroto_fondo_2.jpg')
            nombre="POROTO"

        elif (self.parent.numero_planta == 4):

           
            image_path = os.path.join(ventana_inicial_path, 'tomate_fondo_2.jpg')
            nombre="TOMATE"

        elif(self.parent.numero_planta == 6):

   
            image_path = os.path.join(ventana_inicial_path, 'culantro_fondo_2.jpg')
            nombre="CULANTRO"


        else:
            image1_name = 'lechuga.jpg'
            image_path = os.path.join(ventana_inicial_path, 'lechuga_fondo_2.jpg')
            nombre="LECHUGA"
        

        img2 = self.load_image(image_path, desired_width, desired_height)

        self.label1 = tk.Label(self, image=img2, bd= 0)
        self.label1.image = img2  # Mantén una referencia a la imagen
        self.label1.grid(row=0, column=0)  # Coloca la primera imagen en la fila 0, columna 0
        
        self.frame_principal = tk.Frame(self, width=700, height=500, bg=chocolate)
        self.frame_principal.grid(row=0, column=0, sticky='w', padx = 75)  # Colocar el frame en la ventana principal usando grid
        self.frame_principal.grid_propagate(False)

        # Definir el layout del frame
        self.frame_principal.grid_rowconfigure(0, weight=1)
        self.frame_principal.grid_columnconfigure(0, weight=1)

        self.frame_principal.grid_propagate(False)

        self.titulo = tk.Label(self.frame_principal, text=nombre, bg= chocolate, fg = verde_claro, font=font_titulo)
        self.titulo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        #DATOS CIENTIFICOS*****************************************

        
        self.frame_cientifico = tk.Frame(self.frame_principal, width=700, height=125, bg=chocolate)
        self.frame_cientifico.grid(row= 1, column=0)

        self.frame_cientifico.grid_propagate(False)

        # Definir el layout del frame
        self.frame_cientifico.grid_rowconfigure(0, weight=1)
        self.frame_cientifico.grid_columnconfigure(0, weight=1)

        font_style_cientifico = ("Helvetica", 10, "bold")

        self.nombre_cientifico = tk.Label(self.frame_cientifico, text="", bg= chocolate, fg = verde_claro, font=font_style_cientifico)
        self.nombre_cientifico.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.mostrar_cientifico(self.nombre_cientifico, parent.numero_planta) 


        #FIN DATOS CIENTIFICOS*************************************

        #DATOS PLANTAS*********************************************

        self.frame_datos_plantas = tk.Frame(self.frame_principal, width=700, height=275, bg=verde_oliva)
        self.frame_datos_plantas.grid(row=2, column=0)

        self.frame_datos_plantas.grid_propagate(False)

        # Definir el layout del frame
        self.frame_datos_plantas.grid_rowconfigure(0, weight=1)
        self.frame_datos_plantas.grid_columnconfigure(0, weight=1)

        #self.datos_plantas = tk.Label(self.frame_datos_plantas, bg="olive", fg="chocolate", justify=tk.LEFT, anchor='nw', wraplength=580)
        #self.datos_plantas.pack(fill=tk.BOTH, expand=True)

        self.datos_plantas = tk.Label(self.frame_datos_plantas, text="", bg=verde_oliva, fg = chocolate, font=font_style_cientifico)
        self.datos_plantas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.mostrar_cultivo(self.datos_plantas, parent.numero_planta)



        #FIN DATOS PLANTAS*****************************************

        width, height, radius = 300, 50, 25 #actualmente es 25

        rounded_button_image = self.create_rounded_button_image(width, height, radius, chocolate)
        button_image_tk = ImageTk.PhotoImage(rounded_button_image)

        boton_regresar_inicial = tk.Button(self,activebackground=chocolate, image = button_image_tk, text="Atras", compound="center", fg=verde_claro, font=font_style_boton, borderwidth=0, highlightthickness=0, command=self.parent.mostrar_ventana_botones_plantas, bg = chocolate)
        boton_regresar_inicial.grid(row=0, column=0, pady=50, padx = 30, sticky='se')
        boton_regresar_inicial.image = button_image_tk  # Mantener la referencia a la imagen




    def cargar_imagen(self, image_path):
        # Cargar y redimensionar la imagen
        imagen = Image.open(image_path)

        # Obtener las dimensiones del frame
        ancho_frame = self.frame_imagen_deteccion.winfo_width()
        alto_frame = self.frame_imagen_deteccion.winfo_height()

        # Redimensionar la imagen manteniendo la relación de aspecto
        imagen.thumbnail((ancho_frame, alto_frame), Image.LANCZOS) 
        photo = ImageTk.PhotoImage(imagen)

        # Crear (o actualizar si ya existe) el Label para la imagen
        if hasattr(self, 'label_imagen'):
            self.label_imagen.config(image=photo)
            self.label_imagen.image = photo  # Mantener una referencia para evitar que la imagen sea eliminada
        else:
            self.label_imagen = tk.Label(self.frame_imagen_deteccion, image=photo)
            self.label_imagen.pack()

    def create_rounded_button_image(self, width, height, radius, color):
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Dibuja un rectángulo redondeado
        draw.rounded_rectangle((0, 0, width, height), radius, fill=color)

        return image

    def load_image(self, path, width, height):
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el archivo: {path}")
        image = Image.open(path)
        image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)
        
    def show_photo(self, photo_path):
        image = Image.open(photo_path)
        image = ImageTk.PhotoImage(image)
        self.photo_label.config(image=image)
        self.photo_label.image = image


    def mostrar_cientifico(self, etiqueta, cultivo_id):
        # Detalles de la conexión


        database = 'Plant_protect'  

        # Cadena de conexión
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'

        try:
            # Establecer la conexión
            conn = pyodbc.connect(conn_str)

            # Operaciones con la base de datos
            cursor = conn.cursor()

            # Ejecutar la consulta SQL para obtener la fila correspondiente al cultivo_id
            cursor.execute("SELECT * FROM datos_cientificos WHERE CultivoID = ?", (cultivo_id,))

            # Obtener la fila
            fila = cursor.fetchone()

            # Verificar si se encontró una fila
            if fila:
                # Convertir los valores de la fila en una cadena con texto adicional
                texto_etiqueta = ""
                for indice, valor in enumerate(fila):
                    if indice == 5:

                        texto_etiqueta += "Nombre Comun: " + str(valor) + "\n"

                    elif indice == 0:
                        texto_etiqueta += "Nombre Científico: " + str(valor) + "\n"
                    elif indice == 1:
                        texto_etiqueta += "Familia: " + str(valor) + "\n"
                    elif indice == 2:
                        texto_etiqueta += "Variedades: " + str(valor) + "\n"
                    elif indice == 3:
                        # Aquí puedes agregar más líneas con el formato deseado según las columnas de tu tabla
                        texto_etiqueta += "Origen: " + str(valor) + "\n"
                    else:
                        texto_etiqueta += ""

                # Actualizar el texto del label con la información de la fila

                # Actualizar el texto del label con la información de la fila y alinear hacia la izquierda
                etiqueta.config(text=texto_etiqueta, anchor='w', justify='left')
                #etiqueta.config(text=texto_etiqueta)
            else:
                # Si no se encontró ninguna fila, actualizar el texto del label con un mensaje de error
                etiqueta.config(text="No se encontró información para el cultivo ID especificado")

            # Cerrar la conexión
            conn.close()

        except Exception as e:
            print("Error de conexión:", e)


    def mostrar_cultivo(self, etiqueta, cultivo_id):



        database = 'Plant_protect'

        # Cadena de conexión
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'

        try:
            # Establecer la conexión
            conn = pyodbc.connect(conn_str)

            # Operaciones con la base de datos
            cursor = conn.cursor()

            consulta_sql = """
                SELECT c.planta, c.ciclo, c.epoca, c.distancia, c.suelos, 
                    p.ph_minimo, p.ph_maximo, t.temperatura_min, t.temperatura_max
                FROM cultivos c
                INNER JOIN ph p ON c.id = p.fk_cultivos1
                INNER JOIN temperatura t ON c.id = t.fk_cultivos1
                WHERE c.id = ?  -- Filtrar por el cultivo_id
            """

            # Ejecutar la consulta SQL para obtener la fila correspondiente al cultivo_id
            cursor.execute(consulta_sql, (cultivo_id,))

            # Obtener la fila
            fila = cursor.fetchone()

            # Verificar si se encontró una fila
            if fila:
                # Formatear la información para mostrarla en el label
                texto_etiqueta = f"Ciclo del cultivo: {fila.ciclo}\n\n"
                texto_etiqueta += f"Época de Siembra: {fila.epoca}\n\n"
                texto_etiqueta += f"Distancia de Siembra: {fila.distancia}\n\n"
                texto_etiqueta += "Exigencias Edafoclimáticas:\n\n"
                texto_etiqueta += f"  - Suelos: {fila.suelos}\n"
                texto_etiqueta += f"  - pH: {fila.ph_minimo} a {fila.ph_maximo}\n"
                texto_etiqueta += f"  - Temperatura: {fila.temperatura_min} a {fila.temperatura_max}\n"

                # Actualizar el texto del label con la información de la fila
                etiqueta.config(text=texto_etiqueta, anchor='w', justify='left')
            else:
                # Si no se encontró ninguna fila, actualizar el texto del label con un mensaje de error
                etiqueta.config(text="No se encontró información para el cultivo ID especificado")

            # Cerrar la conexión
            conn.close()

        except Exception as e:
            print("Error de conexión:", e)




# Directorios y archivos de configuración
#CUSTOM_MODEL_NAME = 'plant_protect_model'
CUSTOM_MODEL_NAME = 'new_model'

LABEL_MAP_NAME = 'label_map.pbtxt'

paths = {
    'WORKSPACE_PATH': os.path.join('Tensorflow', 'workspace'),
    'APIMODEL_PATH': os.path.join('Tensorflow', 'models'),
    'ANNOTATION_PATH': os.path.join('Tensorflow', 'workspace', 'annotations'),
    'IMAGE_PATH': os.path.join('Tensorflow', 'workspace', 'images'),
    'MODEL_PATH': os.path.join('Tensorflow', 'workspace', 'models'),
    'CHECKPOINT_PATH': os.path.join('Tensorflow', 'workspace', 'models', CUSTOM_MODEL_NAME, 'my_model', 'checkpoint'),
    'PROTOC_PATH': os.path.join('Tensorflow', 'protoc')
}

files = {
    'PIPELINE_CONFIG': os.path.join('Tensorflow', 'workspace', 'models', CUSTOM_MODEL_NAME, 'my_model', 'pipeline.config'),
    'LABELMAP': os.path.join(paths['ANNOTATION_PATH'], LABEL_MAP_NAME)
}

'''# Define las etiquetas con los nombres específicos que necesitas
labels = [{'name': 'hoja_nabo', 'id': 1},
          {'name': 'hoja_poroto', 'id': 2},
          {'name': 'hoja_sandia', 'id': 3},
          {'name': 'hoja_tomate', 'id': 4},
          {'name': 'lechuga', 'id': 5}]'''

# Define las etiquetas con los nombres específicos que necesitas
labels = [{'name': 'hoja_nabo', 'id': 1},
          {'name': 'hoja_poroto', 'id': 2},
          {'name': 'hoja_sandia', 'id': 3},
          {'name': 'hoja_tomate', 'id': 4},
          {'name': 'lechuga', 'id': 5},
          {'name': 'hoja_culantro', 'id': 6}]

with open(files['LABELMAP'], 'w') as f:
    for label in labels:
        f.write('item { \n')
        f.write('\tname:\'{}\'\n'.format(label['name']))
        f.write('\tid:{}\n'.format(label['id']))
        f.write('}\n')

# Carga la configuración del pipeline y construye el modelo de detección
configs = config_util.get_configs_from_pipeline_file(files['PIPELINE_CONFIG'])
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restaura el checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(paths['CHECKPOINT_PATH'], 'ckpt-0')).expect_partial()

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections

category_index = label_map_util.create_category_index_from_labelmap(files['LABELMAP'])



def perform_detection():
    global image_np_with_detections
    global detection_model
    global category_index

    # Lista de archivos en la carpeta
    image_files = [f for f in os.listdir(fotos_path) if os.path.isfile(os.path.join(fotos_path, f))]

    # Verificar si hay exactamente una imagen en la carpeta
    if len(image_files) == 1:
        # Ruta completa de la imagen única
        image_path = os.path.join(fotos_path, image_files[0])

        img = cv2.imread(image_path)
        image_np = np.array(img)

        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
        detections = detect_fn(input_tensor)

        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
        detections['num_detections'] = num_detections

        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        label_id_offset = 1
        image_np_with_detections = image_np.copy()

        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'],
            detections['detection_classes'] + label_id_offset,
            detections['detection_scores'],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=5,
            min_score_thresh=.8,
            agnostic_mode=False
        )

        # Obtén el cuadro delimitador y la clase de la detección con la puntuación más alta
        max_score_idx = np.argmax(detections['detection_scores'])
        max_score = detections['detection_scores'][max_score_idx]
        max_score_class = detections['detection_classes'][max_score_idx] + label_id_offset
        max_score_class_name = category_index[max_score_class]['name']

        # Imprime el nombre del objeto detectado con la puntuación más alta
        print("Objeto detectado:", max_score_class_name, "con una puntuación de", max_score)

        cv2.imwrite(file_path, image_np_with_detections)
        return(max_score_class_name)
    else:
        print("La carpeta no contiene exactamente una imagen.")


if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()




