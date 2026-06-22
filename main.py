import pygame, sys, random

pygame.init()
pygame.font.init()

screenwidth = 1000
screenheight = 500
win = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption("An Algebraic Adventure")

current_fighter = 1
total_fighters = 2
action_cooldown = 0
action_wait_time = 90

question_cooldown = 0
question_wait_time = 120

levelup_cooldown = 0
levelup_wait_time = 60

font = pygame.font.SysFont("Arial", 26)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

clicked = False

#images
bg = [pygame.image.load('Resources/Backgrounds/levelmush.png'), pygame.image.load('Resources/Backgrounds/levelgob.png'), pygame.image.load('Resources/Backgrounds/levelfly.png'), pygame.image.load('Resources/Backgrounds/levelskel.png'), pygame.image.load('Resources/Backgrounds/levelwiz.png'), pygame.image.load('Resources/Backgrounds/Opening.png')]
story_mode = pygame.image.load('Resources/Backgrounds/story.png')
rules_mode = pygame.image.load('Resources/Backgrounds/rules.png')
#fps
clock = pygame.time.Clock()
fps = 27

base_font = pygame.font.SysFont("Arial", 26)
user_text = ""

feedval = 0
feed = [pygame.image.load('Resources/Feedmark/ansright.png'), pygame.image.load('Resources/Feedmark/answrong.png')]

level = -1
levele = 0
levelquestions = []
levelanswers = []
qno = 0

exp_time = True
etime = True

bonus = 0
level_over = 0
victory = pygame.image.load('Resources/Level_Result/victory.png')
victory = pygame.transform.scale(victory, (round(victory.get_width() * 0.5), round(victory.get_height() * 0.5)))
defeat = pygame.image.load('Resources/Level_Result/defeat.png')
defeat = pygame.transform.scale(defeat, (round(defeat.get_width() * 0.5), round(defeat.get_height() * 0.5)))
start = pygame.image.load('Resources/Buttons/Start.png')
story = pygame.image.load('Resources/Buttons/Story.png')
rules = pygame.image.load('Resources/Buttons/Rules.png')
ending = pygame.image.load('Resources/Backgrounds/Ending.png')

#level 1 questions and answers
leveloneq = []

for i in range(1, 21):
    qs = pygame.image.load(f'Resources/level1q/{i}.png')
    leveloneq.append(qs)

levelonea = ["5", "18", "20", "6", "4", "-13", "34", "80", "-4", "-12", "8", "0", "13", "1", "-16", "-108", "24", "-4", "-7", "-75"]

levelquestions.append(leveloneq)
levelanswers.append(levelonea)

#level 2 questions and answers
leveltwoq = []

for i in range(1, 21):
    qs = pygame.image.load(f'Resources/level2q/{i}.png')
    leveltwoq.append(qs)

leveltwoa = ["0", "5", "-6", "11", "20", "-20", "11", "21", "-1", "7", "1", "-11", "4", "15", "18", "-21", "3", "0", "16", "3"]

levelquestions.append(leveltwoq)
levelanswers.append(leveltwoa)

#level 3 questions and answers
levelthreeq = []

for i in range(1, 21):
    qs = pygame.image.load(f'Resources/level3q/{i}.png')
    levelthreeq.append(qs)

levelthreea = ["4x^{5}", "2", "4x^{4}y^{2}", "4x^{2}", "16x^{6}", "1/16x^{8}", "y^{3}/2x^{4}", "1/2x", "4x^{5}", "1/2", "x", "1", "256", "6xy^{2}", "8x", "1/9x^{2}", "12/xy", "x^{5}/y^{2}", "8x^{5}", "8/x"]

levelquestions.append(levelthreeq)
levelanswers.append(levelthreea)

#level 4 questions and answers
levelfourq = []

for i in range(1, 21):
    qs = pygame.image.load(f'Resources/level4q/{i}.png')
    levelfourq.append(qs)

levelfoura = ["-1or5", "-2or-1", "3or8", "-5or-2", "-1or4", "1", "0or8", "-7or5", "0or6/7", "1/5or3/7", "-1or-5/4", "-3/4or-3/2", "3or8", "-5or-2", "-1or4", "1", "-5or-3", "5or6", "0or13/6", "6/5or3/2"]

levelquestions.append(levelfourq)
levelanswers.append(levelfoura)

#level 5 questions and answers
levelfiveq = []

for i in range(1, 21):
    qs = pygame.image.load(f'Resources/level5q/{i}.png')
    levelfiveq.append(qs)

