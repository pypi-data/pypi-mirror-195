def main():
    import tkinter
    import customtkinter
    import threading
    from time import sleep
    import os
    from PIL import Image
    from tkinter import PhotoImage
    from tkinter import Wm
    import sys
    from tkinter import filedialog

    STEAM = "Main\\Test.png"
    VALO = "Main\\VALORANT.PNG"
    ROBLOX = "Main\\Roblox.png"
    exit = False

    def output_sentence(sentence, color):
        global text
        # Insert the sentence at the end of the text widget, using the color provided
        text.configure(state="normal")
        text.insert("end", f"{sentence}\n", color)  # Use the custom tag for the color and the "bold" tag to make the text bold
        # Update the window size to fit the output
        loginwin.update_idletasks()
        # Set the width of the window to the width of the output and the height to 600 pixels
        text.configure(state="disabled")
        text.tag_add("center", "1.0", "end")
        text.tag_config("center", justify='center')
        text.see("end")
    

    def Program():
            
        import pyautogui as pg
        from time import sleep
        import os
        from os import sys
        import pygetwindow as gw
        from time import sleep
        import requests
        
        global msg, webhook
        msg = "@everyone ,Valorant is restocked."
        webhook = "https://discord.com/api/webhooks/997158836307771402/DAKW7JsqvNa9aIsxDOUGnOoCrw0MukW7kSXNmvA1wVNYRVdnBvzDSpDFJLfeAGpuhLH_"
        def spam(msg, webhook):
            try:
                data = requests.post(webhook, json={'content': msg})
                if data.status_code == 204:
                    print(f"Sent MSG {msg}")
            except:
                print("Bad Webhook :" + webhook)
                sleep(5)
                exit()


        # def resource_path(relative_path):
        #     """ Get absolute path to resource, works for dev and for PyInstaller """
        #     try:
        #         # PyInstaller creates a temp folder and stores path in _MEIPASS
        #         base_path = sys._MEIPASS
        #     except Exception:
        #         base_path = os.path.abspath(".")

        #     return os.path.join(base_path, relative_path)


        # SHOP = resource_path("Main\SHOP.PNG")
        # BUY = resource_path("Main\BUY.PNG")
        # VALORANT = resource_path("Main\VALORANT.PNG")


        win = gw.getWindowsWithTitle('Buff App')[0] 
        win.activate()
        pg.keyDown("enter")


        RefreshEvery = 1
        sleep(2)
        

        def Relode():
            sleep(RefreshEvery)
            shop = pg.locateCenterOnScreen("Main\\SHOP.PNG", confidence=0.8)
            lounge = pg.locateCenterOnScreen("Main\Lounge.png", confidence=0.8)

            if shop != None:
                pg.click(lounge.x, lounge.y)
                sleep(0.5)
                pg.click(shop.x, shop.y)
                sleep(0.5)
                pg.move(200, 0)
                sleep(1)
                
        Relode()


        n = 0
        while True:
            if exit:
                break
            print(n)
            pg.scroll(-n)
            sleep(1)
            product = pg.locateCenterOnScreen(image, confidence=0.8)
            

            if product != None:
                pg.click(product.x, product.y)
                sleep(2)
                Buy = pg.locateCenterOnScreen("Main\\BUY.PNG", confidence=0.8)
                
                if Buy != None:
                    output_sentence("In Stock, Item clicked...","#000")
                    output_sentence("—————","#000")
                    pg.click(Buy.x, Buy.y)
                    # spam(msg, webhook)
                    break
                    
                else:
                    output_sentence("Out of Stock, Reloding Shop...","#000")
                    output_sentence("—————","#000")
                    Relode()

            else:
                output_sentence("Looking For Product...", "")
                n +=  n + 100
                sleep(3)
        if not exit:
            output_sentence("Sleeping to get new emails...","#000")
            output_sentence("—————","#000")
            for n in range(5):
                output_sentence(n+1, "#000")
                sleep(1)

            output_sentence("—————","#000")
            import easyimap as e
            import re
            host = "imap.gmail.com"
            # user = "saifkhouri2@gmail.com"
            # passw = "opabeburanzndmsy"

            "opabeburanzndmsy"

            server = e.connect(host, USER, PASS)

            def emails(n):
                global mail
                mail = server.mail(server.listids()[n])

            for n in range(10):
                emails(n)
                if mail.title == "Buff Game":
                    output_sentence("Email Found","#000")
                    output_sentence("————","#000")
                    buffemail = server.mail(server.listids()[n])
                    temp = re.findall(r'\d{6}', buffemail.body)
                    res = list(map(int, temp))
                    # output_sentence("The numbers list is : " + str(res))
                
                    finalN = []
                    
                    for n in res:
                        if n not in finalN and n != 131517 and n != 165884 and n != 32419 and n != 29238:
                            finalN.append(n)
                    
                    output_sentence("Code is : " + str(finalN[-1]),"#000")
                    break
                
            while True:
                try:
                    Key = pg.locateCenterOnScreen("Main\\Key.png", confidence=0.8)
                    if Key != None:
                        break
                except:
                    sleep("[ERR]Cant find text box")
                    sleep(1)

            pg.click(Key.x, Key.y)
            pg.typewrite(str(finalN[-1]))
            sleep(0.5)
            try:
                confirm = pg.locateCenterOnScreen("Main\\confirm.png", confidence=0.8)
                # pg.click(confirm.x, confirm.y)
            except:
                output_sentence("[err]","#000")
                sleep(0.5)
            
        
    def Startbtn():
        btn.configure(state=("disabled"), fg_color="#5d5d5d", text_color_disabled="#262626")
        global image, USER, PASS
        USER = str(entry1Var.get())
        PASS = str(entry2Var.get())
        
        value = radiobutton_var.get()
        
        if value == 1:
            image = STEAM
        elif value == 2:
            image = VALO
        elif value == 3:
            image = ROBLOX
        elif value == 4:
            filetypes = (('Image', '*.png'), ('Image', '*.jpg'))
            image = filedialog.askopenfile(filetypes=filetypes).name
        
        outputwindow()
        sleep(1)
        threading.Thread(target=Program).start()


    def check():
        while True:
            output_sentence(radiobutton_var.get())
            sleep(1)
            
    def outputwindow():
        global text, window
        window = customtkinter.CTkToplevel()
        window.geometry("200x200")
        window.iconbitmap("Main\\logo.ico")
        window.resizable(width=False, height=False)
        window.title("Console Log")
        
        
        text = customtkinter.CTkTextbox(window, width=200, height=200, fg_color="#242424", text_color="#fff")
        text.place(relx=.5, rely=.5, anchor="center")
        
        def prevent_highlight(event):
            return "break"
        
        text.bind("<1>", prevent_highlight)
        
        window.wm_transient(loginwin)

    def exitP():
        global exit
        try:
            window.destroy()
            exit = True
        except:    
            pass
        loginwin.destroy() 
    loginwin = customtkinter.CTk()
    loginwin.geometry("700x600")
    loginwin.title("Auto Buff")
    backg = customtkinter.CTkImage(Image.open("Main\\bg.jpg"), size=(700, 600))


    loginwin.resizable(width=False, height=False)

    loginwin.iconbitmap("Main\\logo.ico")

    customtkinter.set_default_color_theme("green")

    backgg = customtkinter.CTkLabel(loginwin, image=backg).grid(row=0, column=0)

    frame = customtkinter.CTkFrame(loginwin, fg_color="#303030")
    frame.grid(row=0)
    btnframe= customtkinter.CTkFrame(frame, fg_color="#303030")
    btnframe.grid(column=0, row=9)

    label = customtkinter.CTkLabel(frame, text="User-Info", font=customtkinter.CTkFont("Montserrat", 30, weight="bold"), text_color="#dadada")
    label.grid(column=0, row=0)
    label2 = customtkinter.CTkLabel(frame, text="—————————————————", font=customtkinter.CTkFont("Montserrat", 17, weight="bold"), text_color="#dadada")
    label2.grid(column=0, row=1, pady=0)

    entry1Var = tkinter.StringVar(frame)
    gmailLabel = customtkinter.CTkLabel(frame, text="Gmail", font=customtkinter.CTkFont("Montserrat", 17, weight="bold"), text_color="#dadada")
    gmailLabel.grid(sticky="news", column=0, row=2, pady=(0, 0))
    entry = customtkinter.CTkEntry(frame, textvariable=entry1Var, width=250, font=customtkinter.CTkFont("Montserrat", 14, weight="bold"), text_color="#dadada", border_color="#dadada", corner_radius=8)
    entry.grid(column=0, row=3, pady=(0, 0))

    entry2Var = tkinter.StringVar(frame)
    passLabel = customtkinter.CTkLabel(frame, text="Password", font=customtkinter.CTkFont("Montserrat", 17, weight="bold"), text_color="#dadada")
    passLabel.grid(sticky="news", column=0, row=4, pady=(0, 0))
    entry2 = customtkinter.CTkEntry(frame, textvariable=entry2Var, width=250, font=customtkinter.CTkFont("Montserrat", 18, weight="bold"), text_color="#dadada", show="*", border_color="#dadada", corner_radius=8)
    entry2.grid(column=0, row=5)

    btn = customtkinter.CTkButton(frame, text="Start", font=customtkinter.CTkFont("Montserrat", 15, weight="bold"), command=Startbtn, text_color="#000", fg_color="#c3c3c3", hover_color="#909090", corner_radius=10)
    btn.grid(sticky="", pady=(10, 20) , column=0, row=6)



    radiobutton_var = customtkinter.IntVar(value=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure((2, 3), weight=1)
    btn2 = customtkinter.CTkRadioButton(btnframe, text="Steam", variable=radiobutton_var, value=1, font=customtkinter.CTkFont("Montserrat", 17, weight="bold"), fg_color="#dadada", hover_color="#5d5d5d", corner_radius=0, border_width_checked=3)
    btn2.grid(sticky="news", column=0, row=0, pady=10)
    btn3 = customtkinter.CTkRadioButton(btnframe, text="Valorant", variable=radiobutton_var, value=2, font=customtkinter.CTkFont("Montserrat", 17, weight="bold"), fg_color="#dadada", hover_color="#5d5d5d", corner_radius=0, border_width_checked=3)
    btn3.grid(sticky="news", column=0, row=1, pady=10)
    btn4 = customtkinter.CTkRadioButton(btnframe, text="Roblox", variable=radiobutton_var, value=3, font=customtkinter.CTkFont("Montserrat", 17, weight="bold"), fg_color="#dadada", hover_color="#5d5d5d", corner_radius=0, border_width_checked=3)
    btn4.grid(sticky="news", column=0, row=2, pady=10)
    btn5 = customtkinter.CTkRadioButton(btnframe, text="Custom", variable=radiobutton_var, value=4, font=customtkinter.CTkFont("Montserrat", 17, weight="bold"), fg_color="#dadada", hover_color="#5d5d5d", corner_radius=0, border_width_checked=3)
    btn5.grid(sticky="news", column=0, row=3, pady=10)

    logoIMG = customtkinter.CTkImage(Image.open("Main\\logo.png"), size=(70, 80))
    logo = customtkinter.CTkLabel(btnframe , image=logoIMG, text="").grid(column=0, row=4, sticky="news", pady=(40, 17))

    creds = customtkinter.CTkButton(frame, text="Made By SDK", fg_color="#c3c3c3", hover_color="#909090",text_color="#000", font=customtkinter.CTkFont("Montserrat", 17, weight="bold"))
    creds.grid(column=0, row=10, sticky="we")


    if os.path.isfile('save.txt'):
        with open('save.txt','r') as f:
            lines = [line.rstrip() for line in f]
            entry1Var.set(lines[0])
            entry2Var.set(lines[1])
        
    try:
        loginwin.protocol("WM_DELETE_WINDOW", exitP)
    except:
        pass    

    loginwin.mainloop()

    with open('save.txt','w') as f:
        f.write(entry1Var.get() + "\n")
        f.write(entry2Var.get())