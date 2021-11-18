
#================#
#    IMPORTS     #
#================#

# Internal imports
from music import *

# External imports
from tkinter import *
from tkinter import filedialog as tkifd
import pygame
import os


class MusicPlayer:
    def __init__(self, window):

        self.window = window
        self.window.title("Player")
        self.window.geometry("1000x320+200+200")

        pygame.init()
        pygame.mixer.init()

        self.track = StringVar()
        self.status = StringVar()

        trackframe = LabelFrame(
            self.window,
            text="Song Track",
            font=(
                "times new roman",
                15,
                "bold"
            ),
            bg="Navyblue",
            fg="white",
            bd=5,
            relief=GROOVE
        )
        trackframe.place(
            x=0,
            y=0,
            width=600,
            height=100
        )

        songtrack = Label(
            trackframe,
            textvariable=self.track,
            width=20,
            font=(
                "times new roman",
                24,
                "bold"
            ),
            bg="Orange",
            fg="gold"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=5
        )

        trackstatus = Label(
            trackframe,
            textvariable=self.status,
            font=(
                "times new roman",
                24,
                "bold"
            ),
            bg="orange",
            fg="gold"
        ).grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )

        buttonframe = LabelFrame(
            self.window,
            text="Control Panel",
            font=(
                "times new roman",
                15,
                "bold"
            ),
            bg="grey",
            fg="white",
            bd=5,
            relief=GROOVE
        )
        buttonframe.place(
            x=0,
            y=100,
            width=600,
            height=100
        )

        playbtn = Button(
            buttonframe,
            text="PLAYSONG",
            command=self.playsong,
            width=10,
            height=1,
            font=(
                "times new roman",
                16,
                "bold"
            ),
            fg="navyblue",
            bg="pink"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=5
        )
        playbtn = Button(
            buttonframe,
            text="PAUSE",
            command=self.pausesong,
            width=8,
            height=1,
            font=(
                "times new roman",
                16,
                "bold"
            ),
            fg="navyblue",
            bg="pink"
        ).grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )
        playbtn = Button(
            buttonframe,
            text="UNPAUSE",
            command=self.unpausesong,
            width=10,
            height=1,
            font=(
                "times new roman",
                16,
                "bold"
            ),
            fg="navyblue",
            bg="pink"
        ).grid(
            row=0,
            column=2,
            padx=10,
            pady=5
        )
        playbtn = Button(
            buttonframe,
            text="STOPSONG",
            command=self.stopsong,
            width=10,
            height=1,
            font=(
                "times new roman",
                16,
                "bold"
            ),
            fg="navyblue",
            bg="pink"
        ).grid(
            row=0,
            column=3,
            padx=10,
            pady=5
        )

        songsframe = LabelFrame(
            self.window,
            text="Song Playlist",
            font=(
                "times new roman",
                15,
                "bold"),
            bg="grey",
            fg="white",
            bd=5,
            relief=GROOVE)
        songsframe.place(x=600, y=0, width=400, height=200)

        scrol_y = Scrollbar(songsframe, orient=VERTICAL)
        self.playlist = Listbox(
            songsframe,
            yscrollcommand=scrol_y.set,
            selectbackground="gold",
            selectmode=SINGLE,
            font=(
                "times new roman",
                12,
                "bold"),
            bg="silver",
            fg="navyblue",
            bd=5,
            relief=GROOVE)

        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)

        os.chdir("./songs")
        songtracks = os.listdir()
        for track in songtracks:
            self.playlist.insert(END, track)

        name_label = Label(self.window, text="File name")
        name_label.place(x=0, y=200, width=75, height=20)
        name_entry = Entry(self.window)
        name_entry.place(x=75, y=200, width=525, height=20)

        song_label = Label(self.window, text="Song input")
        song_label.place(x=0, y=220, width=75, height=20)
        song_text = Text(self.window)
        song_text.place(x=75, y=220, width=525, height=100)

        def parseTextEntry():
            text_to_parse = song_text.get("1.0", END)
            if (text_to_parse == None) or (text_to_parse == ""):
                return
            file_name_start = name_entry.get()
            if (file_name_start == None) or (file_name_start == ""):
                return
            music_parser = MusicParser()
            stream = music_parser.parseInput(text_to_parse)
            file_name = file_name_start + ".mid"
            stream.write('midi', fp=file_name)
            self.playlist.insert(END, file_name)

        parse_song_button = Button(text='Parse song', command=parseTextEntry)
        parse_song_button.place(x=610, y=200, width=75, height=20)

        def parseFile():
            name_to_parse = tkifd.askopenfilename()
            if (name_to_parse == None) or (name_to_parse == ""):
                return
            file_to_parse = open(name_to_parse)
            text_to_parse = file_to_parse.read()
            print(text_to_parse)
            music_parser = MusicParser()
            stream = music_parser.parseInput(text_to_parse)
            file_name = name_entry.get() + ".mid"
            stream.write('midi', fp=file_name)
            self.playlist.insert(END, file_name)

        parse_file_button = Button(text='Parse file', command=parseFile)
        parse_file_button.place(x=610, y=230, width=75, height=20)

    def playsong(self):
        self.track.set(self.playlist.get(ACTIVE))
        self.status.set("-Playing")
        pygame.mixer.music.load(self.playlist.get(ACTIVE))
        pygame.mixer.music.play()

    def stopsong(self):
        self.status.set("-Stopped")
        pygame.mixer.music.stop()

    def pausesong(self):
        self.status.set("-Paused")
        pygame.mixer.music.pause()

    def unpausesong(self):
        self.status.set("-Playing")
        pygame.mixer.music.unpause()


def main():
    window = Tk()
    MusicPlayer(window)
    window.mainloop()


if __name__ == "__main__":
    main()
