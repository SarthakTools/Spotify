import os, cProfile, pygame, time, random, threading
from tkinter import BOTH, LEFT, RIGHT, TOP, BOTTOM, X, Y, CENTER
import customtkinter as ct
from CTkXYFrame import CTkXYFrame
from PIL import Image
from mutagen.mp3 import MP3
from extract_info.extract_artist import get_artist
from ctypes import windll
from CTkMessagebox import CTkMessagebox

ct.set_default_color_theme("green")
ct.set_appearance_mode("dark")

class IntroPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Spotfiy - A modern music player built with Python")
        self.root.geometry("550x300")
        self.root.iconbitmap("images\\spotify.ico")
        self.root.overrideredirect(True)
        
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        spotify_image = ct.CTkImage(Image.open(os.path.join(image_path, "spotify.png")), size=(90, 90))

        ct.CTkLabel(self.root, text=" Spotify", image=spotify_image, compound=LEFT, font=("Poppins", 70, "bold")).pack(padx=10, pady=120, anchor="center")
    
        self.text = ct.CTkLabel(self.root, text="Please wait...The First launch of the app may take longer...", font=("IBM Plex Sans", 15))
        self.progressbar = ct.CTkProgressBar(self.root, orientation="horizontal", width=300, mode="determinate", determinate_speed=0.35, 
                                             fg_color="white", height=10, progress_color="#1ED765", corner_radius=0)
        self.progressbar.pack(side=BOTTOM, fill=X)
        self.text.pack(side=BOTTOM, anchor="center")
        
        self.progressbar.set(0)
        self.progressbar.start()

        self.thread = threading.Thread(target=self.loading)
        self.thread.start()
        self.set_appwindow(self.root)
        self.center_window(self.root)

    def loading(self):
        time.sleep(3)
        self.text.configure(text="")
        self.text.configure(text="Please wait.....The First launch of the app may take longer...")
        self.progressbar.stop()
        self.progressbar.set(100)
        self.main()
    
    def center_window(self, win):
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def set_appwindow(self, mainWindow): 
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        hwnd = windll.user32.GetParent(mainWindow.winfo_id())
        stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        stylew = stylew & ~WS_EX_TOOLWINDOW
        stylew = stylew | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)   
        mainWindow.wm_withdraw()
        mainWindow.after(10, lambda: mainWindow.wm_deiconify())

    def main(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        LoginPage(root)

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(False)
        self.root.title("Spotify - Login to play songs for free")
        self.root.geometry("1000x600+200+40")
        self.root.configure(fg_color="#1b1717")
        self.root.resizable(False, False)

        Height = 12
        Width = 300
        icon_size = 35

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        spotify_image = ct.CTkImage(Image.open(os.path.join(image_path, "spotify2.png")), size=(100, 75))
        email_image = ct.CTkImage(Image.open(os.path.join(image_path, "mail.png")), size=(icon_size, icon_size))
        password_image = ct.CTkImage(Image.open(os.path.join(image_path, "lock.png")), size=(icon_size, icon_size))

        self.loginframe = ct.CTkFrame(self.root, fg_color="#111", corner_radius=15)

        ct.CTkLabel(self.loginframe, text="Spotify", image=spotify_image, compound=LEFT, font=("monospace", 40, "bold"), text_color="white").pack(pady=30, side=TOP, anchor="nw", padx=100)

        ct.CTkLabel(self.loginframe, text="Music for everyone", font=("monospace", 30, "bold"), text_color="white").pack(pady=15)

        self.username_frame = ct.CTkFrame(self.loginframe, height=0, width=0, fg_color="#333")
        ct.CTkLabel(self.username_frame, text="", image=email_image, fg_color="transparent", corner_radius=0).pack(side=LEFT, padx=10)
        self.usernameInput = ct.CTkEntry(self.username_frame, placeholder_text="Email or username", font=("monospace", 20, "bold"), 
                                         height=Height, width=Width, text_color="#f3f3f3", fg_color="transparent", border_width=0)
        self.usernameInput.pack(side=LEFT, ipady=15)
        self.username_frame.pack(pady=10, ipadx=10, ipady=2)

        self.password_frame = ct.CTkFrame(self.loginframe, height=0, width=0, fg_color="#333")
        ct.CTkLabel(self.password_frame, text="", image=password_image, fg_color="transparent", corner_radius=0).pack(side=LEFT, padx=10)
        self.passwordInput = ct.CTkEntry(self.password_frame, placeholder_text="Password", font=("monospace", 20, "bold"), 
                                         height=Height, width=Width, text_color="white", fg_color="transparent", border_width=0, show="*")
        self.passwordInput.pack(side=LEFT, ipady=15)
        self.password_frame.pack(pady=5, ipadx=10, ipady=2)

        self.loginBtn = ct.CTkButton(self.loginframe, text="LOG IN", text_color="black", font=("monospace", 20, "bold"), fg_color="white", corner_radius=10,
                                     hover_color="#dcdada", command=self.login)
        self.loginBtn.pack(side=TOP, fill=X, padx=55, pady=10, ipady=10)

        self.loginframe.pack(side=TOP, fill=BOTH, expand=True, pady=40, padx=260)

        progressbar_frame = ct.CTkFrame(self.loginframe, height=0, width=0, fg_color="transparent")
        self.progressbar = ct.CTkProgressBar(self.loginframe,  orientation="horizontal", mode="determinate", determinate_speed=0.6, 
                                             fg_color="white", height=5, progress_color="#1ED765", corner_radius=0, )
        self.progressbar.set(0)
        self.progressbar.pack(side=BOTTOM, fill=X)
        progressbar_frame.pack(side=BOTTOM, fill=X)

        self.thread = threading.Thread(target=self.loading)

    def login(self):
        username = self.usernameInput.get()
        password = self.passwordInput.get()

        if len(username) == 0 or len(password) == 0:
            CTkMessagebox(title="Error", message=" Username or Password can't be empty ", icon="cancel", font=("monospace", 15, "bold"), text_color="white", wraplength=600)
        else:
            if len(password) > 8:
                CTkMessagebox(title="Error", message=" Password should not be more than 8 digits", icon="cancel", font=("monospace", 15, "bold"), text_color="white", wraplength=600)
            else:
                with open("data.txt", "w") as f:
                    user_name = username.split("@")[0]
                    data = {"name" : user_name, "password" : password, "email" : f"{user_name}@spotify.com"}
                    f.write(str(data))

                self.progressbar.start()
                self.thread.start()

    def loading(self):
        time.sleep(1.5)
        self.progressbar.stop()
        self.progressbar.set(100)

        for widget in self.root.winfo_children():
            widget.destroy()

        app = Spotify(self.root)
        add_music(app)
    
class Spotify:
    def __init__(self, root):
        self.root = root

        self.root.title("Spotify")
        self.root.geometry("1300x700")
        self.root.minsize(1300, 700)
        self.bg_color = "#202124"
        self.root.configure(fg_color=self.bg_color)
        self.root.resizable(True, True)
        # pywinstyles.apply_style(self, style="acrylic")

        # Load images from the images folder
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.spotify_img = ct.CTkImage(Image.open(os.path.join(image_path, "spotify.png")), size=(50, 50))
        self.home_img = ct.CTkImage(Image.open(os.path.join(image_path, "home.png")), size=(25, 25))
        self.discover_img = ct.CTkImage(Image.open(os.path.join(image_path, "song.png")), size=(25, 25))
        self.rise_img = ct.CTkImage(Image.open(os.path.join(image_path, "rise.png")), size=(25, 20))
        self.rise_img2 = ct.CTkImage(Image.open(os.path.join(image_path, "search2.png")), size=(20, 20))
        self.audiobooks_img = ct.CTkImage(Image.open(os.path.join(image_path, "headphones.png")), size=(25, 25))
        self.audiobooks_img2 = ct.CTkImage(Image.open(os.path.join(image_path, "bookopen.png")), size=(45, 45))
        self.settings_img = ct.CTkImage(Image.open(os.path.join(image_path, "settings.png")), size=(25, 25))
        self.search_img = ct.CTkImage(Image.open(os.path.join(image_path, "search.png")), size=(30, 30))
        self.add_img = ct.CTkImage(Image.open(os.path.join(image_path, "plus.png")), size=(33, 33))
        self.delete_img = ct.CTkImage(Image.open(os.path.join(image_path, "delete2.png")), size=(28, 28))
        self.edit_img = ct.CTkImage(Image.open(os.path.join(image_path, "edit.png")), size=(28, 28))
        self.favourite_img3 = ct.CTkImage(Image.open(os.path.join(image_path, "star.png")), size=(28, 28))
        self.eyes_icon_open = ct.CTkImage(Image.open(os.path.join(image_path, "eyes_open.png")), size=(20, 20))
        self.eyes_icon_closed =  ct.CTkImage(Image.open(os.path.join(image_path, "eyes_closed.png")), size=(20, 20))
        self.profile_img = ct.CTkImage(Image.open(os.path.join(image_path, "avator2.png")), size=(35, 35)) # avator profile
        self.avator_image = ct.CTkImage(Image.open(os.path.join(image_path, "avator2.png")), size=(155, 155)) # avator profile

        self.nav_frame = ct.CTkFrame(self.root, fg_color="#141517")

        self.spotify_label = ct.CTkLabel(self.nav_frame, text=" Spotify      ", text_color="white", image=self.spotify_img, compound=LEFT,
                                          font=("Poppins", 30))
        self.spotify_label.pack(side=TOP, padx=10, pady=5)

        ct.CTkLabel(self.nav_frame, text="").pack(pady=5)

        self.search = ct.CTkButton(self.nav_frame, text="Search", width=50, height=40, fg_color="transparent", hover_color="#444",
                                  corner_radius=10, image=self.search_img, font=("Montserrat", 20), text_color="white", anchor="w", command=lambda: self.select_frame_name("search"))
        self.search.pack(side=TOP, pady=5, ipady=5, padx=5, fill=X)

        ct.CTkButton(self.nav_frame, text="", fg_color="transparent", hover_color="#141517", text_color="white").pack(side=TOP, pady=10, fill=X)

        self.home = ct.CTkButton(self.nav_frame, text="Home", width=50, height=40, fg_color="transparent", hover_color="#444",
                                  corner_radius=10, image=self.home_img, font=("Montserrat", 20), text_color="white", anchor="w", command=lambda: self.select_frame_name("home"))
        self.home.pack(side=TOP, pady=5, ipady=5, padx=5, fill=X)

        self.artists = ct.CTkButton(self.nav_frame, text="Artists", width=50, height=40, fg_color="transparent", hover_color="#444",
                                  corner_radius=10, image=self.discover_img, font=("Montserrat", 20), text_color="white", anchor="w", command=lambda: self.select_frame_name("artists"))
        self.artists.pack(side=TOP, pady=5, ipady=5, padx=5, fill=X)

        self.trending = ct.CTkButton(self.nav_frame, text="Trending", width=50, height=40, fg_color="transparent", hover_color="#444",
                                  corner_radius=10, image=self.rise_img, font=("Montserrat", 20), text_color="white", anchor="w", command=lambda: self.select_frame_name("trending"))
        self.trending.pack(side=TOP, pady=5, ipady=5, padx=5, fill=X)

        self.audiobooks = ct.CTkButton(self.nav_frame, text="AudioBooks", width=50, height=40, fg_color="transparent", hover_color="#444",
                                  corner_radius=10, image=self.audiobooks_img, font=("Montserrat", 20), text_color="white", anchor="w", command=lambda: self.select_frame_name("audiobooks"))
        self.audiobooks.pack(side=TOP, pady=5, ipady=5, padx=5, fill=X)

        self.favourites_btn = ct.CTkButton(self.nav_frame, text="Favourites", width=50, height=40, fg_color="transparent", hover_color="#444",
                                  corner_radius=10, image=self.favourite_img3, font=("Montserrat", 20), text_color="white", anchor="w", command=lambda: self.select_frame_name("favourites"))
        self.favourites_btn.pack(side=TOP, pady=5, ipady=5, padx=5, fill=X)

        self.settings = ct.CTkButton(self.nav_frame, text="Settings", width=50, height=40, fg_color="transparent", hover_color="#444",
                                  corner_radius=10, image=self.settings_img, font=("Montserrat", 20), text_color="white", anchor="w", command=lambda: self.select_frame_name("settings"))
        self.settings.pack(side=BOTTOM, pady=10, ipady=5, padx=5, fill=X)

        self.nav_frame.pack(side=LEFT, fill=Y)

        self.main = ct.CTkFrame(self.root, corner_radius=0, fg_color=self.bg_color)
        self.main.pack(fill=BOTH, expand=True)

        # Create all the frames for every tab inside the main frame
        self.color_home_frame = "#333"

        # Search frame code here .........................
        self.search_frame = ct.CTkFrame(self.main, corner_radius=0, fg_color="#555")
        self.search_label = ct.CTkLabel(self.search_frame, text="", image=self.search_img)

        self.search_box = ct.CTkEntry(self.search_frame, font=("IBM Plex Sans", 23), placeholder_text="What do you want to play today ?", placeholder_text_color="#a5a5a5",
                                       corner_radius=10, border_width=0, fg_color=self.bg_color, text_color="white")
        self.search_box.pack(side=TOP, fill=X, ipady=15, padx=20, pady=20)
        self.search_box.bind("<KeyRelease>", self.on_button_release)

        self.like_that_entry = ct.CTkEntry(self.search_frame, width=0, height=0, fg_color="#555", text_color="#555", bg_color="#555", border_width=0)
        self.like_that_entry.pack(side=BOTTOM, fill=X)
        self.search_frame.bind("<Button-1>", lambda event: self.like_that_entry.focus())

        self.all_songs_name = ['Arcade', 'Can We Kiss Forever', 'Faded', 
                               'Fearless', 'Hymn For The Weekend', 'Infinity', 'Into Your Arms', 'Khairiyat', 
                               'Let Me Down Slowly', 'Phir Mohabbat', 'Raghupathi Raghava Rajaram', 
                               'Ram Aayenge', 'Safari', 'See You Again','Tere Sang Yaara',
                                 'Tu Jo Mila', 'Tum Hi Ho', 'Chhod Diya']

        self.searching_frame = ct.CTkFrame(self.search_frame, fg_color="#333")
        self.searching_frame.pack(side=TOP, fill=X, padx=20, pady=10)

        #----------------------------------------------------------------------------------------------------

        self.home_frame = CTkXYFrame(self.main, corner_radius=0, fg_color=self.color_home_frame)

        self.home_label = ct.CTkLabel(self.home_frame, text="Home", font=("Poppins", 50), text_color="white")
        self.home_label.pack(anchor="nw", side=TOP, padx=20)

        self.discover_frame = ct.CTkFrame(self.main, corner_radius=0, fg_color="#1f1e42")
        self.popular_frame = ct.CTkFrame(self.main, corner_radius=0, fg_color=self.color_home_frame)
        self.audiobooks_frame = ct.CTkFrame(self.main, corner_radius=0, fg_color=self.color_home_frame)
        self.settings_frame = ct.CTkFrame(self.main, corner_radius=0, fg_color=self.color_home_frame)
        self.favourites_frame = ct.CTkFrame(self.main, corner_radius=0, fg_color=self.color_home_frame)

        ##################### ---------- Artists code ---------------- ###################################

        self.artist_frame = ct.CTkScrollableFrame(self.discover_frame, fg_color="transparent")
        singer_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "singersImage")
        ariijt_image = ct.CTkImage(Image.open(os.path.join(singer_image_path, "arijit_singh.png")), size=(250, 250))
        gayathri_image = ct.CTkImage(Image.open(os.path.join(singer_image_path, "g_gayathri_devi.png")), size=(250, 250))
        kk_image = ct.CTkImage(Image.open(os.path.join(singer_image_path, "kk.png")), size=(250, 250))
        atif_alsam_image = ct.CTkImage(Image.open(os.path.join(singer_image_path, "atif_aslam.png")), size=(250, 250))
        alisha_chinai_image = ct.CTkImage(Image.open(os.path.join(singer_image_path, "alisha_chinai.png")), size=(250, 250))
        sachet_tandon_image = ct.CTkImage(Image.open(os.path.join(singer_image_path, "sachet_tandon.png")), size=(250, 250))
        pamphara_thakur_image = ct.CTkImage(Image.open(os.path.join(singer_image_path, "pamphara_thakur.png")), size=(250, 250))
        swati_mishra_image = ct.CTkImage(Image.open(os.path.join(singer_image_path, "swati_mishra.png")), size=(250, 250))
        alan_walker_image = ct.CTkImage(Image.open(os.path.join(singer_image_path, "alan_walker.png")), size=(250, 250))
        alec_benjamin_image = ct.CTkImage(Image.open(os.path.join(singer_image_path, "alec_benjamin.png")), size=(250, 250))
        duncan_laurence_image = ct.CTkImage(Image.open(os.path.join(singer_image_path, "duncan_laurence.png")), size=(250, 250))
        kina_image = ct.CTkImage(Image.open(os.path.join(singer_image_path, "kina.png")), size=(250, 250))
        # uma_mohan_image = ct.CTkImage(Image.open(os.path.join(singer_image_path, "uma_mohan.png")), size=(250, 250))

        ct.CTkLabel(self.discover_frame, text="Artists", font=("Heleventica", 55, "bold")).pack(side=TOP, anchor="ne", fill=X, pady=5)

        row_1 = ct.CTkFrame(self.artist_frame, fg_color="transparent")
        arijit_singh = ct.CTkLabel(row_1, text="Arijit Singh", font=("IBM Plex Sans", 20, "bold"), image=ariijt_image, compound=TOP)
        arijit_singh.pack(side=LEFT, padx=25)
        g_gayahatri = ct.CTkLabel(row_1, text="G. Gayathri Devi", font=("IBM Plex Sans", 20, "bold"), image=gayathri_image, compound=TOP)
        g_gayahatri.pack(side=LEFT, padx=25)
        kk = ct.CTkLabel(row_1, text="Krishnakumar Kunnath", font=("IBM Plex Sans", 20, "bold"), image=kk_image, compound=TOP)
        kk.pack(side=LEFT, padx=25)
        atif_alsam = ct.CTkLabel(row_1, text="Atif Aslam", font=("IBM Plex Sans", 20, "bold"), image=atif_alsam_image, compound=TOP)
        atif_alsam.pack(side=LEFT, padx=25)
        row_1.pack(fill=X, side=TOP)

        row_2 = ct.CTkFrame(self.artist_frame, fg_color="transparent")
        alisha_chinai = ct.CTkLabel(row_2, text="Alisha Chinai", font=("IBM Plex Sans", 20, "bold"), image=alisha_chinai_image, compound=TOP)
        alisha_chinai.pack(side=LEFT, padx=25)
        sachet_tandon = ct.CTkLabel(row_2, text="Sachet Tandon", font=("IBM Plex Sans", 20, "bold"), image=sachet_tandon_image, compound=TOP)
        sachet_tandon.pack(side=LEFT, padx=25)
        pamphara_thakur = ct.CTkLabel(row_2, text="Parampara Thakur", font=("IBM Plex Sans", 20, "bold"), image=pamphara_thakur_image, compound=TOP)
        pamphara_thakur.pack(side=LEFT, padx=25)
        swati_mishra = ct.CTkLabel(row_2, text="Swati Mishra", font=("IBM Plex Sans", 20, "bold"), image=swati_mishra_image, compound=TOP)
        swati_mishra.pack(side=LEFT, padx=25)

        row_2.pack(fill=X, side=TOP, pady=20)

        row_3 = ct.CTkFrame(self.artist_frame, fg_color="transparent")

        alan_walker = ct.CTkLabel(row_3, text="Alan Walker", font=("IBM Plex Sans", 20, "bold"), image=alan_walker_image, compound=TOP)
        alan_walker.pack(side=LEFT, padx=25)
        alec_benjemin = ct.CTkLabel(row_3, text="Alec Benjamin", font=("IBM Plex Sans", 20, "bold"), image=alec_benjamin_image, compound=TOP)
        alec_benjemin.pack(side=LEFT, padx=25)
        duncan_laurence = ct.CTkLabel(row_3, text="Duncan Laurence", font=("IBM Plex Sans", 20, "bold"), image=duncan_laurence_image, compound=TOP)
        duncan_laurence.pack(side=LEFT, padx=25)
        kina = ct.CTkLabel(row_3, text="Kina Cosper", font=("IBM Plex Sans", 20, "bold"), image=kina_image, compound=TOP)
        kina.pack(side=LEFT, padx=25)

        row_3.pack(side=TOP, fill=X)
    
        self.artist_frame.pack(side=TOP, fill=BOTH, expand=True, padx=20, pady=40)


        # settings frame code ##################################

        self.profile_frame = ct.CTkFrame(self.settings_frame, fg_color=self.bg_color)
        self.profile_button = ct.CTkButton(self.profile_frame, text="", width=0, corner_radius=0, fg_color=self.bg_color, hover_color="#333", image=self.profile_img)
        self.profile_button.pack(side=RIGHT)

        self.username = ct.CTkLabel(self.profile_frame, text="Username", font=("IBM Plex Sans", 25, "bold"))
        self.username.pack(anchor="center", side=LEFT, padx=15)

        self.profile_frame.pack(side=TOP, fill=X, ipady=10, padx=5, pady=2, ipadx=10)

        # settings control frame all the settings
        self.settings_control_frame = ct.CTkFrame(self.settings_frame, fg_color=self.bg_color)
    
        ct.CTkLabel(self.settings_control_frame, text="Settings", font=("IBM Plex Sans", 40, "bold")).pack(side=TOP, anchor="nw", padx=20, pady=20)
        
        # auto update frame
        self.update_frame = ct.CTkFrame(self.settings_control_frame)
        self.update_btn = ct.CTkSwitch(self.update_frame, text="", switch_height=30, switch_width=60, font=("Poppins", 40, "bold"))
        upadte_text = ct.CTkLabel(self.update_frame, text="Auto-Update", font=("IBM Plex Sans", 25, "bold"))
        upadte_text.pack(side=LEFT, padx=20)
        self.update_btn.pack(side=RIGHT, padx=2)
        self.update_frame.pack(side=TOP, fill=X, padx=15, ipady=10)
        self.update_frame.bind("<Button-1>", self.toggle_update)

        # account frame 
        self.account_frame = ct.CTkFrame(self.settings_control_frame)

        with open("data.txt", "r") as f:
            data = f.readline().strip()

            try: data_dict = eval(data)
            except Exception: data_dict = {}

            email_value = data_dict.get("email")
            password_value = data_dict.get("password")

            self.email = data_dict.get("email") if email_value else "username@spotify.com"
            self.password = data_dict.get("password") if password_value else "12345678"

        self.account_details_frame = ct.CTkFrame(self.account_frame, fg_color="transparent")
        ct.CTkLabel(self.account_details_frame, text="Account", font=("Poppins", 30, "bold")).pack(side=TOP, anchor="nw", padx=10)
        
        details_frame = ct.CTkFrame(self.account_details_frame, fg_color="transparent")

        self.email_label = ct.CTkLabel(details_frame, text=f"Email-ID     :   {self.email}", font=("IBM Plex Sans", 20, "bold"))

        password_frame = ct.CTkFrame(details_frame, fg_color="transparent")
        self.password_label = ct.CTkLabel(password_frame, text=f"Password   :   ", font=("IBM Plex Sans", 20, "bold"))
        self.password_input = ct.CTkLabel(password_frame, font=("consolas", 20, "bold"), text="********")
        self.icon_eyes = ct.CTkButton(password_frame, text="", image=self.eyes_icon_closed, width=0, font=("consolas", 100), fg_color="transparent", hover_color=self.bg_color, command=self.show_password)
        self.password_label.pack(side=LEFT)
        self.password_input.pack(side=LEFT)
        self.icon_eyes.pack(side=LEFT, padx=5)

        self.email_label.pack(side=TOP, anchor="nw")
        password_frame.pack(side=TOP, anchor="nw")

        details_frame.pack(side=LEFT, pady=10, padx=10)
        self.account_details_frame.pack(side=LEFT, fill=BOTH, expand=True, pady=10, padx=10)

        self.photo_frame = ct.CTkLabel(self.account_frame, text="", image=self.avator_image, fg_color="transparent")
        self.photo_frame.pack(side=RIGHT, padx=40, fill=BOTH, ipadx=10, pady=10)

        self.delete_account = ct.CTkButton(details_frame, text="Delete Account", font=("Poppins", 20, "bold"), fg_color="#e15455", hover_color="#f44344", corner_radius=10, bg_color="transparent", command=self.deleteAccount)
        self.delete_account.pack(side=TOP, anchor="nw", ipady=7, pady=5)

        self.account_frame.pack(side=TOP, fill=X, padx=15, ipady=10, pady=10)
        
        # about frame 
        self.about_frame = ct.CTkFrame(self.settings_control_frame)
        
        ct.CTkLabel(self.about_frame, text="About", font=("IBM Plex Sans", 40, "bold")).pack(side=TOP, anchor="nw", padx=20, pady=20)
        ct.CTkLabel(self.about_frame, text="About      : © 2024 Spotify Limited. All rights reserved", font=("consolas", 20, "bold")).pack(side=TOP, anchor="nw", padx=20)
        ct.CTkLabel(self.about_frame, text="Version    : 1.1", font=("consolas", 20, "bold")).pack(side=TOP, anchor="nw", padx=20)
        ct.CTkLabel(self.about_frame, text="Developer  : Sarthak Singh", font=("consolas", 20, "bold")).pack(side=TOP, anchor="nw", padx=20)
    
        self.about_frame.pack(side=TOP, fill=BOTH, padx=15, pady=5, ipady=20)

        self.settings_control_frame.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=10)

        # Focus the home tab first
        self.select_frame_name("home")

        self.music_playing = None
        self.frames = {}  # Dictionary to store frames for each tab
        self.frames2 = {}  # Dictionary to store frames for each tab
        # control song frame
        
        # global stop_img, pause_img
        song_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.pause_img = ct.CTkImage(Image.open(os.path.join(song_image_path, "pause.png")), size= (35, 35))
        self.stop_img = ct.CTkImage(Image.open(os.path.join(song_image_path, "play.png")), size= (35, 35))
        self.skip_forward_img = ct.CTkImage(Image.open(os.path.join(song_image_path, "skip-forward.png")), size= (35, 35))
        self.skip_backward_img = ct.CTkImage(Image.open(os.path.join(song_image_path, "skip-back.png")), size= (35, 35))
        self.loop_img = ct.CTkImage(Image.open(os.path.join(image_path, "loop.png")), size=(36, 36))
        self.shuffle_img = ct.CTkImage(Image.open(os.path.join(image_path, "shuffle.png")), size=(28, 28))
        self.favourite_img = ct.CTkImage(Image.open(os.path.join(image_path, "myHeart.png")), size=(35, 35))
        self.favourite_img2 = ct.CTkImage(Image.open(os.path.join(image_path, "myHeart2.png")), size=(35, 35))
        song_image_path2 = os.path.join(os.path.dirname(os.path.realpath(__file__)), "songs_images")
        self.imgPlaylistFavourites = ct.CTkImage(Image.open(os.path.join(song_image_path2, "dark.png")), size=(250, 220))
        
        self.control_frame = ct.CTkFrame(self.root, corner_radius=10, fg_color="transparent")

        self.image_song_label = ct.CTkLabel(self.control_frame, text="", fg_color="#555", height=54, width=54, corner_radius=5)
        self.image_song_label.pack(side=LEFT, padx=10)

        self.slide_time_frame = ct.CTkFrame(self.control_frame, fg_color="transparent")

        self.time_elapsed_label = ct.CTkLabel(self.slide_time_frame, text="00:00", font=("Poppins", 20))
        self.time_elapsed_label.pack(side=LEFT, padx=10)

        self.music_duration_label = ct.CTkLabel(self.slide_time_frame, text="00:00", font=("Poppins", 20))
        self.music_duration_label.pack(side=RIGHT, padx=10)

        self.slider = ct.CTkSlider(self.slide_time_frame, height=20, fg_color="#4b5d4b", progress_color="#106A43", bg_color="transparent", 
                                   command=lambda event: self.slide_song(), from_=0, to=100)
        self.slider.pack(fill=X, padx=20)
        self.slider.set(0)

        self.slide_time_frame.pack(side=TOP, fill=X)

        #########################################

        # playlist frame code ---------------------

        self.audiobooks_heading_frame = ct.CTkFrame(self.audiobooks_frame, corner_radius=8, fg_color="#222")
        ct.CTkLabel(self.audiobooks_heading_frame, text=" AudioBooks", image=self.audiobooks_img2, font=("Poppins", 30, "bold"), 
                    compound=LEFT, text_color="white").pack(side=LEFT, padx=10, ipady=5, ipadx=10)
        self.audiobooks_heading_frame.pack(side=TOP, fill=X, pady=5, padx=10, ipady=10)

        self.audio_frame = ct.CTkScrollableFrame(self.audiobooks_frame)
        self.audio_frame.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)

        self.playlist_container = ct.CTkScrollableFrame(self.favourites_frame, fg_color="#202128", corner_radius=10)
        self.playlist_container.pack(fill=BOTH, expand=True, padx=5, pady=2)

        self.favourites_playlist = ct.CTkFrame(self.playlist_container, fg_color="#333")
        self.favourites_playlist.pack(side=TOP, padx=5, ipady=15, pady=5, fill=X)
        
        # --------------------- playlist code .................
        ########################################################
        # Play control frame for the control of music

        self.singer_name = ct.CTkLabel(self.control_frame, text="Singer name", font=("IBM Plex Sans", 20, "bold"), text_color="#a5a5a5")
        self.singer_name.pack(side=LEFT, padx=10)

        self.play_control_frame = ct.CTkFrame(self.control_frame, fg_color="#212228", width=0)

        self.loop = ct.CTkButton(self.play_control_frame, text="", image=self.loop_img, width=0, fg_color="transparent", command=self.loop_song)
        self.loop.pack(side=LEFT, padx=80)

        self.skip_backward = ct.CTkButton(self.play_control_frame, text="", image=self.skip_backward_img, width=0, fg_color="transparent", corner_radius=5, bg_color="transparent", command=self.play_previous_song)
        self.skip_backward.pack(side=LEFT)
        self.pause = ct.CTkButton(self.play_control_frame, text="", image=self.stop_img, width=0, fg_color="transparent", corner_radius=5, bg_color="transparent", command=self.stop_music, state="disabled")
        self.pause.pack(side=LEFT)
        self.skip_forward = ct.CTkButton(self.play_control_frame, text="", image=self.skip_forward_img, width=0, fg_color="transparent", corner_radius=5, bg_color="transparent", command=self.play_previous_song)
        self.skip_forward.pack(side=LEFT)

        self.favourite = ct.CTkButton(self.play_control_frame, text="", image=self.favourite_img, width=0, fg_color="transparent",
                                      command=self.add_favourite)
        self.favourite.pack(side=RIGHT, padx=80)
        
        self.play_control_frame.pack(side=LEFT, padx=140)

        self.control_frame.pack(side=BOTTOM, fill=X, pady=10)

        self.trends_frame = ct.CTkFrame(self.popular_frame, fg_color="#241d48", bg_color="#241d48")

        ct.CTkLabel(self.trends_frame, text="Popular ", font=("IBM Plex Sans", 40, "bold")).pack(side=TOP, anchor="nw", padx=35, pady=20)
        
        self.trending_song_frame = ct.CTkFrame(self.trends_frame, fg_color="transparent")
        trending_songs = self.generate_random_song(10)

        for i, trends in enumerate(trending_songs):
            i+=1
            ct.CTkButton(self.trending_song_frame, text=f"{i}. {trends}", font=("Poppins", 21, "normal"), 
                         anchor="w", corner_radius=10, fg_color="#3d375a", hover_color="#464d75", command=lambda song=trends: self.play_music(f"{song}.mp3")).pack(side=TOP, fill=X, ipady=10, padx=10, pady=5)

        self.trending_song_frame.pack(side=TOP, fill=X, padx=20, pady=10)
        
        self.trends_frame.pack(fill=BOTH, expand=True)

        self.all_songs = []
        self.playlists = []
        self.favourites = []
        self.previous_song = []

        self.position = 0
        self.loop = False
        self.music_scale = False
        
        self.root.bind("<space>", self.spacebar_event)
        self.open_favourites()
        self.updateFavouritePlaylistImage() 

        intital_songs = self.generate_random_song(10)
        for item in intital_songs:
            ct.CTkButton(self.searching_frame, text=f" {item}", width=20, font=("Poppins", 21, "normal"), command=lambda item=item: self.on_button_click(item), 
                        anchor="w", corner_radius=0, fg_color="#333", text_color="#c7c3c3", image=self.rise_img2, hover_color="#444").pack(fill=X, pady=0, ipady=10, padx=5)

    def deleteAccount(self):
        if os.path.exists("data.txt"):
            msg = CTkMessagebox(title="Delete Account", message=" Are you sure to delete account ? Restart the program to create new account.", icon="question", font=("monospace", 15, "bold"), text_color="white", wraplength=550, option_1="Cancel", option_2="No", option_3="Yes", width=550) 

            if msg.get() == "Yes":
                msg = CTkMessagebox(title="Delete Account", message="Your account has been deleted", icon="check", option_1="Thanks", cancel_button="circle", cancel_button_color="red") 
                if msg.get() == "Thanks":
                    os.remove("data.txt")   
                    self.root.destroy()
            else:
                pass

    def generate_random_song(self, number):
        return random.sample(self.all_songs_name, number)

    def search_filter(self, search_term):
        for widget in self.searching_frame.winfo_children():
            widget.destroy()

        if search_term == "":
            initial_fruits = self.generate_random_song(8)
            for item in initial_fruits:
                ct.CTkButton(self.searching_frame, text=f" {item}", width=20, font=("Poppins", 21, "normal"), command=lambda item=item: self.on_button_click(item), 
                        anchor="w", corner_radius=0, fg_color="#333", text_color="#c7c3c3", image=self.rise_img2, hover_color="#444").pack(fill=X, pady=0, ipady=10, padx=5)
        else:
            filtered_data = [item for item in self.all_songs_name if item.lower().startswith(search_term.lower())]
            filtered_data.sort()
            for item in filtered_data:
                ct.CTkButton(self.searching_frame, text=f" {item}", width=20, font=("Poppins", 21, "normal"), command=lambda item=item: self.on_button_click(item), 
                        anchor="w", corner_radius=0, fg_color="#333", text_color="#c7c3c3", image=self.rise_img2, hover_color="#444").pack(fill=X, pady=0, ipady=10, padx=5)

    def on_button_click(self, item):
        music_name = f"{item}.mp3"
        self.play_music(music_name)
    
    def on_button_release(self, event):
        search_term = event.widget.get()
        self.search_filter(search_term)

    def show_password(self):
        self.icon_eyes.configure(image=self.eyes_icon_open, command=self.hide_password)
        self.password_input.configure(text=self.password)

    def hide_password(self):
        self.icon_eyes.configure(image=self.eyes_icon_closed, command=self.show_password)
        self.password_input.configure(text="********")
        
    def toggle_update(self, event):
        self.update_btn.toggle()

    def playPlaylist_song(self):
        for music_name in self.favourites:
            pygame.mixer.music.load(f"songs\\{music_name}")
            pygame.mixer.music.play()
            self.insertSongImage(music_name)
            self.configure_music(music_name)
            self.previous_song.append(music_name)
            artist_name = self.get_music_info(f"songs\\{music_name}")["artist"]
            self.singer_name.configure(text=artist_name)

            if len(artist_name) > 16: 
                self.play_control_frame.pack_configure(padx=20)
            if len(artist_name) < 16: 
                self.play_control_frame.pack_configure(padx=140)

            self.favourite.pack(side=RIGHT, padx=80)

    def open_favourites(self):
        global playlist_songs_frame, music_name, image_path, title_song
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "songs_images")
        self.favourites_playlist.pack_forget()
        self.playlist_container.pack_forget()
        self.favourites_playlist_full = ct.CTkScrollableFrame(self.favourites_frame, fg_color="#222029")

        self.title_frame = ct.CTkFrame(self.favourites_playlist_full)
        self.title_frame.pack(side=TOP, fill=X)

        title_song = ct.CTkLabel(self.title_frame, text="", bg_color="transparent", corner_radius=10)
        title_song.pack(side=LEFT, pady=10)

        space = ct.CTkLabel(self.title_frame, text="")
        space.pack(side=TOP, anchor="nw", pady=20, padx=10)

        title = ct.CTkLabel(self.title_frame, text="Favourites", font=("Poppins", 50, "bold"), text_color="white")
        title.pack(side=TOP, anchor="nw", pady=20, padx=10)

        play = ct.CTkButton(self.title_frame, text="Play  ", image=self.stop_img, font=("IBM Plex Sans", 30, "bold"), text_color="white", 
                            corner_radius=60, fg_color="#2d862d", hover_color="#2c7c2c", command=self.playPlaylist_song)
        play.pack(side=TOP, anchor="nw", padx=10, ipady=10, ipadx=10)

        if len(self.favourites) > 0:
            music_name = self.favourites[0].lower().replace(" ", "_")
            music_name = music_name.split(".")
            music_name[1] = ".png"
            music_name = str(music_name[0] + music_name[1])
            title_image = ct.CTkImage(Image.open(os.path.join(image_path, f"{music_name}")), size=(250, 220))
            title_song.configure(image=title_image)

        if len(self.favourites) == 0:
            title_song.configure(image=self.imgPlaylistFavourites)

        #########################################################
        playlist_songs_frame = ct.CTkFrame(self.favourites_playlist_full, fg_color="transparent")
        
        for i in self.favourites:
            list_fav_song_frame = ct.CTkFrame(playlist_songs_frame, fg_color="#444")
            photo_name = self.favourites[0].lower().replace(" ", "_")
            photo_name = photo_name.split(".")
            photo_name[1] = ".png"
            photo_name = str(photo_name[0])
            photo = ct.CTkImage(Image.open(os.path.join(image_path, f"{music_name}")), size=(40, 40))

            songs_favourite = ct.CTkButton(list_fav_song_frame, text=i.split(".")[0], fg_color="transparent", hover_color="#444", font=("Poppins", 22, "bold"), 
                                           image=photo, compound=LEFT, text_color="white")
            songs_favourite.pack(side=LEFT, fill=X, padx=10)
            
            singer_name = ct.CTkLabel(list_fav_song_frame, text=self.get_music_info(f"songs\\{i}")["artist"], font=("Poppins", 20, "bold")) # type: ignore
            singer_name.pack(side=RIGHT, padx=20)

            list_fav_song_frame.pack(side=TOP, fill=X, expand=False, ipady=10, padx=10, pady=10, ipadx=10)
        playlist_songs_frame.pack(side=BOTTOM, fill=X, expand=True, pady=10, padx=5)
        #########################################################

        self.favourites_playlist_full.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)

    def update_songs_(self):
        global playlist_songs_frame
        i =  len(self.favourites)
        if i == 0:
            playlist_songs_frame.destroy()
        else:
            playlist_songs_frame.destroy()
            playlist_songs_frame = ct.CTkFrame(self.favourites_playlist_full, fg_color="transparent")
            for i in self.favourites:
                list_fav_song_frame = ct.CTkFrame(playlist_songs_frame, fg_color="#444")
                photo_name = i.lower().replace(" ", "_")
                photo_name = photo_name.split(".")
                photo_name[1] = ".png"
                photo_name = str(photo_name[0])
                photo = ct.CTkImage(Image.open(os.path.join(image_path, f"{photo_name}.png")), size=(40, 40))
                songs_favourite = ct.CTkButton(list_fav_song_frame, text=i.split(".")[0], fg_color="transparent", hover_color="#444", font=("Poppins", 22, "bold"), 
                                            image=photo, compound=LEFT, text_color="white")
                songs_favourite.pack(side=LEFT, fill=X, padx=10)
                
                singer_name = ct.CTkLabel(list_fav_song_frame, text=self.get_music_info(f"songs\\{i}")["artist"], font=("Poppins", 20, "bold")) # type: ignore
                singer_name.pack(side=RIGHT, padx=20)

                list_fav_song_frame.pack(side=TOP, fill=X, expand=False, ipady=10, padx=10, pady=10, ipadx=10)
            playlist_songs_frame.pack(side=BOTTOM, fill=X, expand=True, pady=10, padx=5)
        
    def updateFavouritePlaylistImage(self):
        global music_icon, image_path, title_song
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "songs_images")
        if len(self.favourites) > 0:
            music_name = self.favourites[0].lower().replace(" ", "_")
            music_name = music_name.split(".")
            music_name[1] = ".png"
            music_name = str(music_name[0] + music_name[1])
            music_icon = ct.CTkImage(Image.open(os.path.join(image_path, f"{music_name}")), size=(220, 220))
            title_song.configure(image=music_icon)

        if len(self.favourites) == 0:
            title_song.configure(image=self.imgPlaylistFavourites)

        self.root.after(1000, self.updateFavouritePlaylistImage)

    def play_previous_song(self):
        try:
            self.play_music(self.previous_song[len(self.previous_song)-2])
        except Exception as e:
            print(e)

    def loop_song(self):
        self.loop = True
        if self.music_playing:
            current_position = pygame.mixer.music.get_pos() / 1000
            # print(current_position)

    def add_favourite(self):
        if self.music_playing:
            if self.music_playing not in self.favourites:
                self.favourite.configure(image=self.favourite_img2)
                self.favourite.configure(command=self.remove_favourite)
                self.favourites.append(self.music_playing)
                self.update_songs_()
            else:
                pass

    def remove_favourite(self):
        if self.music_playing:
            try:
                self.favourite.configure(image=self.favourite_img)
                self.favourite.configure(command=self.add_favourite)
                self.favourites.remove(self.music_playing)
                self.updateFavouritePlaylistImage()
                self.update_songs_()
            except Exception as e:
                print(e)

    def spacebar_event(self, event):
        if self.music_playing:
            self.stop_music()
            self.bind("<space>", self.spacebar_event_2)

    def spacebar_event_2(self, event):
        self.resume_music()
        self.bind("<space>", self.spacebar_event)

    def slide_song(self):
        # if self.music_playing:
        #     music_file = f"songs\\{self.music_playing}"
        #     pygame.mixer.music.load(music_file)
        #     music_length = pygame.mixer.Sound(music_file).get_length()
        #     scale_at = int(self.slider.get()) / 100 * music_length
        #     pygame.mixer.music.play(start=int(scale_at))
        pass

    def get_music_info(self, music_name):
        artist = get_artist(music_name)
        # album = get_album(song)

        return {
            "artist" : artist,
            # "album"  : album
            }

    def add_Music(self, music_name, music_image_name, tab="home"):
        self.all_songs.append(music_name)
        global song_image_path, song_img
        song_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "songs_images")
        song_img = ct.CTkImage(Image.open(os.path.join(song_image_path, music_image_name)), size=(280, 230))

        if tab not in self.frames:
            self.frames[tab] = ct.CTkFrame(self.home_frame, fg_color=self.color_home_frame)

        song_button = ct.CTkButton(self.frames[tab], text=music_name, fg_color=self.color_home_frame, bg_color="transparent", corner_radius=10,
                                   image=song_img, command=lambda: self.play_music(f"{music_name}.mp3"), compound=TOP, font=("IBM Plex Sans", 20))
        song_button.pack(side=LEFT, ipady=10, ipadx=0)
        self.frames[tab].pack(side=TOP, fill=X, pady=2)
        
    def add_audiobooks(self, audiobook_name, audiobook_image_name, tab="audiobooks"):
        global audiobooks_image_path, audiobook_img
        audiobooks_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "audiobooks\\audiobooksImage")
        audiobook_img = ct.CTkImage(Image.open(os.path.join(audiobooks_image_path, audiobook_image_name)), size=(190, 250))

        if tab not in self.frames2:
            self.frames2[tab] = ct.CTkFrame(self.audio_frame, fg_color="transparent")

        audiobook_button = ct.CTkButton(self.frames2[tab], text="", fg_color="transparent", bg_color="transparent", hover_color="gray30", image=audiobook_img, command=lambda: self.play_audiobooks(audiobook_name))
        audiobook_button.pack(side=LEFT, ipady=10, ipadx=8, padx=10)
        self.frames2[tab].pack(side=TOP, fill=X, pady=10, padx=30)

    def play_audiobooks(self, audiobook_name):
        self.favourite.pack_forget()
        author = {"Atomic Habits" : "James Clear",
                   "Digital Minimalism" : "Cal Newport",
                     "Rework" : "Jason Fried",
                       "HyperFocus" : "Chris Bailey", 
                       "The Richest Man in Babylon" : "George Clason", 
                       "Essentialism" : "Greg Mekeown"}
        
        pygame.mixer.music.load(f"audiobooks\\{audiobook_name}.mp3")
        pygame.mixer.music.play()
        self.pause.configure(state="normal", image=self.pause_img)
        self.audiobooks_data = MP3(f"audiobooks\\{audiobook_name}.mp3")
        self.audiobooks_length = int(self.audiobooks_data.info.length)
        self.music_duration_label.configure(text=time.strftime('%M:%S', time.gmtime(self.audiobooks_length)))
        self.scale_update2()
        self.insertSongImage2(audiobook_name)

        author_name = author[audiobook_name]

        if len(author_name) > 16:
            self.play_control_frame.pack_configure(padx=20)
        if len(author_name) < 16:
            self.play_control_frame.pack_configure(padx=140)

        self.singer_name.configure(text=f"{author[audiobook_name]}")

    def play_music(self, music_name):
        self.favourite.pack(side=RIGHT, padx=80)
        if self.music_playing != music_name:
            pygame.mixer.music.load(f"songs\\{music_name}")
            pygame.mixer.music.play()
            self.pause.configure(state="normal", image=self.pause_img)
            self.music_data = MP3(f"songs\\{music_name}")
            self.music_length = int(self.music_data.info.length)
            self.music_duration_label.configure(text=time.strftime('%M:%S', time.gmtime(self.music_length)))
            self.scale_update()
            self.insertSongImage(music_name)
            self.configure_music(music_name)
            self.previous_song.append(music_name)
            artist_name = self.get_music_info(f"songs\\{music_name}")["artist"]
            self.singer_name.configure(text=artist_name)
            if len(artist_name) > 16: # type: ignore
                self.play_control_frame.pack_configure(padx=20)
            if len(artist_name) < 16: # type: ignore
                self.play_control_frame.pack_configure(padx=140)

        self.music_playing = music_name

    def configure_music(self, music_name):
        if music_name in self.favourites:
            self.favourite.configure(image=self.favourite_img2, command=self.remove_favourite)
        else:
            self.favourite.configure(image=self.favourite_img, command=self.add_favourite)

    def insertSongImage(self, image):
        music_name = image.lower().replace(" ", "_")
        music_name = music_name.split(".")
        music_name[1] = ".png"
        music_name = str(music_name[0] + music_name[1])
        self.image = ct.CTkImage(Image.open(os.path.join(song_image_path, f"{music_name}")), size= (45, 45))
        self.image_song_label.configure(image=self.image)

    def insertSongImage2(self, image):
        audiobook_name = image.lower()
        audiobook_name = audiobook_name.replace(" ", "_")
        audiobook_name = f"{audiobook_name}.png"
        self.image = ct.CTkImage(Image.open(os.path.join(audiobooks_image_path, f"{audiobook_name}")), size= (45, 45))
        self.image_song_label.configure(image=self.image)

    def scale_update(self):
        try:
            self.root.after_cancel(self.updater2)
            self.updater2 = None
        except:
            pass
        self.slider.configure(to=self.music_data.info.length)
        current_position = pygame.mixer.music.get_pos()
        self.position = int(current_position / 1000)
        self.slider.set(int(current_position / 1000))
        self.time_elapsed_label.configure(text=time.strftime('%M:%S', time.gmtime(self.slider.get())))
        self.updater = self.root.after(1000, self.scale_update)

    def scale_update2(self):
        try:
            self.root.after_cancel(self.updater)
            self.updater = None
        except:
            pass
        self.slider.configure(to=self.audiobooks_data.info.length)
        current_position = pygame.mixer.music.get_pos()
        self.position = int(current_position / 1000)
        self.slider.set(int(current_position / 1000))
        self.time_elapsed_label.configure(text=time.strftime('%M:%S', time.gmtime(self.slider.get())))
        self.updater2 = self.root.after(1000, self.scale_update2)

    def stop_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.pause.configure(image=self.stop_img, command=self.resume_music)
        else:
            pass

    def resume_music(self):
        pygame.mixer.music.unpause()
        self.pause.configure(image=self.pause_img, command=self.stop_music)

    def select_frame_name(self, name):
        self.search.configure(fg_color="#444" if name == "search" else "transparent")
        self.home.configure(fg_color="#444" if name == "home" else "transparent")
        self.artists.configure(fg_color="#444" if name == "artists" else "transparent")
        self.trending.configure(fg_color="#444" if name == "trending" else "transparent")
        self.audiobooks.configure(fg_color="#444" if name == "audiobooks" else "transparent")
        self.settings.configure(fg_color="#444" if name == "settings" else "transparent")
        self.favourites_btn.configure(fg_color="#444" if name == "favourites" else "transparent")

        if name == "search":
            self.search_frame.pack(fill=BOTH, expand=True)
        else:
            self.search_frame.pack_forget()
        if name == "home":
            self.home_frame.pack(fill=BOTH, expand=True)
        else:
            self.home_frame.pack_forget()
        if name == "artists":
            self.discover_frame.pack(fill=BOTH, expand=True)
        else:
            self.discover_frame.pack_forget()
        if name == "trending":
            self.popular_frame.pack(fill=BOTH, expand=True)
        else:
            self.popular_frame.pack_forget()
        if name == "audiobooks":
            self.audiobooks_frame.pack(fill=BOTH, expand=True)
        else:
            self.audiobooks_frame.pack_forget()
        if name == "favourites":
            self.favourites_frame.pack(fill=BOTH, expand=True)
        else:
            self.favourites_frame.pack_forget()
        if name == "settings":
            self.settings_frame.pack(fill=BOTH, expand=True)
        else:
            self.settings_frame.pack_forget()

