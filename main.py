from tkinter import scrolledtext
import os
import pygame
import mysql.connector
pygame.init()



from tkinter import *
from PIL import ImageTk, Image

window = Toplevel()
window.title("Game Window")
window.geometry('925x500+300+200')
window.resizable(False,False)
img = Image.open(r'C:\Users\USER\PycharmProjects\pythonProject5\gameimage\spaceship.jpg')
img = img.resize((925,500))
image_tk = ImageTk.PhotoImage(img)


image_label = Label(window, image=image_tk)
image_label.image = image_tk
image_label.pack()


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="1a_marba"
)
cursor = db.cursor()



WIDTH = 1500
HEIGHT = 790
gamewindow = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Learning Code Attack")

playernmae = pygame.font.SysFont('cooper black',20)
winnerfont =pygame.font.SysFont('cooper black',40)

playerentername1 = " "
playerentername2 = " "


vel = 10
firevel = 7
maxfire = 5
left = 90
right = 270
up = 0
down = 180
playerwidth = 80
playerheight = 80

player1life = 10
player2life = 10

borderline= pygame.Rect(WIDTH/2,0,10,HEIGHT)

WHITE = (250, 250, 220)
red = (255, 0, 0)
yellow = (255, 255, 0)
black=(0,0,0)

current_directory = os.path.dirname(__file__)
image_directory = os.path.join(current_directory, 'gameimage')

player1image = pygame.image.load(os.path.join(image_directory, 'blue plane.png')).convert_alpha()
player2image = pygame.image.load(os.path.join(image_directory, 'white.png')).convert_alpha()
backgroundspace = pygame.transform.scale(pygame.image.load(os.path.join(image_directory, 'space2.jpg')).convert(), (WIDTH, HEIGHT))

playerplane1 = pygame.transform.rotate(pygame.transform.scale(player1image, (playerwidth, playerheight)), 270)
playerplane2 = pygame.transform.rotate(pygame.transform.scale(player2image, (playerwidth, playerheight)), 90)

player1_hit = pygame.USEREVENT = 1
player2_hit = pygame.USEREVENT = 2

def get_settings_from_db():
    global vel, maxfire, firevel
    cursor.execute("SELECT vel, maxfire, firevel FROM settings ORDER BY id DESC LIMIT 1")
    settings = cursor.fetchone()
    if settings:
        vel, maxfire, firevel = settings
def get_player_names_from_db():
    global playerentername1, playerentername2
    cursor.execute("SELECT playerentername1, playerentername2 FROM nameplayer ORDER BY id DESC LIMIT 1")
    names = cursor.fetchone()  # Fetch the names from the database
    if names:
        playerentername1, playerentername2 = names


def nameofplayer():
    def add_settings():
        names1 = playerentername1_entry.get()
        names2 = playerentername2_entry.get()

        # Inserting entered names into the 'nameplayer' table
        cursor.execute("INSERT INTO nameplayer (playerentername1, playerentername2) VALUES (%s, %s)", (names1, names2))
        db.commit()  # Commit the changes

        # Update global variables with new names
        global playerentername1, playerentername2
        playerentername1 = names1
        playerentername2 = names2

        window2.destroy()  # Destroy window2 after adding names
        window.deiconify()  # Show the main window

    window2 = Toplevel()
    window2.geometry('500x500')
    window2.title("Set players name")
    window2.configure(bg='gray')

    font = ('cooper black', 12)
    img4 = Image.open(r'C:\Users\USER\PycharmProjects\pythonProject5\gameimage\white.png')
    img4 = img4.resize((150, 150))
    image_tk = ImageTk.PhotoImage(img4)
    imageplane = Label(window2, image=image_tk)
    imageplane.image = image_tk
    imageplane.place(x=280, y=200)

    img5 = Image.open(r'C:\Users\USER\PycharmProjects\pythonProject5\gameimage\blue plane.png')
    img5 = img5.resize((150, 150))
    image_tk = ImageTk.PhotoImage(img5)
    imageplane1 = Label(window2, image=image_tk)
    imageplane1.image = image_tk
    imageplane1.place(x=50, y=200)

    playerentername1_label = Label(window2, text="player1:", font=font, fg='red', bg='black')
    playerentername1_label.place(x=20, y=100)
    playerentername1_entry = Entry(window2)
    playerentername1_entry.place(x=100, y=100)

    playerentername2_label = Label(window2, text="player2:", font=font, fg='red', bg='black')
    playerentername2_label.place(x=270, y=100)
    playerentername2_entry = Entry(window2)
    playerentername2_entry.place(x=350, y=100)

    add_button = Button(window2, text="SAVE NAME", fg='red', command=add_settings, bg='black', font=font)
    add_button.place(x=190, y=400)

    window.withdraw()
    window2.mainloop()


    window.deiconify()


