import tkinter as tk
import logic
from tkinter import font 

BGC = '#86B2A6'
DG = '#3D806E'

class App:
    def __init__(self,screen):
        #INITIALIZE WIDGETS AND MEMBER VARIBALES
        self.title_font = font.Font(family='Times New Roman', size = 30, weight = 'bold')
        self.font = font.Font(family='TkDefaultFont', size = 16)
        self.screen = screen
        self.sp = ''
        self.names = []
        self.ids = []
        self.listbox = tk.Listbox(self.screen,width = 70,height=25, bg=BGC,bd=0,justify='center',selectmode='single')
        
        #SET UP LOGIN SCREEN ATTRIBUTES AND WIDGETS
        screen.title("Spotiy Playgen")
        screen.geometry('700x700')
        screen.configure(bg=BGC)
        welcome_text = tk.Label(text = 'Welcome to Spotify Playgen!', bg = BGC, font=self.title_font)
        welcome_text.pack(pady = 4)
        self.listbox.pack(fill='y',pady=15)

        self.home_screen()
        self.toggle_playlist_widgets('')


    def home_screen(self):
        def get_artists(): self.selection_made('top artists')
        def get_songs(): self.selection_made('top songs')
        def get_recents(): self.selection_made('recently played songs')
        
        navbar = tk.Frame(self.screen,bg='#eeeeee')
        artist_button = tk.Button(navbar, text='Top Artists',highlightbackground=BGC, activebackground='#dddddd',width=22,command=get_artists)
        song_button = tk.Button(navbar, text='Top Songs',highlightbackground=BGC, activebackground='#dddddd',width=22, command=get_songs)
        recent_button = tk.Button(navbar, text='Recently Played',highlightbackground=BGC, activebackground='#dddddd',width=22,command=get_recents)

        artist_button.pack(side = 'left')
        song_button.pack(side = 'left')
        recent_button.pack(side = 'left')

        navbar.pack()

    def selection_made(self,selection):
        data = logic.handle_selection(selection)
        self.sp = data['sp']
        self.names = data['names']
        self.ids = data['ids']
        self.display_selection(selection)


    def display_selection(self,selection):
        self.listbox.delete(0,'end')
        for i in self.names:
            self.listbox.insert(tk.END,i)
        self.toggle_playlist_widgets(selection)


    def get_playlist_widgets(self,selection):
        menu = tk.Frame(self.screen,bg='#3D806E')
        playlist_label = tk.Label(menu, text='',bg='#3D806E')
        playlist_label.pack()
        
        title_frame = tk.Frame(menu,bg='#3D806E')
        title_label = tk.Label(title_frame,text = 'Title:            ',font=self.font,fg='white',bg='#3D806E')
        title_field = tk.Entry(title_frame,width=22,borderwidth=0,highlightbackground='#3D806E',highlightthickness=2)
        title_label.pack(side='left')
        title_field.pack(side='left',padx=10)
        title_clear_btn = tk.Button(title_frame,text='Clear',command= lambda: title_field.delete(0,'end'),highlightbackground='#3D806E')
        title_clear_btn.pack(side='right')
        title_frame.pack(pady=4)

        des_frame = tk.Frame(menu,bg='#3D806E')
        des_label = tk.Label(des_frame,text = 'Description:',font=self.font,fg='white',bg='#3D806E')
        des_field = tk.Entry(des_frame,width=22,borderwidth=0,highlightbackground='#3D806E',highlightthickness=2)
        des_label.pack(side='left')
        des_field.pack(side='left',padx=10)
        des_clear_btn = tk.Button(des_frame,text='Clear',command= lambda: des_field.delete(0,'end'),highlightbackground='#3D806E')
        des_clear_btn.pack(side='right')
        des_frame.pack(pady=4)

        space_label = tk.Label(menu, text='',bg='#3D806E',height=100000,font=self.font,fg='red')

        def make_playlist():
            title,des = title_field.get(), des_field.get()
            if title != '':
                logic.create_playlist(self.sp,selection,title,des,self.ids)
                space_label.config(text= '')
            else:
                space_label.config(text= 'Please input a title!')
        
        playlist_btn = tk.Button(menu, text='Create/add to playlist!', command = make_playlist,width=44,bd=0,highlightbackground='#3D806E')
        playlist_btn.pack(pady=4)
        space_label.pack(pady=4)
        return menu


    def toggle_playlist_widgets(self,selection):
        self.get_playlist_widgets(selection).pack(fill='both')

     
def main():
    screen = tk.Tk()
    App(screen)
    screen.mainloop()

if __name__ == '__main__':
    main()

