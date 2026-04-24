import pygame
import bcrypt
from user_data_manager import FileManager,AuthManager,FileMissingError,FileCorruptedError,Stats


file_manager = FileManager()


try:
    stats = file_manager.load_player_stats()
except (FileMissingError,FileCorruptedError):
    stats = {}

try:
    credentials = file_manager.load_user_credentials()
except (FileMissingError,FileCorruptedError):
    credentials = {}

auth_manager = AuthManager(credentials)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Jujutsu Game")
clock = pygame.time.Clock()
state = "MAIN MENU"
active_box = None



title_font = pygame.font.Font(None,90)
game_title_surf = title_font.render("Jujutsu Game",True,(240,234,255))
game_title_rect = game_title_surf.get_rect(center = (640,150))

subtitle_font = pygame.font.Font(None,60)
game_subtitle_surf = subtitle_font.render("Cursed Clash",True,(123,77,225))
game_subtitle_rect = game_subtitle_surf.get_rect(center = (640,200))

button_font = pygame.font.Font(None,40)
sign_button = pygame.Rect(490,360,300,55)
signin_surf = button_font.render("Sign in",True,(201,184,240))
signin_rect = signin_surf.get_rect(center = sign_button.center)

login_button = pygame.Rect(490,440,300,55)
login_surf = button_font.render("login",True,(201,184,240))
login_rect = login_surf.get_rect(center = login_button.center)


def draw_main_menu():
    screen.fill((13,11,20))

    screen.blit(game_title_surf,game_title_rect)
    screen.blit(game_subtitle_surf,game_subtitle_rect)

    pygame.draw.rect(screen,(90,31,209),sign_button,border_radius=15)
    screen.blit(signin_surf,signin_rect)

    pygame.draw.rect(screen,(90,31,209),login_button,border_radius=15)
    screen.blit(login_surf,login_rect)



username = ""
password = ""
passkey = ""
new_password = ""

username_label_surf = button_font.render("USERNAME", True, (107,90,138))
username_label_rect = username_label_surf.get_rect(center=(640,255))
username_textbox = pygame.Rect(440,270,400,50)

password_label_surf = button_font.render("PASSWORD", True, (107,90,138))
password_label_rect = password_label_surf.get_rect(center=(640,355))
password_textbox = pygame.Rect(440,370,400,50)

passkey_label_surf = button_font.render("PASS KEY", True, (107,90,138))
passkey_label_rect = passkey_label_surf.get_rect(center=(640,445))
passkey_textbox = pygame.Rect(440,460,400,50)

passkey_text_font = pygame.font.Font(None,36)
passkey_surf = passkey_text_font.render("", True, (201,184,240))
passkey_rect = passkey_surf.get_rect(center=passkey_textbox.center)

username_text_font = pygame.font.Font(None,36)
username_surf = username_text_font.render("", True, (201,184,240))
username_rect = username_surf.get_rect(center=username_textbox.center)

password_text_font = pygame.font.Font(None,36)
password_surf = password_text_font.render("", True, (201,184,240))
password_rect = password_surf.get_rect(center=password_textbox.center)

submit_surf = button_font.render("Submit",True,(201,184,240))
submit_button = pygame.Rect(560, 570, 150, 55)
submit_rect = submit_surf.get_rect(center=submit_button.center)

back_surf = button_font.render("Back", True, (107,90,138))
back_button = pygame.Rect(580, 645, 100, 40)
back_rect = back_surf.get_rect(center=back_button.center)

error_font = pygame.font.Font(None,30)
error_surf = error_font.render("", True, (220,80,80))
error_rect = error_surf.get_rect(center=(640,545))

new_password_label_surf = button_font.render("NEW PASSWORD", True, (107,90,138))
new_password_label_rect = new_password_label_surf.get_rect(center=(640,445))
new_password_textbox = pygame.Rect(440,460,400,50)

new_password_text_font = pygame.font.Font(None,36)
new_password_surf = new_password_text_font.render("", True, (201,184,240))
new_password_rect = new_password_surf.get_rect(center=new_password_textbox.center)

forgot_surf = error_font.render("Forgot Password?", True, (107,90,138))
forgot_button = pygame.Rect(490, 530, 300, 35)
forgot_rect = forgot_surf.get_rect(center=forgot_button.center)

