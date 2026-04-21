from random import choices


class Character():
    def __init__(self,name,hp,ce,defense,speed,moves,awakened_moves):

        self.name = name
        self.hp = hp
        self.ce = ce
        self.defense = defense
        self.speed = speed
        self.moves = moves
        self.awakened_moves = awakened_moves
        self.max_ce = ce
        self.max_hp = hp


        self.is_awakened = False
        self.has_awakened = False
        self.awakened_turns_left = 0
        self.can_awaken = False



        self.player_effects = {}
        self.ai_effects = {}


class Gojo(Character):
    def __init__(self):
        moves = [
            {"name": "Consecutive Punches","damage": 10,"CE": 15},
            {"name": "Red","damage":20,"CE": 30},
            {"name": "Blue","damage": 15,"CE": 23},

        ]

        awakened_moves = [
            {"name": "Max Blue","damage": 25,"CE": 38},
            {"name": "Max Red","damage": 30,"CE": 45},
            {"name": "Max Purple","damage": 40,"CE":60},

            {"name": "domain expansion","damage": 0,"CE": 100,"effects":{"stun":{"turns": 2,"chance": 100},
            "damage debuff": {"multiplier": 0.7, "turns": 2},"damage buff": {"multiplier": 1.3, "turns": 1,"chance": 100}}}
        ]

        super().__init__("Gojo", 540, 300, 85 , 95, moves, awakened_moves)

class Sukana(Character):
    def __init__(self):

        moves = [{"name": "Consecutive Punches","damage":10,"CE": 15},
                {"name": "Dismantle","damage":25,"CE": 38},
                {"name": "Cleave","damage":20,"CE": 35}
                 ]
        
        awakened_moves = [
            {"name": "Rush","damage": 30,"CE": 45},
            {"name": "Max Dismantle","damage": 30,"CE": 45,},
            {"name": "Fuga","damage": 40,"CE":60},
            {"name": "domain expansion","damage": 0,"CE": 100,"effects":{"passive damage":{"damage": 30, "turns": 3}}}
        ]       

        super().__init__("Sukana", 480, 400, 80 , 75, moves, awakened_moves)

class Yuji(Character):
    def __init__(self):

        moves = [
            {"name": "Cursed Blow","damage":15,"CE": 23},
            {"name": "Cursed Strike","damage":25,"CE": 38},

            {"name": "Divergent Fist","damage":20,"CE": 100,"effects":{"stun":{"turns": 1, "chance": 0.8}
            ,"damage buff":{"multiplier": 2.5,"turns":1,"chance": 0.5}}}                 
        ]

        awakened_moves = [
            {"name": "Supernova","damage":0 ,"CE": 100,"effects":{"pending damage":{"damage":70,"turns":2}}},
            {"name": "Chained Black Flash","damage": 40,"CE": 45,},
            {"name": "Piercing Blood","damage": 40,"CE":60},
            {"name": "BrotherHood bond","damage": 0,"CE": 100,"effects":{"damage buff":{"multiplier":1.5,"turns":3,"chance":100}}}
        ]

        super().__init__("Yuji", 450, 350 , 90 , 85 ,moves, awakened_moves)

class Megumi(Character):
    def __init__(self):

        moves = [
            {"name": "Nue","damage":20,"CE": 30},
            {"name": "Rabbit Escape","damage":15,"CE": 23},
            {"name": "Demon Dogs","damage":25,"CE": 38}
                 ]
        

        awakened_moves = [
            {"name": "Snake","damage": 30,"CE": 45},
            {"name": "Max Elephant","damage": 40,"CE": 60},

            {"name": "Mahoraga","damage": 0,"CE":100,"Turns":2,"effects":
            {"stun":{"self stun":{"turns":2},"opp stun":{"turns":1}},"pending damage":{"damage":70,"turns":2}}},

            {"name": "domain expansion","damage": 0,"CE": 100,"effects":
            {"damage buff":{"multiplier":1.25,"turns":3,"chance":100},"CE reduc":{"multiplier":0.8,"turns":3}}}
        ] 


        super().__init__("Megumi", 510 , 320 , 80 , 65 , moves, awakened_moves) 