levelfivea = ["4x^{2}y/z", "6/5or3/2", "3", "-75", "5or6", "24", "x^{2}z^{4}/2y^{4}", "15", "0or13/6", "2x^{2}z/3y", "-4", "16", "-33", "3x^{7}/yz", "-5or-3", "18", "-1or-5/4", "z^{3}/xy^{2}", "-11", "0"]

levelquestions.append(levelfiveq)
levelanswers.append(levelfivea)

#explanations for each level
explain = []
for i in range(0, 5):
    exs = pygame.image.load(f'Resources/expla/{i}.png')
    explain.append(exs)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    win.blit(img, (x, y))

def redrawGameWindow():
    win.blit(bg[level], (0, 0))
    if level != -1:
        draw_text(f'Arick Odarin HP: {wizard.hp}', font, white, 100, 20)
        if level == 0:
            draw_text(f'Troadstool HP: {mushroom.hp}', font, white, 700, 20)
        elif level == 1:
            draw_text(f'Smugteeth HP: {goblin.hp}', font, white, 700, 20)
        elif level == 2:
            draw_text(f'Murkeye HP: {flyeye.hp}', font, white, 700, 20)
        elif level == 3:
            draw_text(f'Stinkbone HP: {skele.hp}', font, white, 700, 20)
        elif level == 4:
            draw_text(f'Alcheminus HP: {evwizard.hp}', font, white, 700, 20)

def inputs():
    global user_text
    user_text = ""

    input_rect = pygame.Rect(450, 425, 140, 32)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color("gray15")

    active = True

    runq = True

    while runq:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                    runq = False
                if active == True:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[0:-1]
                    else:
                        user_text += event.unicode
        win.blit(levelquestions[level][qno], (0, 0))
        if active:
            color = color_active
        else:
            color = color_passive

        pygame.draw.rect(win, color, input_rect, 2)

        text_surface = base_font.render(user_text, True, (250, 250, 250))
        win.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        input_rect.w = max(100, text_surface.get_width() + 10)
        pygame.display.flip()
        clock.tick(60)
    pygame.display.update()

def feedback():
    win.blit(feed[feedval], (0, 0))
    runf = True
    while runf:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        win.blit(feed[feedval], (0, 0))
        runf = False
    pygame.display.update()

def explanation():
    global useless
    useless = ""

    input_rect = pygame.Rect(375, 468, 140, 32)
    color_active = blue
    color_passive = red

    active = True

    runq = True

    while runq:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                    runq = False
                if active == True:
                    if event.key == pygame.K_BACKSPACE:
                        useless = useless[0:-1]
                    else:
                        useless += event.unicode
        win.blit(explain[levele], (0, 0))
        if active:
            color = color_active
        else:
            color = color_passive

        pygame.draw.rect(win, color, input_rect, 2)

        text_surface = base_font.render("Click Enter to Proceed!", True, (0, 0, 0))
        win.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        input_rect.w = max(100, text_surface.get_width() + 10)
        pygame.display.flip()
        clock.tick(60)
    pygame.display.update()

def storyrules():
    global useless
    useless = ""

    input_rect = pygame.Rect(375, 468, 140, 32)
    color_active = blue
    color_passive = red

    active = True

    runq = True

    while runq:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                    runq = False
                if active == True:
                    if event.key == pygame.K_BACKSPACE:
                        useless = useless[0:-1]
                    else:
                        useless += event.unicode
        if open_type == "story":
            win.blit(story_mode, (0, 0))
        elif open_type == "rules":
            win.blit(rules_mode, (0, 0))
        if active:
            color = color_active
        else:
            color = color_passive

        pygame.draw.rect(win, color, input_rect, 2)

        text_surface = base_font.render("Click Enter to Proceed!", True, (0, 0, 0))
        win.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        input_rect.w = max(100, text_surface.get_width() + 10)
        pygame.display.flip()
        clock.tick(60)
    pygame.display.update()