forgot_passkey_textbox = pygame.Rect(440, 360, 400, 50)
forgot_passkey_label_rect = passkey_label_surf.get_rect(center=(640, 345))
forgot_new_password_textbox = pygame.Rect(440, 460, 400, 50)


def update_textbox(text,event,font):

    if event.key == pygame.K_BACKSPACE:
        text = text[:-1]

    elif len(text) < 18:
        text += event.unicode

    else:
        surf = font.render(text,True,(201,184,240))
        return text,surf,False


    surf = font.render(text,True,(201,184,240))
    return text,surf,True


def show_error(message):
    global error_surf,error_rect

    error_surf = error_font.render(message, True, (220,80,80))
    error_rect = error_surf.get_rect(center = (640,545))


def handle_textbox_input(text,event,font,textbox):
    text, surf,result = update_textbox(text, event, font)
    rect = surf.get_rect(center = textbox.center)

    if not result:
        show_error("Character limit Reached!")
    
    return text,surf,rect


def reset_form(target_state):
    global username, password, passkey, new_password
    global username_surf, password_surf, passkey_surf, new_password_surf
    global error_surf, error_rect, active_box, state
    
    username = password = passkey = new_password = ""
    active_box = ""
    state = target_state
    
    username_surf = username_text_font.render("", True, (201,184,240))
    password_surf = password_text_font.render("", True, (201,184,240))
    passkey_surf = passkey_text_font.render("", True, (201,184,240))
    new_password_surf = new_password_text_font.render("", True, (201,184,240))
    error_surf = error_font.render("", True, (220,80,80))


def draw_form(show_password, show_passkey=True, show_new_password=False, show_forgot=False):
    screen.fill((13,11,20))
    
    screen.blit(username_label_surf, username_label_rect)
    pygame.draw.rect(screen,(19,16,31),username_textbox,border_radius=15)
    screen.blit(username_surf, username_rect)


    if show_password:
        screen.blit(password_label_surf, password_label_rect)
        pygame.draw.rect(screen,(19,16,31),password_textbox,border_radius=15)
        screen.blit(password_surf, password_rect)


    if show_passkey:
        if state == "FORGOT MENU":
            screen.blit(passkey_label_surf, forgot_passkey_label_rect)
            pygame.draw.rect(screen,(19,16,31),forgot_passkey_textbox,border_radius=15)
            screen.blit(passkey_surf, passkey_surf.get_rect(center=forgot_passkey_textbox.center))

        else:
            screen.blit(passkey_label_surf, passkey_label_rect)
            pygame.draw.rect(screen,(19,16,31),passkey_textbox,border_radius=15)
            screen.blit(passkey_surf, passkey_rect)
        

    if show_new_password:
        screen.blit(new_password_label_surf, new_password_label_rect)
        pygame.draw.rect(screen,(19,16,31),forgot_new_password_textbox,border_radius=15)
        screen.blit(new_password_surf, new_password_surf.get_rect(center=forgot_new_password_textbox.center))

        
    if show_forgot:
        screen.blit(forgot_surf, forgot_rect)
        

    pygame.draw.rect(screen,(90,31,209),submit_button,border_radius=15)
    screen.blit(submit_surf, submit_rect)
    screen.blit(back_surf, back_rect)
    screen.blit(error_surf, error_rect)



# GAME MENU

backround_img = pygame.image.load("assets/main_menu_bg.png").convert_alpha()

play_button_img = pygame.image.load("assets/play_button.png").convert_alpha()
play_button_img = pygame.transform.smoothscale(play_button_img, (160, 160))
play_button_rect = play_button_img.get_rect(center =(640, 420))

settings_img = pygame.image.load("assets/settings.png").convert_alpha()
settings_img = pygame.transform.smoothscale(settings_img, (80, 80))
settings_rect = settings_img.get_rect(center=(1170, 620))


def draw_game_menu():
    screen.fill((0,0,0))
    screen.blit(backround_img, (0,0))

    screen.blit(play_button_img, play_button_rect)
    screen.blit(settings_img, settings_rect)


