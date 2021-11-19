#================#
#    IMPORTS     #
#================#

from tkinter import *
from tkinter import filedialog as tkifd
import pygame
import os

from music_parser import MusicParser

#================#
#    CLASSES     #
#================#


class MusicPlayer:
    def __init__(self, window):

        # Cria configuracoes GUI iniciais
        self.window = window
        self.window.title("Player")
        self.window.geometry("635x410")

        # Inicializa o player de musica
        pygame.init()
        pygame.mixer.init()

        # Inicializa variaveis da classe
        self.track = StringVar(self.window, "Track name")
        self.status = StringVar(self.window, "Status")
        self.error_message = StringVar()
        self.stream = None

        # Frame interno para o player
        trackframe = LabelFrame(
            self.window,
            text="Song Track",
            font=(
                "helvetica",
                9
            ),
            bg="lightgrey",
            fg="black"
        )
        trackframe.place(
            x=0,
            y=0,
            width=430,
            height=67
        )

        # Label do nome da faixa sendo reproduzida
        songtrack = Label(
            trackframe,
            textvariable=self.track,
            width=20,
            font=(
                "helvetica",
                11
            ),
            bg="darkgrey",
            fg="white",
            height=1
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=6
        )

        # Label do status de reproducao (playing, paused...)
        trackstatus = Label(
            trackframe,
            textvariable=self.status,
            font=(
                "helvetica",
                11
            ),
            bg="darkgrey",
            fg="white",
            width=20
        ).grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )

        # Frame interno do painel de controle de reproducao
        buttonframe = LabelFrame(
            self.window,
            text="Control Panel",
            font=(
                "helvetica",
                9
            ),
            bg="lightgrey",
            fg="black"
        )
        buttonframe.place(
            x=0,
            y=75,
            width=430,
            height=70
        )

        # Botao de play
        playbtn = Button(
            buttonframe,
            text="PLAY",
            command=self.playSong,
            width=10,
            height=1,
            font=(
                "helvetica",
                9
            ),
            fg="white",
            bg="darkgrey"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=5
        )

        # Botao de pause
        pausebtn = Button(
            buttonframe,
            text="PAUSE",
            command=self.pauseSong,
            width=10,
            height=1,
            font=(
                "helvetica",
                9
            ),
            fg="white",
            bg="darkgrey"
        ).grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )

        # Botao de despausar
        unpausebtn = Button(
            buttonframe,
            text="UNPAUSE",
            command=self.unpauseSong,
            width=10,
            height=1,
            font=(
                "helvetica",
                9
            ),
            fg="white",
            bg="darkgrey"
        ).grid(
            row=0,
            column=2,
            padx=10,
            pady=5
        )

        # Botao de stop
        stopbtn = Button(
            buttonframe,
            text="STOP",
            command=self.stopSong,
            width=10,
            height=1,
            font=(
                "helvetica",
                9
            ),
            fg="white",
            bg="darkgrey"
        ).grid(
            row=0,
            column=3,
            padx=10,
            pady=5
        )

        # Frame interno para a playlist
        songsframe = LabelFrame(
            self.window,
            text="Song Playlist",
            font=(
                "helvetica",
                9
            ),
            bg="lightgrey",
            fg="black"
        )
        songsframe.place(
            x=430,
            y=0,
            width=205,
            height=146
        )

        # Conteiner da playlist
        scrol_y = Scrollbar(songsframe, orient=VERTICAL)
        self.playlist = Listbox(
            songsframe,
            yscrollcommand=scrol_y.set,
            selectbackground="grey",
            selectmode=SINGLE,
            font=(
                "helvetica",
                9
            ),
            bg="lightgrey",
            fg="navy"
        )
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)

        # Diretorio de musicas
        os.chdir("./songs")

        # Carrega a lista de faixas e insere cada uma na playlist
        songtracks = os.listdir()
        for track in songtracks:
            self.playlist.insert(END, track)

        # ------------- UPLOAD DE ARQUIVO ----------------------
        # Frame com os campos de upload de arquivo .txt
        uploadFrame = LabelFrame(
            self.window,
            text="Upload the input from a .txt file here:",
            font=(
                "helvetica",
                9
            ),
            fg="black"
        )
        uploadFrame.place(
            x=0,
            y=150,
            width=635,
            height=75
        )

        # Campo para o nome do arquivo a ser salvo
        save_file_name_label = Label(uploadFrame, text="Save song as:")
        save_file_name_label.place(x=10, y=10, width=75, height=25)
        save_file_name_field = Entry(uploadFrame)
        save_file_name_field.place(x=90, y=10, width=342, height=25)

        # Funcao que traduz o conteudo de um .txt em um Score
        def uploadAndParseFromFile():
            # abre janela pedindo pelo arquivo e o valida
            name_to_parse = tkifd.askopenfilename()
            if (name_to_parse == None) or (name_to_parse == ""):
                self.error_message.set("Must enter name to save file as")
                return
            self.error_message.set("")

            # abre o arquivo e le
            file_to_parse = open(name_to_parse)
            text_to_parse = file_to_parse.read()

            # inicia o parser e traduz o arquivo lido num Score
            music_parser = MusicParser()
            self.stream = music_parser.parseInput(text_to_parse)

            # salva Score para arquivo de nome lido do campo
            file_name = save_file_name_field.get() + ".mid"
            self.stream.write('midi', fp=file_name)
            self.playlist.insert(END, file_name)

        # Botao de upload/salvamento do arquivo
        parse_file_button = Button(
            uploadFrame, text='Parse from File', command=uploadAndParseFromFile)
        parse_file_button.place(x=440, y=10, width=95, height=25)

        # ------------- INPUT DE TEXTO ----------------------
        # Frame com os campos de entrada de texto
        inputFrame = LabelFrame(
            self.window,
            text="Write your text input here:",
            font=(
                "helvetica",
                9
            ),
            fg="black"
        )
        inputFrame.place(
            x=0,
            y=230,
            width=635,
            height=150
        )

        # Campo para o texto de entrada
        text_input_label = Label(inputFrame, text="Text input:")
        text_input_label.place(x=22, y=5, width=75, height=25)
        text_input_field = Text(inputFrame)
        text_input_field.place(x=100, y=10, width=430, height=60)

        # Campo para o nome do arquivo a ser salvo
        file_name_label = Label(inputFrame, text="Save song as:")
        file_name_label.place(x=15, y=80, width=75, height=25)
        file_name_field = Entry(inputFrame)
        file_name_field.place(x=100, y=80, width=430, height=25)

        # Funcao de parsing do texto de entrada
        def parseTextEntry():
            # pega o texto a ser convertido do campo e o valida
            text_to_parse = text_input_field.get("1.0", END)
            if (text_to_parse == None) or (text_to_parse == "\n"):
                self.error_message.set("Must enter text to parse")
                return

            # pega o nome inicial do arquivo do campo e o valida
            file_name_start = file_name_field.get()
            if (file_name_start == None) or (file_name_start == ""):
                self.error_message.set("Must enter name to save file as")
                return
            self.error_message.set("")

            # inicia o parser e traduz o texto em um Score
            music_parser = MusicParser()
            self.stream = music_parser.parseInput(text_to_parse)

            # adiciona a extensao ao nome do arquivo e escreve o Score nele
            file_name = file_name_start + ".mid"
            self.stream.write('midi', fp=file_name)

            # adiciona o arquivo na playlist
            self.playlist.insert(END, file_name)

        # Botao de parsing do texto de entrada
        parse_song_button = Button(
            inputFrame, text='Parse song', command=parseTextEntry)
        parse_song_button.place(x=540, y=80, width=75, height=25)

        # Messagem de erro, caso tenha algum.
        error_label = Label(
            self.window,
            textvariable=self.error_message,
            fg="red"
        )
        error_label.place(x=10, y=390, width=200, height=20)

    # funcao que toca a musica
    def playSong(self):
        # pega a musica atualmente selecionada da playlist
        current_song = self.playlist.get(ACTIVE)
        music = pygame.mixer.music

        # seta os textos
        self.track.set(current_song)
        self.status.set("-Playing")

        # inicia a reproducao
        music.load(current_song)
        music.play()

    # para a musica
    def stopSong(self):
        self.status.set("-Stopped")
        pygame.mixer.music.stop()

    # pausa a musica
    def pauseSong(self):
        self.status.set("-Paused")
        pygame.mixer.music.pause()

    # despausa a musica
    def unpauseSong(self):
        self.status.set("-Playing")
        pygame.mixer.music.unpause()

def main():
    window = Tk()
    MusicPlayer(window)
    window.mainloop()

if __name__ == "__main__":
    main()
