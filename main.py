import pygame
import bcrypt
import random

from user_data_manager import FileManager,AuthManager,FileMissingError,FileCorruptedError,Stats
from battle_mech import Character, Gojo, Sukana, Yuji, Megumi, Mahito, BattleManager

#battle_manager
file_manager = FileManager()

gojo = Gojo()
sukana = Sukana()
yuji = Yuji()
megumi = Megumi()
mahito = Mahito()


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



game_menu_bg_img = pygame.image.load("assets/others/game-menu.png").convert_alpha()

play_button_img = pygame.image.load("assets/others/play_button.png").convert_alpha()
play_button_img = pygame.transform.smoothscale(play_button_img, (160, 160))
play_button_rect = play_button_img.get_rect(center =(640, 420))

settings_img = pygame.image.load("assets/others/settings.png").convert_alpha()
settings_img = pygame.transform.smoothscale(settings_img, (80, 80))
settings_rect = settings_img.get_rect(center=(1170, 620))


def draw_game_menu():
    screen.fill((0,0,0))
    screen.blit(game_menu_bg_img, (0,0))

    screen.blit(play_button_img, play_button_rect)
    screen.blit(settings_img, settings_rect)


character_object = [gojo, sukana, yuji, megumi, mahito]
character_names = ["gojo","sukana","yuji","megumi","mahito"]

character_no = 0
current_character = character_object[character_no]
displayed_character = character_names[character_no]

character_img = pygame.image.load(f"assets/{displayed_character}/character_select.png").convert_alpha()
character_img = pygame.transform.smoothscale(character_img, (400,500))

character_txt_font = pygame.font.Font(None,70)
select_txt_font = pygame.font.Font(None,38)
arrow_font = pygame.font.Font(None,150)

right_arrow_surf = arrow_font.render(">", True, (255,255,255))
right_arrow_rect = right_arrow_surf.get_rect(center=(1200,360))

left_arrow_surf = arrow_font.render("<", True, (255,255,255))
left_arrow_rect = left_arrow_surf.get_rect(center=(80,360))

select_surf = select_txt_font.render("SELECT", True, (0,220,255))
select_rect = select_surf.get_rect(center=(1190-80,665-25))


def show_stats_pre_battle(y, text):
    stats_surf = character_txt_font.render(text, True, (255,255,255))
    stats_rect = stats_surf.get_rect(topleft=(625,y))
    screen.blit(stats_surf,stats_rect)


def draw_character_menu():
    global displayed_character

    screen.fill((15,20,25))

    character_rect = character_img.get_rect(center = (315,360))
    screen.blit(character_img, character_rect)

    pygame.draw.rect(screen, (100, 70, 160), (115, 110, 400, 500), 2)
    pygame.draw.rect(screen, (70, 50, 110), (40, 40, 1200, 640), 3)

    character_name_surf = character_txt_font.render(displayed_character, True, (255,255,255))
    character_name_rect = character_name_surf.get_rect(center=(850,75))
    screen.blit(character_name_surf,character_name_rect)

    panel = pygame.Surface((550, 500), pygame.SRCALPHA)
    panel.fill((25, 15, 40, 200))
    screen.blit(panel, (585, 110))

    show_stats_pre_battle(200, f"Health: {current_character.max_hp}")
    show_stats_pre_battle(290, f"Cursed Energy: {current_character.max_ce}")
    show_stats_pre_battle(380, f"Defense: {current_character.defense}")
    show_stats_pre_battle(460, f"Speed: {current_character.speed}")


    pygame.draw.rect(screen, (0, 80, 100), (1110-80, 640-25, 160, 50), border_radius=15)

    screen.blit(select_surf,select_rect)

    screen.blit(right_arrow_surf, right_arrow_rect)
    screen.blit(left_arrow_surf, left_arrow_rect)
    

start_time = 0

pre_battle_bg_img = pygame.image.load("assets/others/pre-battle.png").convert_alpha()
pre_battle_bg_img = pygame.transform.smoothscale(pre_battle_bg_img,(1280,720))

select_surf = select_txt_font.render("Next", True, (0,220,255))
select_rect = select_surf.get_rect(center=(1190-80,665-25))

center_x = 1220
center_y = 680

font = pygame.font.Font(None, 28)
next_surf = font.render("NEXT", True, (255, 255, 255))
next_rect = next_surf.get_rect(center=(center_x, center_y))

ai = random.choice(character_object)
ai_character = ai.name


