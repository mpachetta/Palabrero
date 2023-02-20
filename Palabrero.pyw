from tkinter import *
import random as rd
import re
import pygame
import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment
import speech_recognition as sr
import csv
import os
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
from tkinter import filedialog as fd

colors = ["#88F2A2", "#7D7ABF", "#F2C335", "#D93B84", "#F2D649","#60A140"]


class Game:
    def __init__(self):
        self.root = root
        self.counter = 10

    def define_element(self, file):
        self.file = file
        with open(self.file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            self.element = list(reader)

    def choose(self):

        self.selected_index = rd.randrange(1, len(self.element))

        return self.element[self.selected_index]

    def listen(self, sound):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

    def speaching(self):
        return self.element[self.selected_index]

    def end_screen(self):
        if self.counter < 1:

            self.root.after(2000, lambda: self.go_back())
        else:
            self.root.after(2200, lambda: self.play())


class User:

    def __init__(self):

        self.user_name = ""
        self.user_password = ""
        self.user_img=""
        self.user_stars = 0

    def set_name(self, name):
        self.user_name = name

    def get_name(self):

        return self.user_name

    def give_stars(self, points):

        self.user_stars += points

        df = pd.read_csv("usuarios.csv")

        # Obtiene el índice de la fila que deseas modificar
        index = df[df["name"] == self.user_name].index[0]

        # Asigna un valor a la celda en la columna "stars" de esa fila
        df.at[index, "stars"] = self.user_stars

        # Guarda los cambios en el archivo csv
        df.to_csv("usuarios.csv", index=False)

    def publish_stars(self):

        x = str(self.user_stars) + " puntos"
        return x
    def get_user_img(self):
        if os.path.exists(str("Images_user/"+self.get_name()+".png")):
            self.user_img=PhotoImage(file=str("Images_user/"+self.get_name()+".png"))
        else:
            self.user_img=PhotoImage(file="usuario.png")
    def change_user_img(self):
        # Abrir archivo de imagen
        file_path = fd.askopenfilename()
        
        image = Image.open(file_path)

        # Cambiar tamaño de la imagen a 32x32
        resized_img = image.resize((32, 32))
        
        save_dir="Images_user"
        filename=self.get_name()+".png"
        save_path = os.path.join(save_dir, str(filename))
        resized_img.save(save_path)
        # Convertir imagen para usar en tkinter
        photo = ImageTk.PhotoImage(resized_img)

        # Asignar imagen al atributo user_img
        self.user_img = photo

class MainScreen:
    def __init__(self, root):
        self.root = root
        self.root.geometry("350x600")

        self.title = Label(self.root, text="PALABRERO",
                           font=("Fun Blob", 35),fg=colors[5])
        self.title.pack(pady=20)
        self.img_logo = PhotoImage(file="rompecabezas256.png")
        self.container1 = Frame(self.root)
        self.container1.pack()
        self.logo = ttk.Label(self.container1, image=self.img_logo)
        self.logo.grid(row=0, columnspan=2)
        self.btn_style = ttk.Style()
        self.btn_style.configure("MyButton.TButton", font=("Serif", 12))
        self.login_button = ttk.Button(
            self.container1, text="Iniciar sesión", command=self.login, style="MyButton.TButton")
        self.login_button.grid(row=1, column=0, pady=20)
        self.signup_button = ttk.Button(
            self.container1, text="Registrarse", style="MyButton.TButton", command=self.signup)
        self.signup_button.grid(row=1, column=1, pady=20)

        self.img_exit = PhotoImage(file="off.png")
        self.exit = Button(self.container1, text="Salir",
                           image=self.img_exit, command=self.app_exit)
        self.exit.grid(columnspan=2, row=2, pady=35)
        self.creditos = Button(
            self.container1, text="Créditos", command=self.ir_creditos)
        self.creditos.grid(columnspan=2, row=3, pady=35)

        self.container = Label(self.root)
        self.label_username = Label(self.container, text="Nombre de usuario: ")
        self.entry_username = Entry(self.container)
        self.label_pasword = Label(self.container, text="Ingrese una clave: ")
        self.entry_password = Entry(self.container, show="*")
        self.label_pasword_repeat = Label(
            self.container, text="Repita la clave: ")
        self.entry_password_repeat = Entry(self.container, show="*")
        self.button_signup = ttk.Button(
            self.container, text="Registrarse", command=self.datos_completos, style="MyButton.TButton")
        self.button_login = ttk.Button(self.container, text="Ingresar", command=lambda: self.login_comprobate(
            self.entry_username.get(), self.entry_password.get()), style="MyButton.TButton")
        self.button_back = Button(
            self.container, text="Volver", command=self.volver)

    def login(self):
        self.clean()

        self.title.pack(pady=20)
        self.container1.pack()
        self.logo.grid(row=0, column=0)
        self.container.pack()
        self.label_username.grid(column=0, row=0, pady=10)
        self.entry_username.grid(column=1, row=0, pady=10)
        self.label_pasword.grid(column=0, row=1, pady=10)
        self.entry_password.grid(column=1, row=1, pady=10)
        self.button_login.grid(columnspan=2, row=2, pady=10)
        self.button_back.grid(columnspan=2, row=3)

    def login_comprobate(self, name, clave):
        if self.entry_username.get() and self.entry_password.get():
            df = pd.read_csv("usuarios.csv")
            if name in df['name'].values:
                # Obtener la fila en la que el elemento aparece en la columna "name"
                row = df[df['name'] == name].index[0]
                # Comprobar si la clave coincide con el elemento correspondiente en la misma fila
                if df.at[row, 'clave'] == clave:
                    print("ok")

                    result = df[(df["name"] == name) & (df["clave"] == clave)]

                    current_user.user_stars = int(result["stars"].values[0])

                    current_user.set_name(name)
                    current_user.publish_stars()
                    self.go_to_second_screen()
                    return True
                else:
                    print("El usuario o clave son incorrectos")
                    return False
            else:
                return False

    def signup(self):
        self.clean()

        self.title.pack(pady=20)
        self.container1.pack()
        self.logo.grid(row=0, column=0)
        self.container.pack()

        self.label_username.grid(column=0, row=0, pady=10)
        self.entry_username.grid(column=1, row=0, pady=10)
        self.label_pasword.grid(column=0, row=1, pady=10)
        self.entry_password.grid(column=1, row=1, pady=10)
        self.label_pasword_repeat.grid(column=0, row=2, pady=10)
        self.entry_password_repeat.grid(column=1, row=2, pady=10)
        self.button_signup.grid(columnspan=2, row=3, pady=10)
        self.button_back.grid(columnspan=2, row=4)

    def signup_create(self, name, clave, clave1):
        with open("usuarios.csv", "r") as file:
            reader = csv.reader(file)
            try:
                usuarios = [row[0] for row in reader]

            except IndexError:
                print("El archivo CSV no contiene la columna requerida")
                return False

        if name in usuarios:
            print("El usuario ya existe.")
            self.ventana_aviso("El usuario ya existe.")
            return False

        if clave != clave1:
            print("Las claves no coinciden.")
            self.ventana_aviso("Las claves no coinciden.")
            return False

        with open("usuarios.csv", "a", newline="\n") as file:
            writer = csv.writer(file)
            writer.writerow([name, clave, 0.0])

        print("Usuario creado exitosamente.")

        self.login()

    def ventana_aviso(self, msj):
        self.ventana = Toplevel(self.root)
        self.ventana.geometry("200x100+100+100")
        self.ventana.title("Ventana Emergente")

        self.mensaje = Label(self.ventana, text=msj)
        self.mensaje.pack()
        self.btn_cerrar = Button(
            self.ventana, text="Cerrar", command=self.cerrar)
        self.btn_cerrar.pack()

    def cerrar(self):
        self.ventana.destroy()

    def datos_completos(self):
        if self.entry_username.get() and self.entry_password.get() and self.entry_password_repeat.get():

            self.signup_create(self.entry_username.get(
            ), self.entry_password.get(), self.entry_password_repeat.get())
        else:
            self.ventana_aviso("Hay campos sin completar")

    def clean(self):

        self.title.pack_forget()
        self.login_button.grid_forget()
        self.signup_button.grid_forget()
        self.entry_password.grid_forget()
        self.entry_password_repeat.grid_forget()
        self.entry_username.grid_forget()
        self.label_pasword.grid_forget()
        self.label_pasword_repeat.grid_forget()
        self.label_username.grid_forget()
        self.button_signup.grid_forget()
        self.container.pack_forget()
        self.container1.pack_forget
        self.logo.grid_forget()
        self.button_login.pack_forget()
        self.login_button.pack_forget()
        self.button_back.grid_forget()
        self.logo.grid_forget()
        self.signup_button.grid_forget()
        self.container1.pack_forget()
        self.creditos.grid_forget()
        self.exit.grid_forget()

    def ir_creditos(self):
        self.clean()
        Creditos(self.root)

    def volver(self):
        self.clean()
        MainScreen(root)

    def app_exit(self):
        self.root.destroy()

    def go_to_second_screen(self):
        self.clean()
        SecondScreen(self.root)


class Creditos:
    def __init__(self, root):
        self.root = root
        self.credito_title = Label(text="PALABRERO", font=("Fun Blob", 35),fg=colors[5])
        self.credito_title.pack(pady=20)
        self.credito_app = Message(self.root, text=open(
            "credito_app.txt", "r", encoding="UTF-8").read(), bg=colors[4], width=300)
        self.credito_app.pack()
        self.img_cc = Image.open("cc.png")
        self.img_cc_tk = ImageTk.PhotoImage(self.img_cc)
        self.img_label = Label(self.root, image=self.img_cc_tk)
        self.img_label.pack(pady=20)

        self.credito_exit = Button(
            self.root, text="Volver", command=self.go_back)
        self.credito_exit.pack()

    def clean(self):
        self.credito_title.pack_forget()

        self.credito_app.pack_forget()
        self.credito_exit.pack_forget()
        self.img_label.pack_forget()

    def go_back(self):
        self.clean()
        MainScreen(root)


class SecondScreen:
    def __init__(self, root):

        self.root = root

        self.label_box = Frame(self.root,bg=colors[2])
        self.label_box.pack(pady=5)
        self.img_0 = PhotoImage(file="exit.png")
        
        self.style = ttk.Style()
        self.style.configure("Label.User.TLabel", font=(14),width=14, height=3, background=colors[2])

        current_user.get_user_img()
        self.label_username = ttk.Label(
            self.label_box, text=current_user.get_name(), image=current_user.user_img, compound="left",style="Label.User.TLabel")
        
        
        self.label_username.bind("<Button-1>",self.new_user_img)
        
        self.label_stars = ttk.Label(
            self.label_box, text=current_user.publish_stars(), style="Label.User.TLabel")
        self.log_out = Button(
            self.label_box, image=self.img_0, command=self.exit)

        self.label_username.grid(column=0, row=0)
        self.label_stars.grid(column=1, row=0)
        self.log_out.grid(column=2, row=0)

        self.img_1 = PhotoImage(file="spell-check1.png")
        self.img_2 = PhotoImage(file="microphone1.png")
        self.img_3 = PhotoImage(file="auditory1.png")
        self.img_4 = PhotoImage(file="learning1.png")
        self.img_7 = PhotoImage(file="sentence1.png")

        self.button1 = Button(self.root, image=self.img_1,
                              bd="0", command=self.go_to_screen1)
        self.button1.pack()
        self.button2 = Button(self.root, image=self.img_2,
                              text="Opción 2", bd="0", command=self.go_to_screen2)
        self.button2.pack()
        self.button3 = Button(self.root, image=self.img_3,
                              text="Opción 3", bd="0", command=self.go_to_screen3)
        self.button3.pack()
        self.button4 = Button(self.root, image=self.img_4,
                              text="Opción 4", bd="0", command=self.go_to_screen4)
        self.button4.pack()
        self.button5 = Button(self.root, image=self.img_7,
                              text="Opción 5", bd="0", command=self.go_to_screen5)
        self.button5.pack()
        self.label_username["bg"] = colors[2]
        self.label_stars["bg"] = colors[4]
    
    def new_user_img(self,event):
        current_user.change_user_img()
        self.button1.pack_forget()
        self.button2.pack_forget()
        self.button3.pack_forget()
        self.button4.pack_forget()
        self.button5.pack_forget()
        self.label_username.grid_forget()
        self.label_stars.grid_forget()
        self.label_box.pack_forget()
        SecondScreen(root) 
    
    def exit(self):
        self.button1.pack_forget()
        self.button2.pack_forget()
        self.button3.pack_forget()
        self.button4.pack_forget()
        self.button5.pack_forget()
        self.label_username.grid_forget()
        self.label_stars.grid_forget()
        self.label_box.pack_forget()
        
        MainScreen(self.root)

    def go_to_screen1(self):
        self.button1.pack_forget()
        self.button2.pack_forget()
        self.button3.pack_forget()
        self.button4.pack_forget()
        self.button5.pack_forget()
        self.label_username.grid_forget()
        self.label_stars.grid_forget()
        self.label_box.pack_forget()
        Screen1(self.root)

    def go_to_screen2(self):
        self.button1.pack_forget()
        self.button2.pack_forget()
        self.button3.pack_forget()
        self.button4.pack_forget()
        self.button5.pack_forget()
        self.label_username.grid_forget()
        self.label_stars.grid_forget()
        self.label_box.pack_forget()
        Screen2(self.root)

    def go_to_screen3(self):
        self.button1.pack_forget()
        self.button2.pack_forget()
        self.button3.pack_forget()
        self.button4.pack_forget()
        self.button5.pack_forget()
        self.label_username.grid_forget()
        self.label_stars.grid_forget()
        self.label_box.pack_forget()
        Screen3(self.root)

    def go_to_screen4(self):
        self.button1.pack_forget()
        self.button2.pack_forget()
        self.button3.pack_forget()
        self.button4.pack_forget()
        self.button5.pack_forget()
        self.label_username.grid_forget()
        self.label_stars.grid_forget()
        self.label_box.pack_forget()
        Screen4(self.root)

    def go_to_screen5(self):
        self.button1.pack_forget()
        self.button2.pack_forget()
        self.button3.pack_forget()
        self.button4.pack_forget()
        self.button5.pack_forget()
        self.label_username.grid_forget()
        self.label_stars.grid_forget()
        self.label_box.pack_forget()
        Screen5(self.root)


# juego de ortografía, solo palabras individuales

class Screen1:

    def __init__(self, root):

        self.root = root
        self.screen1_title = Label(self.root, text="Escucha y escribe:", font=(
            "Calibri", 12), bg=colors[1], fg="white")
        self.screen1_title.pack(fill=X)
        self.screen1_listen_ico = PhotoImage(file="listen.png")
        self.screen1_listen = Button(
            self.root, text="Escuchar", bd="0", width="350")
        self.screen1_listen.config(image=self.screen1_listen_ico)
        self.screen1_listen.pack(pady=20)
        self.screen1_notice = Frame(self.root)

        self.screen1_label = Label(self.screen1_notice, font=(14))

        self.screen1_label.pack()
        self.screen1_entry = Entry(
            self.root, font=(14), fg="blue", justify="center")
        self.screen1_entry.pack(pady=20)

        self.btn_style = ttk.Style()
        self.btn_style.configure("MyButton.TButton", font=("Verdana", 12))

        self.valuation_button = ttk.Button(
            self.root, text="Comprobar", style="MyButton.TButton")
        # self.valuation_button.config(font=("Verdana",12),relief="ridge",overrelief="raised",bd=1,activeforeground=colors[0])
        self.valuation_button.pack(ipadx=6, ipady=2)
        self.back_button = Button(
            self.root, text="Volver", command=self.go_back)
        self.back_button.pack(side="bottom", pady=10)

        self.current_game = Game()
        self.counter = 10
        self.used_elements = []
        self.root.after(1000, lambda: self.play())
        self.current_game.define_element("palabras.csv")

    def play(self):

        self.elemento_elegido = self.current_game.choose()
        if self.elemento_elegido not in self.used_elements:
            self.used_elements.append(self.elemento_elegido)
            self.current_game.listen(self.elemento_elegido[0])
            self.screen1_entry.focus_set()
            self.screen1_listen.config(
                command=lambda: self.current_game.listen(self.elemento_elegido[0]))

            self.valuation_button.config(command=lambda: self.evaluate_spelling(
                self.elemento_elegido[1], self.screen1_entry.get()))

    def evaluate_spelling(self, arg, answer):

        if re.match(arg, answer, re.IGNORECASE):

            current_user.give_stars(10)
            self.screen1_entry.delete("0", "end")

            self.screen1_label.config(
                text="¡Muy bien!\n"+"\n"+"\nTienes "+current_user.publish_stars())
            self.screen1_label.config(bg=colors[0])
            self.screen1_notice.config(bg=colors[0])
            self.screen1_notice.pack(ipadx=10, ipady=30, expand=True, fill=X)
            current_user.publish_stars()

        else:
            current_user.give_stars(0)
            self.screen1_entry.delete("0", "end")
            self.screen1_label.config(text="Intenta la próxima")
            self.screen1_label.config(bg=colors[3])
            self.screen1_notice.config(bg=colors[3])
            self.screen1_notice.pack(ipadx=10, ipady=30, expand=True, fill=X)

        self.root.after(2000, lambda: self.screen1_label.config(text=""))
        self.root.after(2000, lambda: self.screen1_notice.pack_forget())

        self.counter -= 1
        self.end_screen()

    def end_screen(self):
        if self.counter < 1:

            self.root.after(2000, lambda: self.go_back())
        else:
            self.root.after(2200, lambda: self.play())

    def go_back(self):
        self.screen1_title.pack_forget()
        self.back_button.pack_forget()
        self.screen1_label.pack_forget()
        self.screen1_listen.pack_forget()
        self.screen1_entry.pack_forget()
        self.valuation_button.pack_forget()
        self.screen1_notice.pack_forget()
        SecondScreen(self.root)


# juego en el que tienen que pronunciar
class Screen2:
    def __init__(self, root):
        self.root = root
        self.screen2_title = Label(self.root, text="Lee en voz alta", font=(
            "Calibri", 12), bg=colors[1], fg="white")
        self.screen2_title.pack(fill=X)
        self.screen2_label1 = Label(
            self.root, font=("Comic Sans", 15), bg=colors[2])
        self.screen2_label1.pack(fill=X, pady=20, ipady=10)
        self.img_6 = PhotoImage(file="microfono.png")
        self.img_5 = PhotoImage(file="microfono_bn.png")
        self.screen2_microphone = Button(
            self.root, image=self.img_6, relief="flat")
        self.screen2_microphone.pack(pady=20)

        self.img_9 = PhotoImage(file="siguiente.png")
        self.next_button = Button(
            self.root, text="Siguiente", image=self.img_9, command=self.play)
        self.next_button.pack()

        self.screen2_notice = Frame(self.root)

        self.screen2_label = Label(self.screen2_notice, font=(14))

        self.screen2_label.pack()

        self.back_button = Button(
            self.root, text="Volver", command=self.go_back)
        self.back_button.pack(side="bottom", pady=10)

        self.current_game = Game()
        self.current_game.define_element("palabras.csv")
        self.counter = 10
        self.used_elements = []
        self.root.after(1000, lambda: self.play())
        self.audio = None

    def iniciar_grabacion(self, event):

        # self.screen2_microphone.config(image=self.img_6)

        # Código para iniciar la grabación

        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            self.audio = r.listen(source)

    def finalizar_grabacion(self, event):

        # self.screen2_microphone.config(image=self.img_5)

        r = sr.Recognizer()
        try:
            text = r.recognize_google(self.audio)
            if re.search(self.elemento_elegido[1], text, re.IGNORECASE):

                current_user.give_stars(10)

                self.screen2_label.config(
                    text="¡Muy bien!\n"+self.elemento_elegido[1]+"\nTienes "+current_user.publish_stars())
                self.screen2_label.config(bg=colors[0])
                self.screen2_notice.config(bg=colors[0])
                self.screen2_notice.pack(
                    ipadx=10, ipady=30, expand=True, fill=X)
                current_user.publish_stars()
            else:

                current_user.give_stars(0)

                self.screen2_label.config(text="Intenta la próxima")
                self.screen2_label.config(bg=colors[3])
                self.screen2_notice.config(bg=colors[3])
                self.screen2_notice.pack(
                    ipadx=10, ipady=30, expand=True, fill=X)
            self.counter -= 1

        except:

            self.screen2_label.config(text="No se pudo escuchar el audio")
            self.screen2_label.config(bg=colors[3])
            self.screen2_notice.config(bg=colors[3])
            self.screen2_notice.pack(ipadx=10, ipady=30, expand=True, fill=X)

        self.root.after(2000, lambda: self.screen2_label1.config(text=""))
        self.root.after(2000, lambda: self.screen2_notice.pack_forget())
        self.end_screen()

    def end_screen(self):
        if self.counter < 1:

            self.root.after(2000, lambda: self.go_back())
        else:
            self.root.after(2200, lambda: self.play())

    def play(self):

        self.elemento_elegido = self.current_game.choose()
        if self.elemento_elegido not in self.used_elements:
            self.used_elements.append(self.elemento_elegido)
            self.elemento_elegido = self.current_game.choose()
            self.screen2_label1.config(text=self.elemento_elegido[1])

            self.screen2_microphone.bind("<Button-1>", self.iniciar_grabacion)
            self.screen2_microphone.bind(
                "<ButtonRelease-1>", self.finalizar_grabacion)

    # Volver a la pantalla anterior

    def go_back(self):
        self.screen2_title.pack_forget()
        self.back_button.pack_forget()
        self.screen2_label.pack_forget()
        self.screen2_microphone.pack_forget()
        self.next_button.pack_forget()
        self.screen2_label1.pack_forget()

        SecondScreen(self.root)


# escuchar frases y escribirlas
class Screen3:

    def __init__(self, root):

        self.root = root
        self.screen3_title = Label(self.root, text="Escucha y escribe la frase:", font=(
            "Calibri", 12), bg=colors[1], fg="white")
        self.screen3_title.pack(fill=X)
        self.screen3_listen_ico = PhotoImage(file="listen.png")
        self.screen3_listen = Button(
            self.root, text="Escuchar", bd="0", width="350")
        self.screen3_listen.config(image=self.screen3_listen_ico)
        self.screen3_listen.pack(pady=20)
        self.screen3_notice = Frame(self.root)

        self.screen3_label = Label(self.screen3_notice, font=(14))

        self.screen3_label.pack()
        self.screen3_board = Text(
            self.root, width=35, height=5, bg=colors[0], wrap="word", font=(20))
        self.screen3_board.pack(pady=20)

        self.screen3_options_box = Frame(self.root, width=300)
        self.screen3_options_box.pack(pady=10)

        self.screen3_palabras = Button()

        self.img_8 = PhotoImage(file="deshacer.png")

        self.screen3_deshacer = Button(self.root, image=self.img_8)
        self.screen3_deshacer.pack(pady=10)

        self.btn_style = ttk.Style()
        self.btn_style.configure("MyButton.TButton", font=("Verdana", 12))

        self.valuation_button = ttk.Button(
            self.root, text="Comprobar", style="MyButton.TButton")
        self.valuation_button.pack(pady=25)
        self.back_button = Button(
            self.root, text="Volver", command=self.go_back)
        self.back_button.pack(side="bottom", pady=10)

        self.current_game = Game()
        self.counter = 10
        self.used_elements = []
        self.root.after(1000, lambda: self.play())
        self.current_game.define_element("frases.csv")

    def play(self):

        self.elemento_elegido = self.current_game.choose()
        if self.elemento_elegido not in self.used_elements:
            self.used_elements.append(self.elemento_elegido)
            self.current_game.listen(self.elemento_elegido[0])
            self.screen3_board.focus_set()
            self.screen3_listen.config(
                command=lambda: self.current_game.listen(self.elemento_elegido[0]))

            self.segmentar = self.elemento_elegido[1].split(" ")

            self.propuesta = rd.sample(self.segmentar, k=len(self.segmentar))
            i = 0
            y = 0

            for x in self.propuesta:

                self.screen3_palabras = Button(
                    self.screen3_options_box, text=x)
                self.screen3_palabras.config(
                    font=("Comic Sans", 13), bg="white", relief="flat", highlightthickness=0)

                self.screen3_palabras.grid(row=y, column=i, padx=5, pady=5)
                i += 1
                if i > 4:
                    i = 0
                    y += 1

                self.screen3_palabras.bind(
                    "<Button-1>", lambda event: self.apretar(event))
                self.screen3_deshacer.configure(
                    command=lambda: self.deshacer_apretados(self.propuesta))

            self.valuation_button.config(command=lambda: self.evaluate_spelling(
                self.elemento_elegido[1], self.screen3_board.get(1.0, END)))

    def apretar(self, event):
        valor = event.widget.cget("text")
        self.screen3_board.insert("end", valor+" ")
        # event.widget.config(state="disabled")
        event.widget.destroy()

    def deshacer_apretados(self, prop):
        i = 0
        y = 0

        for x in self.propuesta:

            self.screen3_palabras = Button(self.screen3_options_box, text=x)
            self.screen3_palabras.config(
                font=("Comic Sans", 13), bg="white", relief="flat", highlightthickness=0)

            self.screen3_palabras.grid(row=y, column=i, padx=5, pady=5)
            i += 1
            if i > 4:
                i = 0
                y += 1
            self.screen3_palabras.bind(
                "<Button-1>", lambda event: self.apretar(event))
        self.screen3_board.delete("1.0", END)

    def evaluate_spelling(self, arg, answer):

        if re.match(arg, answer):

            current_user.give_stars(10)

            self.screen3_label.config(
                text="¡Muy bien!\n"+"\n"+"\nTienes "+current_user.publish_stars())
            self.screen3_label.config(bg=colors[0])
            self.screen3_notice.config(bg=colors[0])
            self.screen3_notice.pack(ipadx=10, ipady=30, expand=True, fill=X)

            current_user.publish_stars()

        else:
            current_user.give_stars(0)

            self.screen3_label.config(text="Intenta la próxima")
            self.screen3_label.config(bg=colors[3])
            self.screen3_notice.config(bg=colors[3])
            self.screen3_notice.pack(ipadx=10, ipady=30, expand=True, fill=X)

        self.root.after(2000, lambda: self.screen3_label.config(text=""))
        self.root.after(2000, lambda: self.screen3_notice.pack_forget())
        self.screen3_board.delete("1.0", "end")
        for child in self.screen3_options_box.winfo_children():
            child.destroy()
        self.counter -= 1
        self.end_screen()

    def end_screen(self):
        if self.counter < 1:

            self.root.after(2000, lambda: self.go_back())
        else:
            self.root.after(2200, lambda: self.play())

    def go_back(self):
        self.screen3_title.pack_forget()
        self.back_button.pack_forget()
        self.screen3_label.pack_forget()
        self.screen3_listen.pack_forget()
        self.screen3_board.pack_forget()
        self.valuation_button.pack_forget()
        self.screen3_notice.pack_forget()
        self.screen3_options_box.pack_forget()
        self.screen3_palabras.pack_forget()
        self.screen3_deshacer.pack_forget()
        SecondScreen(self.root)

# juego con textos breves en los que tengan que localizar información o interpretar


class Screen4:
    def __init__(self, root):
        self.root = root
        self.screen4_title = Label(self.root, text="Lee con atención y elige la respuesta correcta:", font=(
            "Calibri", 12), bg=colors[1], fg="white")
        self.screen4_title.pack(fill=X)

        self.screen4_sentence = Message(
            self.root, text="", width=250, font=("Comic Sans MS", 14), bg="lightgray")

        self.screen4_question = Message(
            self.root, width=250, font=("Helvética", 12), bg=colors[3])

        self.screen4_options = Frame(self.root, width=300, bd=0)
        self.btn_style = ttk.Style()
        self.btn_style.configure(
            "MyButton.TButton", font=("Calibri Light", 10))

        self.screen4_option1 = ttk.Button(
            self.screen4_options, text="", style="MyButton.TButton")

        self.screen4_option2 = ttk.Button(
            self.screen4_options, text="", style="MyButton.TButton")

        self.screen4_option3 = ttk.Button(
            self.screen4_options, text="", style="MyButton.TButton")

        self.screen4_notice = Frame(self.root)
        self.screen4_label = Label(self.screen4_notice, font=(14))
        self.screen4_label.pack()

        # self.valuation_button=Button(self.root,text="Comprobar")
        # self.valuation_button.pack()

        self.back_button = Button(
            self.root, text="Volver", command=self.go_back)
        self.back_button.pack(side="bottom", pady=10)

        self.current_game = Game()
        self.current_game.define_element("trivia.csv")
        self.used_elements = []
        self.counter = 10
        self.root.after(1000, lambda: self.play())

    def play(self):
        self.elemento_elegido = self.current_game.choose()

        if self.elemento_elegido not in self.used_elements:
            self.used_elements.append(self.elemento_elegido)
            self.screen4_sentence.config(text=self.elemento_elegido[0])
            self.screen4_question.config(text=self.elemento_elegido[1])

            self.opciones = [2, 3, 4]
            rd.shuffle(self.opciones)

            self.screen4_option1.config(
                text=self.elemento_elegido[self.opciones[0]], state="!disabled")
            self.screen4_option2.config(
                text=self.elemento_elegido[self.opciones[1]], state="!disabled")
            self.screen4_option3.config(
                text=self.elemento_elegido[self.opciones[2]], state="!disabled")

            self.screen4_option1.bind("<Button-1>", self.evaluate)
            self.screen4_option2.bind("<Button-1>", self.evaluate)
            self.screen4_option3.bind("<Button-1>", self.evaluate)

            self.screen4_sentence.pack(pady=20)

            self.screen4_question.pack()

            self.screen4_options.pack()

            self.screen4_option1.pack(pady=2)

            self.screen4_option2.pack(pady=2)

            self.screen4_option3.pack(pady=2)

    def evaluate(self, event):
        self.selected_index = event.widget["text"]
        self.screen4_option1.config(state="disabled")
        self.screen4_option2.config(state="disabled")
        self.screen4_option3.config(state="disabled")
        self.screen4_option1.unbind("<Button-1>")
        self.screen4_option2.unbind("<Button-1>")
        self.screen4_option3.unbind("<Button-1>")
        if self.selected_index == self.elemento_elegido[5]:
            current_user.give_stars(10)
            self.screen4_label.config(
                text="¡Muy bien!\n"+"\nTienes "+current_user.publish_stars())
            self.screen4_label.config(bg=colors[0])
            self.screen4_notice.config(bg=colors[0])
            self.screen4_notice.pack(ipadx=10, ipady=30, expand=True, fill=X)
            current_user.publish_stars()
        elif self.selected_index != self.elemento_elegido[5]:
            current_user.give_stars(0)

            self.screen4_label.config(text="Intenta la próxima")
            self.screen4_label.config(bg=colors[3])
            self.screen4_notice.config(bg=colors[3])
            self.screen4_notice.pack(ipadx=10, ipady=30, expand=True, fill=X)

        self.root.after(2000, lambda: self.screen4_label.config(text=""))
        self.root.after(2000, lambda: self.screen4_notice.pack_forget())

        self.counter -= 1
        self.end_screen()

    def end_screen(self):
        if self.counter < 1:

            self.root.after(2000, lambda: self.go_back())
        else:
            self.root.after(2200, lambda: self.play())

    def go_back(self):
        self.screen4_title.pack_forget()
        self.back_button.pack_forget()
        self.screen4_label.pack_forget()
        self.screen4_notice.pack_forget()
        self.screen4_option1.pack_forget()
        self.screen4_option2.pack_forget()
        self.screen4_option3.pack_forget()
        self.screen4_options.pack_forget()
        self.screen4_question.pack_forget()
        self.screen4_sentence.pack_forget()
        SecondScreen(self.root)

#Juego rellenar el espacio
class Screen5:
    def __init__(self, root):
        self.root = root
        self.screen5_title = Label(self.root, text="Completa el espacio con la palabra correcta:", font=(
            "Calibri", 12), bg=colors[1], fg="white")
        self.screen5_title.pack(fill=X)
        self.screen5_sentence = Message(
            self.root, text="", width=250, font=("Comic Sans MS", 12), bg="lightgray")

        self.screen5_options = Frame(self.root, width=300, bd=0)
        self.btn_style = ttk.Style()
        self.btn_style.configure(
            "MyButton.TButton", font=("Calibri Light", 10))

        self.screen5_option1 = ttk.Button(
            self.screen5_options, text="", style="MyButton.TButton")

        self.screen5_option2 = ttk.Button(
            self.screen5_options, text="", style="MyButton.TButton")

        self.screen5_option3 = ttk.Button(
            self.screen5_options, text="", style="MyButton.TButton")

        self.screen5_notice = Frame(self.root)
        self.screen5_label = Label(self.screen5_notice, font=(14))
        self.screen5_label.pack()

        self.back_button = Button(
            self.root, text="Volver", command=self.go_back)
        self.back_button.pack(side="bottom", pady=10)

        self.current_game = Game()
        self.current_game.define_element("rellenar.csv")
        self.used_elements = []
        self.counter = 10
        self.root.after(1000, lambda: self.play())

    def play(self):
        self.elemento_elegido = self.current_game.choose()

        if self.elemento_elegido not in self.used_elements:
            self.used_elements.append(self.elemento_elegido)
            self.screen5_sentence.config(text=self.elemento_elegido[0])

            self.opciones = [1, 2, 3]
            rd.shuffle(self.opciones)

            self.screen5_option1.config(
                text=self.elemento_elegido[self.opciones[0]], state="!disabled")
            self.screen5_option2.config(
                text=self.elemento_elegido[self.opciones[1]], state="!disabled")
            self.screen5_option3.config(
                text=self.elemento_elegido[self.opciones[2]], state="!disabled")

            self.screen5_option1.bind("<Button-1>", self.evaluate)
            self.screen5_option2.bind("<Button-1>", self.evaluate)
            self.screen5_option3.bind("<Button-1>", self.evaluate)

            self.screen5_sentence.pack(pady=20)

            self.screen5_options.pack()

            self.screen5_option1.pack(pady=2)

            self.screen5_option2.pack(pady=2)

            self.screen5_option3.pack(pady=2)

    def evaluate(self, event):
        self.selected_index = event.widget["text"]
        self.screen5_option1.config(state="disabled")
        self.screen5_option2.config(state="disabled")
        self.screen5_option3.config(state="disabled")
        self.screen5_option1.unbind("<Button-1>")
        self.screen5_option2.unbind("<Button-1>")
        self.screen5_option3.unbind("<Button-1>")
        if self.selected_index == self.elemento_elegido[4]:
            current_user.give_stars(10)
            self.screen5_label.config(
                text="¡Muy bien!\n"+"\nTienes "+current_user.publish_stars())
            self.screen5_label.config(bg=colors[0])
            self.screen5_notice.config(bg=colors[0])
            self.screen5_notice.pack(ipadx=10, ipady=30, expand=True, fill=X)
            current_user.publish_stars()
        elif self.selected_index != self.elemento_elegido[5]:
            current_user.give_stars(0)

            self.screen5_label.config(text="Intenta la próxima")
            self.screen5_label.config(bg=colors[3])
            self.screen5_notice.config(bg=colors[3])
            self.screen5_notice.pack(ipadx=10, ipady=30, expand=True, fill=X)

        self.root.after(2000, lambda: self.screen5_label.config(text=""))
        self.root.after(2000, lambda: self.screen5_notice.pack_forget())

        self.counter -= 1
        self.end_screen()

    def end_screen(self):
        if self.counter < 1:

            self.root.after(2000, lambda: self.go_back())
        else:
            self.root.after(2200, lambda: self.play())

    def go_back(self):
        self.screen5_title.pack_forget()
        self.back_button.pack_forget()
        self.screen5_label.pack_forget()
        self.screen5_notice.pack_forget()
        self.screen5_option1.pack_forget()
        self.screen5_option2.pack_forget()
        self.screen5_option3.pack_forget()
        self.screen5_options.pack_forget()
        self.screen5_sentence.pack_forget()

        SecondScreen(self.root)


root = Tk()
root.iconbitmap("ico.ico")
root.title("Palabrero")
current_user = User()
MainScreen(root)

root.mainloop()


# Mejoras:
# establecer niveles: crear por ejemplo palabras1.csv, palabras2.csv etc según complejidad que se vayan habilitando si es que consigue el nivel anterior
# debería tener una variable que guarde los niveles y un if elif elif que designe el archico a usar para cada juego deacuerdo a al nivel al que puedan acceder