class Mahito(Character):
    def __init__(self):

        moves = [
            {"name": "Body Repel","damage":30,"CE": 45},
            {"name": "Soul Multiplicity","damage":20,"CE": 35},
            {"name": "Black Flash","damage":25,"CE": 38}
                 ]
        
        awakened_moves = [
            {"name": "Idle Transfiguration","damage": 30,"CE": 45,},
            {"name": "Polymorphic Soul Isomer","damage": 30,"CE": 40,},
            {"name": "Instant Spirit Body","damage": 40,"CE":60,"effects":{"hp buff": +30, "defense buff": +30}},
            {"name": "domain expansion","damage": 0,"CE": 100,"effects":{"defense opp debuff":{"multiplier":0.4,"turns":3}}}
        ] 


        super().__init__("Mahito", 450 , 300, 90 , 65 , moves, awakened_moves) 


class BattleManager():
    def __init__(self,player,ai):

        self.player = player
        self.ai = ai

        self.attacker = None
        self.defender = None

        self.battle_over = False
        self.winner = None

        self.player_effects = {}
        self.ai_effects = {}

        self.move = None
        self.player_turn_counter = 0
        self.ai_turn_counter = 0
        self.current_turn = None

        self.attacker_effects = {"stun": 0,"damage buff": {"multiplier":0,"turns":0},"damage debuff":
        {"multiplier":0,"turns":0},"defense buff": {"multiplier":0,"turns":0}, "defense debuff":
        {"multiplier":0,"turns":0}, "CE reduc": {"multiplier":0,"turns":0},"passive damage": 
        {"damage":0,"turns":0},"defense opp debuff":{"multiplier":0,"turns":0},"pending damage":{"damage":0,"turns":0}
        ,"hp buff":0, "active domain turns": 0}

        self.defender_effects = {"stun": 0,"damage buff": {"multiplier":0,"turns":0},"damage debuff":
        {"multiplier":0,"turns":0},"defense buff": {"multiplier":0,"turns":0}, "defense debuff":
        {"multiplier":0,"turns":0}, "CE reduc": {"multiplier":0,"turns":0},"passive damage": 
        {"damage":0,"turns":0},"defense opp debuff":{"multiplier":0,"turns":0},"pending damage":{"damage":0,"turns": 0}
        ,"hp buff":0, "active domain turns": 0}

        self.player_domain_effects = {}
        self.ai_domain_effects = {}

        self.awakening = 0
        self.awaken


    def calculate_damage(self):
        damage = self.move["damage"]

        if self.attacker_effects["damage buff"]["turns"]:

            chance = self.move["effects"]["damage buff"]["chance"]
            choice = choices([True,False], weights=[chance,100-chance])[0]   #---- WHAT DOES THIS [0] MEAN..

            if choice and ["turns"]:

                if self.move["effects"]["damage buff"]["turns"]:
                    damage *= self.move["effects"]["damage buff"]["multiplier"]


        if self.move["effects"]["damage debuff"]["turns"]:
            damage *= self.move["effects"]["multiplier"]

        else:
            damage_buff = 0
            damage_debuff = 0


        damage = damage*(1 + damage_buff)*(1 - damage_debuff)


        if self.attacker_effects["passive damage"]["turns"]:
            damage += self.attacker_effects["passive damage"]["damage"]


        if self.attacker_effects["pending damage"]["turns"]:   
            damage += self.attacker_effects["pending damage"]["damage"]

        return damage

    def apply_damage(self,damage):
        defense = self.defender.defense
        defense_debuff = 1
        defense_buff = 1

        if self.attacker_effects["defense opp debuff"]["turns"]:
            defense_debuff *= self.attacker_effects["defense opp debuff"]["multiplier"]

        applied_damage = damage - (defense*defense_debuff*defense_buff / 20)

        self.defender.hp -= applied_damage


    def apply_ce_cost(self):
        if self.attacker_effects["CE reduc"]["turns"]:
            self.attacker.ce -= self.move["CE"]*self.attacker_effects["CE reduc"]["multiplier"]

        else:
            self.attacker.ce -= self.move["CE"]
        
    def recover_ce(self,character):
        if character.max_ce - 20 >= character.ce:
            character.ce += 20
        
        else:
            character.ce = character.max_ce

    def ce_recovery(self):
        
        self.recover_ce(self.player)
        self.recover_ce(self.ai)


    def turn_decrementer(self,effect_dict):

        for values in effect_dict.items():
            if isinstance(values, dict) and "turns" in values:
                
                if values["turns"] > 0:
                    values["turns"] -= 1

    def turn_decrementer(self):

        self.turn_decrementer(self.player_effects)
        self.turn_decrementer(self.ai_effects)


    def apply_effects(self):

        self.turn_decrementer()

        for effect, values in self.move.get("effects", {}).items():

            if effect == "stun":
                if self.attacker_effects["stun"]["turns"] == 0:

                    if "self stun" in values:
                        self.attacker_effects["stun"] += values["self stun"]["turns"]

                    if "opp stun" in values:
                        self.defender_effects["stun"] += values["opp stun"]["turns"]

                    if "turns" in values: 
                        self.defender_effects["stun"] += values["turns"]
                

            elif effect == "damage buff":

                if self.attacker_effects["damage buff"]["turns"] == 0:

                    self.attacker_effects["damage buff"]["turns"] = values["turns"]
                    self.attacker_effects["damage buff"]["damage"] = values["damage"]


            elif effect == "damage debuff":
                
                if self.attacker_effects["damage debuff"]["turns"] == 0:

                    self.attacker_effects["damage debuff"]["turns"] = values["turns"]
                    self.attacker_effects["damage debuff"]["damage"] = values["damage"]


            elif effect == "hp buff":
                if self.attacker.hp <= self.attacker.max_hp - values:
                    self.attacker.hp += values 

                elif self.attacker.hp < self.attacker.max_hp:
                    self.attacker.hp = self.attacker.max_hp
 
 
            elif effect == "defense buff":
                self.attacker.defense += values


            elif effect == "defense opp debuff":

                if self.attacker_effects["defense opp debuff"]["turns"] == 0:

                    self.attacker_effects["defense opp debuff"]["turns"] = values["turns"]
                    self.attacker_effects["defense opp debuff"]["damage"] = values["damage"]
                

            elif effect == "CE reduc":

                if self.attacker_effects["CE reduc"]["turns"] == 0:

                    self.attacker_effects["CE reduc"]["turns"] = values["turns"]
                    self.attacker_effects["CE reduc"]["damage"] = values["damage"]

            
            elif effect == "passive damage":

                if self.attacker_effects["passive damage"]["turns"] == 0:

                    self.attacker_effects["passive damage"]["turns"] = values["turns"]
                    self.attacker_effects["passive damage"]["damage"] = values["damage"] 

            
            elif effect == "pending damage":

                if self.attacker_effects["pending damage"]["turns"] == 0:

                    self.attacker_effects["pending damage"]["turns"] = values["turns"]
                    self.attacker_effects["pending damage"]["damage"] = values["damage"]



    def decide_winner(self):
        if self.player.hp <= 0 or self.player.ce <= 0:
            return "Computer"
        
        elif self.ai.hp <= 0 or self.ai.ce <= 0:
            return "player"
        
        return None


    def domain_clash(self):
                
        if self.current_turn == self.player and self.move["name"] == "domain expansion":

            self.attacker_effects["active domain turns"] = 3
            self.player_domain_effects = self.move["effects"]

        elif self.current_turn == self.ai and self.move["name"] == "domain expansion":

            self.attacker_effects["active domain turns"] = 3
            self.ai_domain_effects = self.move["effects"]


        if self.attacker_effects["active domain turns"] and self.move["name"] == "domain expansion":
            loser = self.ai if self.player.ce > self.ai.ce else self.player


        if loser == self.player:
            for effect in self.player_domain_effects:

                if effect in self.player_effects:

                    self.player_effects[effect]["turns"] = 0
                            
                    if "multiplier" in self.player_effects[effect]:
                        self.player_effects[effect]["multiplier"] = 0 
                        
                    if "passive damage" in self.player_effects[effect]:
                        self.player_effects[effect]["damage"] = 0



        elif loser == self.ai:
            for effect in self.ai_domain_effects:

                if effect in self.ai_effects:

                    self.ai_effects[effect]["turns"] = 0

                    if "multiplier" in self.player_effects[effect]:
                        self.ai_effects[effect]["multiplier"] = 0 
                        
                    if "passive damage" in self.player_effects[effect]:
                        self.ai_effects[effect]["damage"] = 0



    def turn_executer(self):
            self.check_awakening()

            self.apply_effects()

            self.domain_clash()

            damage = self.calculate_damage()   

            self.apply_damage(damage)

            self.apply_ce_cost()
            self.ce_recovery()

            result = self.decide_winner()
            if result:
                self.battle_over = True
                self.winner = self.player if result == "player" else self.ai
        

    def turn_flow(self):

        if self.player_turn_counter == self.ai_turn_counter and self.player.speed > self.ai.speed:
            self.current_turn = self.player
        
        elif self.ai_turn_counter > self.player_turn_counter:
            self.current_turn = self.player

        else:
            self.current_turn = self.ai

        if self.current_turn == self.player:

            self.attacker_effects.update(self.player_effects)
            self.defender_effects.update(self.ai_effects)

            if not self.player_effects["stun"]:

                self.player_turn_counter += 1

                self.attacker = self.player
                self.defender = self.ai

                self.turn_executer()

                self.player_effects.update(self.attacker_effects)
                self.ai_effects.update(self.defender_effects) 

            else:
                self.turn_decrementer()
           

        elif self.current_turn == self.ai:

            self.attacker_effects.update(self.ai_effects)
            self.defender_effects.update(self.player_effects)

            if not self.ai_effects["stun"]:

                self.ai_turn_counter += 1

                self.attacker = self.ai
                self.defender = self.player

                self.ai_turn_select()
                
                self.turn_executer()

                self.ai_effects.update(self.attacker_effects)
                self.player_effects.update(self.defender_effects)

            else:
                self.turn_decrementer()


    def check_awakening(self):
        if self.awakened_turns_left == 0:
            self.is_awakened = False

        if self.player_turn_counter >= 6 and not self.player.has_awakened:
            self.player.can_awaken = True

        elif self.ai_turn_counter >= 6 and not self.ai.has_awakened:
            self.ai.can_awaken = True


    def ai_turn_select(self):
        available_moves = []

        if self.ai.is_awakened:

            for move in self.ai.awakened_moves:
                if self.ai.ce >= move["CE"]:

                    available_moves.append({**move, "score" : 0}) # Creates a new dict with score : 0, like appends it in the new dict
        else:

            for move in self.ai.moves:
                if self.ai.ce >= move["CE"]:

                    available_moves.append({**move, "score" : 0})


        if not available_moves:
            self.move = "wait"


        elif self.player_effects["active domain turns"] and next((move for move in available_moves if move["name"] == "domain expansion"), None):
            self.move = next(move for move in available_moves if move["name"] == "domain expansion")

        elif max(available_moves, key = lambda m: m["damage"])["damage"] >= self.defender.hp:
            self.move = max(available_moves, key = lambda m: m["damage"])

        else:

            if self.ai.hp / self.ai.max_hp <= 0.3:
                available_moves[max(available_moves, key = lambda m: m["damage"])]["score"] += 3 # so it access the returned move data and access its score and increament 3 to it.
            
            if self.ai.ce / self.ai.max_ce <= 0.3:
                available_moves[min(available_moves, key = lambda m: m["CE"])]["score"] += 3

            if self.ai.ce / self.ai.max_ce > 0.3 and self.ai.hp / self.ai.max_hp > 0.3:
                available_moves[max(available_moves, key = lambda m: m["damage"])]["score"] += 2

            if self.ai.ce / self.ai.max_ce >= 0.5:

                if self.ai.can_awaken:
                    self.awakening += 2

            if self.player.has_awakened:

                if self.ai.can_awaken:
                    self.awakening += 2

        
            for moves in available_moves:

                if "effects" in moves:
                    for effects in moves["effects"]:
                        
                            if isinstance(self.player_effects.get(effects), dict) and self.player_effects[effects]["turns"]:

                                if effects in self.player_effects[effects]:
                                    moves["score"] -= 2
            

            if self.awakening >= sorted(available_moves, key = lambda m: m["score"], reverse = True)[1]:

                self.is_awakened = True
                self.has_awakened = True
                self.awakened_turns_left = 3


            self.move = available_moves[max(available_moves, key = lambda m: m["score"])]