def draw_pre_battle_menu():
    global displayed_character

    if start_time/1000 - start_time <= 8000:
        state = "BATTLE MENU"

    screen.fill((0,0,0))
    
    screen.blit(pre_battle_bg_img,(0,0))

    pygame.draw.circle(screen, (80,10,20), (center_x, center_y), 35)

    screen.blit(next_surf, next_rect)

    ai_img = pygame.image.load(f"assets/{ai_character}/pre_battle.png").convert_alpha()
    ai_img = pygame.transform.smoothscale(ai_img, (320,300))
    ai_img = pygame.transform.flip(ai_img, True, False)
    screen.blit(ai_img, (900,314))

    player_img = pygame.image.load(f"assets/{displayed_character}/pre_battle.png").convert_alpha()
    player_img = pygame.transform.smoothscale(player_img, (320,300))
    screen.blit(player_img, (60,99))


battle_menu_img = pygame.image.load("assets/others/battle-menu.png").convert_alpha()
battle_menu_img = pygame.transform.smoothscale(battle_menu_img, (1280,720))

awakening_img = pygame.image.load("assets/others/awakening.png").convert_alpha()
awakening_img = pygame.transform.smoothscale(awakening_img, (220,130))
awakening_rect = awakening_img.get_rect(topleft = (60, 475))

stats_font = pygame.font.Font(None,70)

battle_manager = BattleManager(player = current_character, ai = ai)
player = current_character

moves_font = pygame.font.Font(None, 33)

hp_img = pygame.image.load("assets/others/hp_bar.png")
ce_img = pygame.image.load("assets/others/ce_bar.png")

ai_img = pygame.image.load(f"assets/{ai_character}/battle.png").convert_alpha()
ai_img = pygame.transform.smoothscale(ai_img, (85,85))
ai_img = pygame.transform.flip(ai_img, True, False)
ai_img_rect = ai_img.get_rect(center = (1207,69))

player_img = pygame.image.load(f"assets/{displayed_character}/battle.png").convert_alpha()
player_img = pygame.transform.smoothscale(player_img, (85,85))
player_img_rect = player_img.get_rect(center = (73,66))

ai_full_img = pygame.image.load(f"assets/{ai_character}/character_select.png").convert_alpha()
ai_full_img = pygame.transform.smoothscale(ai_full_img, (400, 450))
ai_full_img = pygame.transform.flip(ai_full_img, True, False)
ai_full_img_rect = ai_full_img.get_rect(center = (1082,390))

character_img = pygame.transform.smoothscale(character_img, (400, 450))

move2_rect = pygame.Rect(70, 220, 230, 65)
move1_rect = pygame.Rect(70, 310, 230, 65)
move3_rect = pygame.Rect(70, 400, 230, 65)


def show_stats_battle_menu(y, x, text, text_color):
    stats_surf = moves_font.render(text, True, text_color)
    stats_rect = stats_surf.get_rect(topleft=(x,y))
    screen.blit(stats_surf,stats_rect)

    return stats_rect


def show_bars(character, location1, location2):

    width1 = round(character.hp / character.max_hp * 356)
    width2= round(character.ce / character.max_ce * 213)
    height = 20

    bar1 = pygame.transform.smoothscale(hp_img, (width1, height))
    bar2 = pygame.transform.smoothscale(ce_img, (width2, height))
    bar2_flipped = pygame.transform.flip(bar2, True, False)

    screen.blit(bar1, location1)
    screen.blit(bar2_flipped, location2)

state = "BATTLE MENU"

def draw_battle_menu():
    screen.fill((0,0,0))

    screen.blit(battle_menu_img, (0,0))

    # Fill colour (dark purple) + border colour (lighter purple)
    fill_col = (40, 20, 60)
    border_col = (140, 100, 200)

    pygame.draw.rect(screen, fill_col, move1_rect, border_radius=10)      # filled interior
    pygame.draw.rect(screen, border_col, move1_rect, 3, border_radius=10) # border outline