class Hero():
    def __init__(self, x, y, name, max_hp, strength):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        #this should be included
        self.alive = True
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #idle
        temp_list =[]
        self.animation_list = []
        for i in range(1, 7):
            img = pygame.image.load(f'Resources/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (round(img.get_width() * 1.55 * 1.75), round(img.get_height() * 1.55 * 1.75)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #attack1
        temp_list = []
        for i in range(1, 9):
            img = pygame.image.load(f'Resources/{self.name}/Attack1/{i}.png')
            img = pygame.transform.scale(img, (round(img.get_width() * 1.55 * 1.75), round(img.get_height() * 1.55 * 1.75)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #attack2
        temp_list = []
        for i in range(1, 9):
            img = pygame.image.load(f'Resources/{self.name}/Attack2/{i}.png')
            img = pygame.transform.scale(img, (round(img.get_width() * 1.55 * 1.75), round(img.get_height() * 1.55 * 1.75)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #hit
        temp_list = []
        for i in range(1, 13):
            img = pygame.image.load(f'Resources/{self.name}/Hit/{i}.png')
            img = pygame.transform.scale(img, (round(img.get_width() * 1.55 * 1.75), round(img.get_height() * 1.55 * 1.75)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #death
        temp_list = []
        for i in range(1, 16):
            img = pygame.image.load(f'Resources/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (round(img.get_width() * 1.55 * 1.75), round(img.get_height() * 1.55 * 1.75)))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 4:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        attstyl = random.randint(1, 2)
        self.action = attstyl
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        damage = self.strength
        target.hp -= damage
        target.hit()
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()

    def hit(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        self.action = 4
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        win.blit(self.image, self.rect)

class Monster():
    def __init__(self, x, y, name, max_hp, strength):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        #this should be included
        self.alive = True
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #idle
        temp_list =[]
        self.animation_list = []
        for i in range(1, 9):
            img = pygame.image.load(f'Resources/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (round(img.get_width() * 2.75 * 1.75), round(img.get_height() * 2.75 * 1.75)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #attack
        temp_list = []
        for i in range(1, 9):
            img = pygame.image.load(f'Resources/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (round(img.get_width() * 2.75 * 1.75), round(img.get_height() * 2.75 * 1.75)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #hit
        temp_list = []
        for i in range(1, 13):
            img = pygame.image.load(f'Resources/{self.name}/Hit/{i}.png')
            img = pygame.transform.scale(img, (round(img.get_width() * 2.75 * 1.75), round(img.get_height() * 2.75 * 1.75)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #death
        temp_list = []
        for i in range(1, 14):
            img = pygame.image.load(f'Resources/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (round(img.get_width() * 2.75 * 1.75), round(img.get_height() * 2.75 * 1.75)))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        damage = self.strength
        target.hp -= damage
        target.hit()
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hit(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        win.blit(self.image, self.rect)


class Healthbar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        self.hp = hp

        ratio = self.hp / self.max_hp

        pygame.draw.rect(win, red, (self.x, self.y, 350, 20))
        pygame.draw.rect(win, green, (self.x, self.y, 350 * ratio, 20))

class Button():
	def __init__(self, surface, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.surface = surface

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		self.surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

wizard = Hero(200, 380, 'Wizard', 100, 10)
mushroom = Monster(800, 375, 'Mushroom', 100, 10)
goblin = Monster(800, 375, 'Goblin', 100, 10)
flyeye = Monster(800, 375, 'Flying_Eye', 100, 10)
skele = Monster(800, 375, 'Skeleton', 100, 10)
evwizard = Monster(800, 375, 'Evil_Wizard', 100, 10)


wizard_health_bar = Healthbar(25, 50, wizard.hp, wizard.max_hp)
mushroom_health_bar = Healthbar(625, 50, mushroom.hp, mushroom.max_hp)
goblin_health_bar = Healthbar(625, 50, goblin.hp, goblin.max_hp)
flyeye_health_bar = Healthbar(625, 50, flyeye.hp, flyeye.max_hp)
skele_health_bar = Healthbar(625, 50, skele.hp, skele.max_hp)
evwizard_health_bar = Healthbar(625, 50, evwizard.hp, evwizard.max_hp)

start_button = Button(win, 300, 144, start)
story_button = Button(win, 300, 266, story)
rules_button = Button(win, 300, 388, rules)

qtime = True

# mainloop
run = True
while run:
    clock.tick(fps)
    pos = pygame.mouse.get_pos()

    if level == -1:

        # reset initializations
        wizard = Hero(200, 380, 'Wizard', 100, 10)
        mushroom = Monster(800, 375, 'Mushroom', 100, 10)
        goblin = Monster(800, 375, 'Goblin', 100, 10)
        flyeye = Monster(800, 375, 'Flying_Eye', 100, 10)
        skele = Monster(800, 375, 'Skeleton', 100, 10)
        evwizard = Monster(800, 375, 'Evil_Wizard', 100, 10)

        wizard_health_bar = Healthbar(25, 50, wizard.hp, wizard.max_hp)
        mushroom_health_bar = Healthbar(625, 50, mushroom.hp, mushroom.max_hp)
        goblin_health_bar = Healthbar(625, 50, goblin.hp, goblin.max_hp)
        flyeye_health_bar = Healthbar(625, 50, flyeye.hp, flyeye.max_hp)
        skele_health_bar = Healthbar(625, 50, skele.hp, skele.max_hp)
        evwizard_health_bar = Healthbar(625, 50, evwizard.hp, evwizard.max_hp)

        redrawGameWindow()
        start_button.draw()
        story_button.draw()
        rules_button.draw()

        if start_button.rect.collidepoint(pos) and clicked == True:
            levele = 0
            if etime == True:
                explanation()
                etime = False
            level = 0
            qno = 0
            etime = True
        elif story_button.rect.collidepoint(pos) and clicked == True:
            open_type = "story"
            storyrules()
            clicked = False
        elif rules_button.rect.collidepoint(pos) and clicked == True:
            open_type = "rules"
            storyrules()
            clicked = False

    elif level == 0:
        levele = 1
        redrawGameWindow()

        wizard.update()
        wizard.draw()
        wizard_health_bar.draw(wizard.hp)
        mushroom.update()
        mushroom.draw()
        mushroom_health_bar.draw(mushroom.hp)

        question_cooldown += 1

        if question_cooldown >= question_wait_time and wizard.alive == True and mushroom.alive == True:
            if qtime == True:
                inputs()
                if user_text == levelanswers[level][qno]:
                    feedval = 0
                    feedback()
                    pygame.time.delay(2000)
                else:
                    feedval = 1
                    feedback()
                    pygame.time.delay(2000)
                while qtime == True:
                    if user_text == levelanswers[level][qno]:
                        if wizard.alive == True:
                            action_cooldown += 1
                            if action_cooldown >= action_wait_time:
                                wizard.attack(mushroom)
                                current_fighter += 1
                                action_cooldown = 0
                                qtime = False
                        else:
                            level_over = -1
                    else:
                        if mushroom.alive == True:
                            action_cooldown += 1
                            if action_cooldown >= action_wait_time:
                                mushroom.attack(wizard)
                                current_fighter += 1
                                action_cooldown = 0
                                qtime = False
                        else:
                            level_over = 1
                        #else:
                        #    bonus = True
            qno += 1
            question_cooldown = 0
            qtime = True

        if mushroom.alive == False:
            win.blit(victory, (387, 75))
            levelup_cooldown += 1
        if wizard.alive == False:
            win.blit(defeat, (387, 75))

        if levelup_cooldown / levelup_wait_time == 1:
            wizard.hp = 100
            if etime == True:
                explanation()
                etime = False
            level = 1
            qno = 0
            etime = True


    elif level == 1:
        levele = 2
        redrawGameWindow()

        wizard.update()
        wizard.draw()
        wizard_health_bar.draw(wizard.hp)
        goblin.update()
        goblin.draw()
        goblin_health_bar.draw(goblin.hp)

        question_cooldown += 1

        if question_cooldown >= question_wait_time and wizard.alive == True and goblin.alive == True:
            if qtime == True:
                inputs()
                if user_text == levelanswers[level][qno]:
                    feedval = 0
                    feedback()
                    pygame.time.delay(2000)
                else:
                    feedval = 1
                    feedback()
                    pygame.time.delay(2000)
                while qtime == True:
                    if user_text == levelanswers[level][qno]:
                        if wizard.alive == True:
                            action_cooldown += 1
                            if action_cooldown >= action_wait_time:
                                wizard.attack(goblin)
                                current_fighter += 1
                                action_cooldown = 0
                                qtime = False
                        else:
                            level_over = -1
                    else:
                        if goblin.alive == True:
                            action_cooldown += 1
                            if action_cooldown >= action_wait_time:
                                goblin.attack(wizard)
                                current_fighter += 1
                                action_cooldown = 0
                                qtime = False
                qno += 1
                question_cooldown = 0
                qtime = True

        if goblin.alive == False:
            win.blit(victory, (387, 75))
            levelup_cooldown += 1
        if wizard.alive == False:
            win.blit(defeat, (387, 75))

        if levelup_cooldown / levelup_wait_time == 2:
            wizard.hp = 100
            if etime == True:
                explanation()
                etime = False
            level = 2
            qno = 0
            etime = True

    elif level == 2:
        levele = 3
        redrawGameWindow()

        wizard.update()
        wizard.draw()
        wizard_health_bar.draw(wizard.hp)
        flyeye.update()
        flyeye.draw()
        flyeye_health_bar.draw(flyeye.hp)

        question_cooldown += 1

        if question_cooldown >= question_wait_time and wizard.alive == True and flyeye.alive == True:
            if qtime == True:
                inputs()
                if user_text == levelanswers[level][qno]:
                    feedval = 0
                    feedback()
                    pygame.time.delay(2000)
                else:
                    feedval = 1
                    feedback()
                    pygame.time.delay(2000)
                while qtime == True:
                    if user_text == levelanswers[level][qno]:
                        if wizard.alive == True:
                            action_cooldown += 1
                            if action_cooldown >= action_wait_time:
                                wizard.attack(flyeye)
                                current_fighter += 1
                                action_cooldown = 0
                                qtime = False
                        else:
                            level_over = -1
                    else:
                        if flyeye.alive == True:
                            action_cooldown += 1
                            if action_cooldown >= action_wait_time:
                                flyeye.attack(wizard)
                                current_fighter += 1
                                action_cooldown = 0
                                qtime = False
                qno += 1
                question_cooldown = 0
                qtime = True

        if flyeye.alive == False:
            win.blit(victory, (387, 75))
            levelup_cooldown += 1
        if wizard.alive == False:
            win.blit(defeat, (387, 75))

        if levelup_cooldown / levelup_wait_time == 3:
            wizard.hp = 100
            if etime == True:
                explanation()
                etime = False
            level = 3
            qno = 0
            etime = True
            
    elif level == 3:
        levele = 4
        redrawGameWindow()

        wizard.update()
        wizard.draw()
        wizard_health_bar.draw(wizard.hp)
        skele.update()
        skele.draw()
        skele_health_bar.draw(skele.hp)

        question_cooldown += 1

        if question_cooldown >= question_wait_time and wizard.alive == True and skele.alive == True:
            if qtime == True:
                inputs()
                if user_text == levelanswers[level][qno]:
                    feedval = 0
                    feedback()
                    pygame.time.delay(2000)
                else:
                    feedval = 1
                    feedback()
                    pygame.time.delay(2000)
                while qtime == True:
                    if user_text == levelanswers[level][qno]:
                        if wizard.alive == True:
                            action_cooldown += 1
                            if action_cooldown >= action_wait_time:
                                wizard.attack(skele)
                                current_fighter += 1
                                action_cooldown = 0
                                qtime = False
                        else:
                            level_over = -1
                    else:
                        if skele.alive == True:
                            action_cooldown += 1
                            if action_cooldown >= action_wait_time:
                                skele.attack(wizard)
                                current_fighter += 1
                                action_cooldown = 0
                                qtime = False
                qno += 1
                question_cooldown = 0
                qtime = True

        if skele.alive == False:
            win.blit(victory, (387, 75))
            levelup_cooldown += 1
        if wizard.alive == False:
            win.blit(defeat, (387, 75))

        if levelup_cooldown / levelup_wait_time == 4:
            wizard.hp = 100
            if etime == True:
                explanation()
                etime = False
            level = 4
            qno = 0
            etime = True

    elif level == 4:
        levele = 5
        redrawGameWindow()

        wizard.update()
        wizard.draw()
        wizard_health_bar.draw(wizard.hp)
        evwizard.update()
        evwizard.draw()
        evwizard_health_bar.draw(evwizard.hp)

        question_cooldown += 1

        if question_cooldown >= question_wait_time and wizard.alive == True and evwizard.alive == True:
            if qtime == True:
                inputs()
                if user_text == levelonea[qno]:
                    feedval = 0
                    feedback()
                    pygame.time.delay(2000)
                else:
                    feedval = 1
                    feedback()
                    pygame.time.delay(2000)
                while qtime == True:
                    if user_text == user_text == levelonea[qno]:
                        if wizard.alive == True:
                            action_cooldown += 1
                            if action_cooldown >= action_wait_time:
                                wizard.attack(evwizard)
                                current_fighter += 1
                                action_cooldown = 0
                                qtime = False
                        else:
                            level_over = -1
                    else:
                        if evwizard.alive == True:
                            action_cooldown += 1
                            if action_cooldown >= action_wait_time:
                                evwizard.attack(wizard)
                                current_fighter += 1
                                action_cooldown = 0
                                qtime = False
                        else:
                            level_over = 1
                qno += 1
                question_cooldown = 0
                qtime = True

        if evwizard.alive == False:
            win.blit(victory, (387, 75))
            levelup_cooldown += 1
        if wizard.alive == False:
            win.blit(defeat, (387, 75))

        if levelup_cooldown / levelup_wait_time == 5:
            level = 5
    elif level == 5:
        win.blit(ending, (0, 0))
        pygame.time.delay(30000)
        run = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True

    pygame.display.update()

pygame.quit()