def add_music(app):
        # Music code here
        app.add_Music(music_name="Let Me Down Slowly", music_image_name="let_me_down_slowly.png", tab="home1")
        app.add_Music(music_name="Raghupathi Raghava Rajaram", music_image_name="raghupathi_raghava_rajaram.png", tab="home1")
        app.add_Music(music_name="Ram Aayenge", music_image_name="ram_aayenge.png", tab="home1")
        app.add_Music(music_name="Tu Jo Mila", music_image_name="tu_jo_mila.png", tab="home1")

        app.add_Music(music_name="Faded", music_image_name="faded.png", tab="home2")
        app.add_Music(music_name="See you Again", music_image_name="see_you_again.png", tab="home2")
        app.add_Music(music_name="Hymn For The Weekend", music_image_name="hymn_for_the_weekend.png", tab="home2")
        app.add_Music(music_name="Into Your Arms", music_image_name="into_your_arms.png", tab="home2")

        app.add_Music(music_name="Infinity", music_image_name="infinity.png", tab="home3")
        app.add_Music(music_name="Can We Kiss Forever", music_image_name="can_we_kiss_forever.png", tab="home3")
        app.add_Music(music_name="Arcade", music_image_name="arcade.png", tab="home3")
        app.add_Music(music_name="Safari", music_image_name="safari.png", tab="home3")

        app.add_Music(music_name="Fearless", music_image_name="fearless.png", tab="home4")
        app.add_Music(music_name="Tum Hi Ho", music_image_name="tum_hi_ho.png", tab="home4")
        app.add_Music(music_name="Khairiyat", music_image_name="Khairiyat.png", tab="home4")
        app.add_Music(music_name="Baaton Ko Teri", music_image_name="baaton_ko_teri.png", tab="home4")

        app.add_Music(music_name="Khamoshiyan", music_image_name="khamoshiyan.png", tab="home5")
        app.add_Music(music_name="Tere Sang Yaara", music_image_name="tere_sang_yaara.png", tab="home5")
        app.add_Music(music_name="Chhod Diya", music_image_name="chhod_diya.png", tab="home5")
        app.add_Music(music_name="Phir Mohabbat", music_image_name="phir_mohabbat.png", tab="home5")

        # AudioBooks code here 
        app.add_audiobooks(audiobook_name="Atomic Habits", audiobook_image_name="atomic_habits.png", tab="audiobooks1")
        app.add_audiobooks(audiobook_name="Digital Minimalism", audiobook_image_name="digital_minimalism.png", tab="audiobooks1")
        app.add_audiobooks(audiobook_name="Rework", audiobook_image_name="rework.png", tab="audiobooks1")
        app.add_audiobooks(audiobook_name="HyperFocus", audiobook_image_name="hyperfocus.png", tab="audiobooks1")
        app.add_audiobooks(audiobook_name="The Richest Man in Babylon", audiobook_image_name="the_richest_man_in_babylon.png", tab="audiobooks1")
        app.add_audiobooks(audiobook_name="Essentialism", audiobook_image_name="essentialism.png", tab="audiobooks2")

if __name__ == "__main__":
    pygame.mixer.init()

    root = ct.CTk()

    if os.path.exists("data.txt"):
        app = Spotify(root)
        add_music(app)
    else:
        IntroPage(root)

    cProfile.run("root.mainloop()", sort="time")