#turn_flow
    pygame.draw.rect(screen, fill_col, move2_rect, border_radius=10)
    pygame.draw.rect(screen, border_col, move2_rect, 3, border_radius=10)

    pygame.draw.rect(screen, fill_col, move3_rect, border_radius=10)
    pygame.draw.rect(screen, border_col, move3_rect, 3, border_radius=10)

    screen.blit(player_img, player_img_rect)
    screen.blit(ai_img, ai_img_rect)

    show_bars(player, (175, 54), (174, 80))
    show_bars(ai, (753, 54), (893, 80))

    battle_manager.check_awakening()

    if player.can_awaken:
        screen.blit(awakening_img, awakening_rect)

    battle_manager.get_available_moves(player)
    y = 220
    x = 70


    for move in player.available_moves:

        show_stats_battle_menu(y, x, move["name"], (255, 0, 0))
        show_stats_battle_menu(y+25, x, f"Damage: {move['damage']}", (0,0,0))
        show_stats_battle_menu(y+45, x, f"Cursed Energy: {move['CE']}", (0,0,0))

        y += 90
        if y > 400:
            break


    character_img_rect = character_img.get_rect(center = (575,390))
    screen.blit(character_img, character_img_rect)
    screen.blit(ai_full_img, ai_full_img_rect)

    
    #print(pygame.mouse.get_pos())

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.USEREVENT:
            pygame.mixer.music.pause() 

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


        elif state == "CHARACTER MENU":
            if event.type == pygame.MOUSEBUTTONDOWN:

                if left_arrow_rect.collidepoint(event.pos):

                    if character_no != 0:
                        character_no -= 1

                        current_character = character_object[character_no]
                        displayed_character = character_names[character_no]

                        character_img = pygame.image.load(f"assets/{displayed_character}/character_select.png").convert_alpha()
                        character_img = pygame.transform.smoothscale(character_img, (400,500))


                elif right_arrow_rect.collidepoint(event.pos):

                    if character_no != 4:
                        character_no += 1

                        current_character = character_object[character_no]
                        displayed_character = character_names[character_no]

                        character_img = pygame.image.load(f"assets/{displayed_character}/character_select.png").convert_alpha()
                        character_img = pygame.transform.smoothscale(character_img, (400,500))

                
                
                elif select_rect.collidepoint(event.pos):
                    state = "PRE-BATTLE MENU"
                    start_time = pygame.time.get_ticks()

                    player = current_character

                    player_img = player_img = pygame.image.load(f"assets/{displayed_character}/battle.png").convert_alpha()
                    player_img = pygame.transform.smoothscale(player_img, (85,85))
                    player_img_rect = player_img.get_rect(center = (73,66))


        elif state == "PRE-BATTLE MENU":
            if event.type == pygame.MOUSEBUTTONDOWN:

                if next_rect.collidepoint(pygame.mouse.get_pos()):
                    state = "BATTLE MENU"
                    

        elif state == "BATTLE MENU":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if move1_rect.collidepoint(mouse_pos) and battle_manager.current_turn == player:
                    move = battle_manager.player.available_moves[0]
                    battle_manager.move = move
                    battle_manager.turn_flow()

                elif move2_rect.collidepoint(mouse_pos) and battle_manager.current_turn == player:
                    move = battle_manager.player.available_moves[1]
                    battle_manager.move = move
                    battle_manager.turn_flow()

                elif move3_rect.collidepoint(mouse_pos) and battle_manager.current_turn == player:
                    move = battle_manager.player.available_moves[2]
                    battle_manager.move = move
                    battle_manager.turn_flow()

                battle_manager.turn_flow()
                print(player.hp)
                print(player.ce)
                print(ai.hp)
                print(ai.ce)


    if state == "MAIN MENU":
        draw_main_menu()

    elif state == "SIGNUP MENU":    
        draw_form(show_password = True,show_passkey=True,show_new_password= False, show_forgot= False)

    elif state == "LOGIN MENU":
        draw_form(show_password=True, show_passkey= False, show_new_password= False, show_forgot= True)

    elif state == "FORGOT MENU":
        draw_form(show_password= False,show_passkey= True, show_new_password= True, show_forgot = False)


    if state == "GAME MENU":
        pygame.mixer.music.load("assets/soundtracks/Concrete_Fracture.mp3")
        pygame.mixer.music.play(0)                        
        pygame.mixer.music.set_endevent(pygame.USEREVENT) 

        draw_game_menu()

    elif state == "CHARACTER MENU":
        pygame.mixer.music.load("assets/soundtracks/Cursed_Strike.mp3")
        pygame.mixer.music.play(0)                        
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        draw_character_menu()

    elif state == "SETTINGS MENU":
        pass

    elif state == "PRE-BATTLE MENU":
        pygame.mixer.music.load("assets/soundtracks/Domain_Collapse.mp3")
        pygame.mixer.music.play(0)                        
        pygame.mixer.music.set_endevent(pygame.USEREVENT)


        draw_pre_battle_menu()

    elif state == "BATTLE MENU":
        pygame.mixer.music.load("assets/soundtracks/Metal_Lung.mp3")
        pygame.mixer.music.play(0)                        
        pygame.mixer.music.set_endevent(pygame.USEREVENT)


        draw_battle_menu()



    pygame.display.update()
    clock.tick(60)