while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if state == "MAIN MENU":
            if event.type == pygame.MOUSEBUTTONDOWN:

                if sign_button.collidepoint(pygame.mouse.get_pos()):
                    state = "SIGNUP MENU"

                elif login_button.collidepoint(pygame.mouse.get_pos()):
                    state = "LOGIN MENU"



        elif state == "SIGNUP MENU" or state == "LOGIN MENU":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if username_textbox.collidepoint(mouse_pos):
                    active_box = "username"

                elif back_button.collidepoint(mouse_pos):
                    reset_form("MAIN MENU")

                elif password_textbox.collidepoint(mouse_pos) and state != "FORGOT MENU":
                    active_box = "password"

                elif passkey_textbox.collidepoint(mouse_pos) and state == "SIGNUP MENU":
                    active_box = "passkey"

                elif forgot_button.collidepoint(mouse_pos) and state == "LOGIN MENU":
                    state = "FORGOT MENU"

                elif state == "SIGNUP MENU" and submit_button.collidepoint(mouse_pos):
                    result1 = auth_manager.username_verifier(username)
                    result2 = auth_manager.pass_verifier(password) 
                    result3 = auth_manager.pass_verifier(passkey)

                    if result1 and result2 and result3:
                        hashed_password = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
                        hashed_passkey = bcrypt.hashpw(passkey.encode(),bcrypt.gensalt()).decode()

                        credentials = auth_manager.add_and_change_credentials(username,hashed_password,hashed_passkey)
                        file_manager.save_user_credentials(credentials)
                        state = "GAME MENU"
                        auth_manager.currentuser = username

                    else:
                        show_error("Username or password or passkey is invalid!")

                elif forgot_passkey_textbox.collidepoint(mouse_pos) and state == "FORGOT MENU":
                        active_box = "passkey"

                elif forgot_new_password_textbox.collidepoint(mouse_pos) and state == "FORGOT MENU":
                        active_box = "new password"


                elif state == "LOGIN MENU" and submit_button.collidepoint(mouse_pos):
                    result = auth_manager.login(username,password)

                    if result:
                        auth_manager.currentuser = username
                        state = "GAME MENU" 
                    else:
                        error_surf = error_font.render("Invalid username or password!", True, (220,80,80))
                        error_rect = error_surf.get_rect(center = (640,545))

                elif state == "FORGOT MENU" and submit_button.collidepoint(mouse_pos):
                    result,credentials = auth_manager.forgot_password(username,passkey,new_password)

                    if not result:
                        show_error("Username or password or passekey is invalid!")
                    else:
                        file_manager.save_user_credentials(credentials)
                        reset_form("LOGIN MENU")


                else:
                    active_box = None


            if event.type == pygame.KEYDOWN:
                if active_box == "username":
                    username,username_surf,username_rect = handle_textbox_input(username,event,button_font,username_textbox)

                elif active_box == "password":
                    password,password_surf,password_rect = handle_textbox_input(password,event,button_font,password_textbox)
                
                elif active_box == "passkey":
                    box = forgot_passkey_textbox if state == "FORGOT MENU" else passkey_textbox
                    passkey,passkey_surf,passkey_rect = handle_textbox_input(passkey,event,button_font,box) 

                elif active_box == "new password":
                    new_password,new_password_surf,new_password_rect = handle_textbox_input(
                        new_password,event,button_font,forgot_new_password_textbox)



        elif state == "GAME MENU":
            if event.type == pygame.MOUSEBUTTONDOWN:
                    
                if play_button_rect.collidepoint(event.pos):
                    state = "CHARACTER MENU"

                elif settings_rect.collidepoint(event.pos):
                    state = "SETTINGS MENU"




    if state == "MAIN MENU":
        draw_main_menu()

    elif state == "SIGNUP MENU":    
        draw_form(show_password = True,show_passkey=True,show_new_password= False, show_forgot= False)

    elif state == "LOGIN MENU":
        draw_form(show_password=True, show_passkey= False, show_new_password= False, show_forgot= True)

    elif state == "FORGOT MENU":
        draw_form(show_password= False,show_passkey= True, show_new_password= True, show_forgot = False)


    if state == "GAME MENU":
        draw_game_menu()

    elif state == "CHARACTER MENU":
        pass

    elif state == "SETTINGS MENU":
        pass

    print(state)
    pygame.display.update()
    clock.tick(60)