def controlplayer1(key_pressed, playerplace1):
    global playerplane1
    if key_pressed[pygame.K_a] and playerplace1.x - vel > 0:
        playerplace1.x -= vel
        playerplane1 = pygame.transform.rotate(pygame.transform.scale(player1image, (playerwidth, playerheight)), left)

    if key_pressed[pygame.K_d] and playerplace1.x + vel < borderline.x - playerplace1.width:
        playerplace1.x += vel
        playerplane1 = pygame.transform.rotate(pygame.transform.scale(player1image, (playerwidth, playerheight)), right)
    if key_pressed[pygame.K_w] and playerplace1.y - vel > 0:
        playerplace1.y -= vel
        playerplane1 = pygame.transform.rotate(pygame.transform.scale(player1image, (playerwidth, playerheight)), up)
    if key_pressed[pygame.K_s] and playerplace1.y + vel < HEIGHT - playerplace1.height:
        playerplace1.y += vel
        playerplane1 = pygame.transform.rotate(pygame.transform.scale(player1image, (playerwidth, playerheight)), down)


def controlplayer2(key_pressed, playerplace2):
    global playerplane2
    if key_pressed[pygame.K_LEFT] and playerplace2.x - vel > borderline.x + borderline.width:
        playerplace2.x -= vel
        playerplane2 = pygame.transform.rotate(pygame.transform.scale(player2image, (playerwidth, playerheight)), left)
    if key_pressed[pygame.K_RIGHT] and playerplace2.x + vel < WIDTH - playerplace2.width:
        playerplace2.x += vel
        playerplane2 = pygame.transform.rotate(pygame.transform.scale(player2image, (playerwidth, playerheight)), right)
    if key_pressed[pygame.K_UP] and playerplace2.y - vel > 0:
        playerplace2.y -= vel
        playerplane2 = pygame.transform.rotate(pygame.transform.scale(player2image, (playerwidth, playerheight)), up)
    if key_pressed[pygame.K_DOWN] and playerplace2.y + vel < HEIGHT - playerplace2.height:
        playerplace2.y += vel
        playerplane2 = pygame.transform.rotate(pygame.transform.scale(player2image, (playerwidth, playerheight)), down)
def fire_pressed(player1fire, player2fire, playerplace1, playerplace2):
    for fire in player1fire[:]:
        fire.x += firevel
        if fire.colliderect(playerplace2):
            pygame.event.post(pygame.event.Event(player2_hit))
            player1fire.remove(fire)
        elif fire.x > WIDTH:
            player1fire.remove(fire)

    for fire in player2fire[:]:
        fire.x -= firevel
        if fire.colliderect(playerplace1):
            pygame.event.post(pygame.event.Event(player1_hit))
            player2fire.remove(fire)
        elif fire.x <0:
            player2fire.remove(fire)





def display(playerplace1, playerplace2, player1fire, player2fire,P1life,P2life):
    get_player_names_from_db()

    gamewindow.blit(backgroundspace, (0, 0))
    pygame.draw.rect(gamewindow, black, borderline)

    playername1_text = playernmae.render(playerentername1 + str(P1life), 1, WHITE)
    playername2_text = playernmae.render(playerentername2 + str(P2life), 1, WHITE)

    # Calculate positions for displaying names
    playername1_x = 10  # Left side
    playername1_y = 10

    playername2_x = WIDTH - playername2_text.get_width() - 10  # Right side
    playername2_y = 10

    # Blit the texts and player planes
    gamewindow.blit(playername1_text, (playername1_x, playername1_y))
    gamewindow.blit(playername2_text, (playername2_x, playername2_y))
    gamewindow.blit(playerplane1, (playerplace1.x, playerplace1.y))
    gamewindow.blit(playerplane2, (playerplace2.x, playerplace2.y))

    for fire in player1fire:
        pygame.draw.rect(gamewindow, red, fire)
    for fire in player2fire:
        pygame.draw.rect(gamewindow, yellow, fire)

    pygame.display.update()




def show_question(P1life, P2life):


    def restart_game():
        window.deiconify()
        pygame.display.set_mode((WIDTH, HEIGHT)) # Restart when correct
        start_game()

    def fetch_question():
        cursor.execute("SELECT id, question, answer FROM game_question ORDER BY RAND() LIMIT 1")
        fetched_question = cursor.fetchone()
        if fetched_question:
            question_id, question_text, correct_answer = fetched_question
            question_label.config(
                text=question_text,
                font=("cooper black", 14),
                fg="black",
                wraplength=380,
                justify="center"
            )

            check_answer.config(
                command=lambda: check_correct_answer(question_id, correct_answer, question_window, P1life, P2life)
            )

    def check_correct_answer(question_id, correct_answer, question_window, P1life, P2life):
        user_answer = answer_entry.get()

        if user_answer.lower() == correct_answer.lower():
            question_window.destroy()
            restart_game()
        else:
            question_window.destroy()
            winner = ""
            if P1life <= 0:
                if P2life <= 0:
                    winner = "It's a Draw!"
                else:
                    winner = playerentername2
            elif P2life <= 0:
                winner = playerentername1

            if winner:
                winner_text = winner + " wins"
                winnerfunct(winner_text)
                question_window.destroy()

    def surrender_game():
        question_window.destroy()
        winner = ""
        if P1life <= 0:
            if P2life <= 0:
                winner = "It's a Draw!"
            else:
                winner = playerentername2
        elif P2life <= 0:
            winner = playerentername1

        if winner:
            winner_text = winner + " wins"
            winnerfunct(winner_text)
            question_window.destroy()
            window.deiconify()

    question_window = Toplevel()
    question_window.title("Question Window")
    question_window.geometry('500x500')

    custom_font = ('cooper black', 14)
    img2 = Image.open(r'C:\Users\USER\PycharmProjects\pythonProject5\gameimage\background .jpg')
    img2 = img2.resize((500, 500))
    image_tk = ImageTk.PhotoImage(img2)

    image_label2 = Label(question_window, image=image_tk)
    image_label2.image = image_tk
    image_label2.place(x=0, y=0)

    question_label = Label(question_window, text="", font=custom_font, wraplength=50, bg='red',fg='black')
    question_label.pack(pady=30)
    answer_entry = Entry(question_window, font=custom_font)
    answer_entry.pack(pady=30)

    check_answer = Button(question_window, text="Submit Answer", font=custom_font,bg='black',fg='red')
    check_answer.pack(pady=30)

    fetch_question_button = Button(question_window, text="Next Question", font=custom_font, command=fetch_question,fg='red',bg='black')
    fetch_question_button.pack(pady=20)

    surrender_button = Button(question_window, text="Surrender", font=custom_font,bg='black',fg='red',command=surrender_game)
    surrender_button.pack()

    fetch_question()
    question_window.mainloop()
def winnerfunct(winner_name):
    text = f"{winner_name}"
    textvar = winnerfont.render(text, 1, WHITE)
    gamewindow.blit(textvar, (1500/2 - textvar.get_width()/2, HEIGHT/2 - textvar.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)  # Delay for 3000 milliseconds (3 seconds)

    update_winner_query = "UPDATE nameplayer SET winner = %s WHERE id = (SELECT MAX(id) FROM nameplayer)"
    cursor.execute(update_winner_query, (winner_name,))
    db.commit()

    pygame.quit()

    window.deiconify()
def helpinfo():
    helpwindow = Tk()
    helpwindow.geometry('900x500')
    helpwindow.title('Help')
    helpwindow.configure(bg='gray')

    info_text = """
    Welcome to Space quest ignition:\n knowledge combat System

    Game Controls:
    Player 1 (Blue Plane):
    - Move Up: W key
    - Move Down: S key
    - Move Left: A key
    - Move Right: D key
    - Fire: SPACE key

    Player 2 (White Plane):
    - Move Up: UP arrow key
    - Move Down: DOWN arrow key
    - Move Left: LEFT arrow key
    - Move Right: RIGHT arrow key
    - Fire: Numpad 0 key

    Objective:
    - Players control their planes to dodge enemy fire.
    - Use the fire button to attack the opponent.
    - Each hit reduces the player's life by 1.
    - Answer questions correctly to win!

    Note: You can configure player names in the 'Player Names' section.

    Have fun playing!
    """

    # Create a scrolled text widget
    info_text_widget = scrolledtext.ScrolledText(helpwindow, width=80, height=20, wrap='word', font=('cooper black', 12), bg='black', fg='red')
    info_text_widget.pack(padx=20, pady=20)

    # Insert the information text into the scrolled text widget
    info_text_widget.insert('1.0', info_text)

    helpwindow.mainloop()
def start_game():
    pygame.init()
    window.withdraw()





    def main():
        get_settings_from_db()
        playerplace1 = pygame.Rect(200, 375, playerwidth, playerheight)
        playerplace2 = pygame.Rect(1200, 375, playerwidth, playerheight)
        clock = pygame.time.Clock()

        player1fire = []
        player2fire = []

        P1life = player1life
        P2life = player2life

        run = True
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and len(player1fire) < maxfire:
                        fire = pygame.Rect(playerplace1.x + playerplace1.width,
                                           playerplace1.y + playerplace1.height // 2 - 2, 40, 5)
                        player1fire.append(fire)

                    if event.key == pygame.K_KP0 and len(player2fire) < maxfire:
                        fire = pygame.Rect(playerplace2.x, playerplace2.y + playerplace2.height // 2 - 2, 40, 5)
                        player2fire.append(fire)

                if event.type == player1_hit:
                    P1life -= 1
                    if P1life <= 0:
                        show_question(P1life, P2life)

                if event.type == player2_hit:
                    P2life -= 1
                    if P2life <= 0:
                        show_question(P1life, P2life)

            key_pressed = pygame.key.get_pressed()
            controlplayer1(key_pressed, playerplace1)
            controlplayer2(key_pressed, playerplace2)
            display(playerplace1, playerplace2, player1fire, player2fire, P1life, P2life)
            fire_pressed(player1fire, player2fire, playerplace1, playerplace2)

    window.withdraw()
    main()

def close_game_window():
    pygame.quit()  # Quit Pygame
    window.destroy()

# Bind closing the window to the close_game_window function
window.protocol("WM_DELETE_WINDOW", close_game_window)



frm = Frame(window, width=250, height=250,border=0, highlightthickness=0)
frm.place(x=300,y=100)
img = Image.open(r'C:\Users\USER\PycharmProjects\pythonProject5\gameimage\background .jpg')
img = img.resize((300,300))
image_tk = ImageTk.PhotoImage(img)


image_label = Label(frm, image=image_tk)
image_label.image = image_tk
image_label.pack()





start_game_button = Button(frm, text="Start Game",border=0,font=('Microsoft YaHei UI Light',10,'bold'),bg="black",fg="white",command=start_game)
start_game_button.place(x=115, y=50)

ingameplayer_name = Button(frm, text="Player Names",border=0,font=('Microsoft YaHei UI Light',10,'bold'),bg="aqua",command=nameofplayer)
ingameplayer_name.place(x=105, y=100)

close_game_button = Button(frm, text="Close Game",border=0,font=('Microsoft YaHei UI Light',10,'bold'),bg="red", command=close_game_window)
close_game_button.place(x=110, y=150)

helpButton= Button (frm,text="Help",border=0,font=('Microsoft YaHei UI Light',10,'bold'),command=helpinfo)
helpButton.place(x=135, y=200)


window.mainloop()


