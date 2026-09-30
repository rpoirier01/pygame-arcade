# Example file showing a circle moving on screen
import pygame
import random


#TO ADD:
#Enemy invulnerability indicator
#Start game/game over UI
#Powerups
#Enemy location variety/levels

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
#origin is in the top left


bullets = [] #gemini suggestion to improve rendering
enemy_bullets = []
bullet_move_speed = 10

enemies = []
enemy_hitboxes = []
enemy_locations = [pygame.Vector2(340, 100), pygame.Vector2(440,100), pygame.Vector2(540,100), pygame.Vector2(640,100), pygame.Vector2(740,100), pygame.Vector2(840,100), pygame.Vector2(940, 100)]

class Player:
    def __init__(self, player_pos = pygame.Vector2(640,680), player_health_value = 3, player_health_colors = [(0,0,0), (255, 200, 200), (255, 100, 100), (255, 0, 0)]):
        self.player_pos = player_pos
        self.player_health_value = player_health_value
        self.player_health_colors = player_health_colors

    player_invulnerability_frames = 0
    player_shot_cooldown_frames = 0
    player_rect = None
    player_size = 32

class Enemy:
    #instance parameter which is unique to each object
    #BUG each enemy shoots their first shot at the exact same time
    def __init__(self, enemy_location = pygame.Vector2(340, 100), enemy_health = 2, enemy_rect = None, enemy_shot_cooldown_frames = random.randrange(60, 120), max_left=0, max_right = 0):
        # self.enemy_range = enemy_range
        # self.enemy_size = enemy_size
        self.enemy_location = enemy_location
        self.enemy_health = enemy_health
        self.enemy_rect = enemy_rect
        self.enemy_shot_cooldown_frames = enemy_shot_cooldown_frames 
        #enemy movement is being calculated individually, which is less efficient, but is needed if we ever want to split enemy movement
        self.max_left = self.enemy_location.x - self.enemy_range
        self.max_right = self.enemy_location.x + self.enemy_range  

    enemy_range = 200
    enemy_move_speed = 2.5
    enemy_size = 15
    enemy_invulnerability_frames = 0
    move_direction = "left"

    def enemy_move(self):
        if self.move_direction == "left":
            #if we hit the max movement distance, start moving the other way
            if self.enemy_location.x == self.max_left:
                self.move_direction = "right"
            #if moving over puts the enemy outside of their range, round to the max range
            elif self.enemy_location.x + self.enemy_move_speed < self.max_left:
                self.enemy_location.x = self.max_left
            #move normally
            else:
                self.enemy_location.x -= self.enemy_move_speed
        elif self.move_direction == "right":
            #same logic as above, but for moving right
            if self.enemy_location.x == self.max_right:
                self.move_direction = "left"
            elif self.enemy_location.x + self.enemy_move_speed > self.max_right:
                self.enemy_location.x = self.max_right
            else:
                self.enemy_location.x += self.enemy_move_speed


    def enemy_die(self):
        print("Enemy dead")


for position in enemy_locations:
    enemy_holder = Enemy(enemy_location = position)
    # enemy_holder.enemy_location = position
    enemies.append(enemy_holder)

player = Player()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and (player.player_shot_cooldown_frames == 0):
                # shoot(player_pos + pygame.Vector2(0, -25), screen)
                # player_health_value -= 1   
                new_bullet = pygame.Rect((player.player_pos + pygame.Vector2(0, -50)), (3, 10))
                bullets.append(new_bullet)
                player.player_shot_cooldown_frames = 20

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    #this could be tied to the player object
    player.player_rect = pygame.draw.circle(screen, player.player_health_colors[player.player_health_value], player.player_pos, player.player_size)
    # player_health_indicator = pygame.draw.circle(screen, health_colors[player_health_value], player_health_indicator_position, 25)

    #AI help to render bullets
    for bullet in bullets:
        bullet.y -= bullet_move_speed
        pygame.draw.rect(screen, "white", bullet) #bullets go forever, which could eat memory

        if bullet.bottom < 0:
            bullets.remove(bullet)

    for enemy_bullet in enemy_bullets:
        enemy_bullet.y += bullet_move_speed
        pygame.draw.rect(screen, "blue", enemy_bullet)

        if enemy_bullet.bottom > 720:
            enemy_bullets.remove(enemy_bullet)

    #render enemies (according to AI, it's better to use a Slice of the list to iterate over a copy)
    for enemy in enemies.copy():
        enemy.enemy_rect = pygame.draw.circle(screen, "blue", enemy.enemy_location, 30)
        if enemy.enemy_invulnerability_frames > 0:
            enemy.enemy_invulnerability_frames -= 1
        #A bullet is just a rectangle, so I can take the enemy rect and compare it with the list of bullets to see if they intersect
        #This method assumes bullets will never collide (technically, they can if someone hit the spacebar fast enough)
        collided_bullet = enemy.enemy_rect.collideobjects(bullets)
        if collided_bullet:
            if (enemy.enemy_invulnerability_frames == 0): #if we use 1 check, the bullet does not get removed
                enemy.enemy_health -= 1
            bullets.remove(collided_bullet)

            if enemy.enemy_health == 0:
                # enemy.enemy_die()
                #python lets you remove a value from a list by using that value
                enemies.remove(enemy)
            enemy.enemy_invulnerability_frames = 60

        if enemy.enemy_shot_cooldown_frames < 1:#shoot, then reset cooldown
            new_enemy_bullet = pygame.Rect((enemy.enemy_location + pygame.Vector2(0, 50)), (3, 10))
            enemy_bullets.append(new_enemy_bullet)
            
            enemy.enemy_shot_cooldown_frames = random.randrange(60, 180)

        enemy.enemy_shot_cooldown_frames -= 1
        enemy.enemy_move()

    if player.player_invulnerability_frames > 0:
        player.player_invulnerability_frames -= 1

    collided_enemy_bullet = player.player_rect.collideobjects(enemy_bullets)
    if collided_enemy_bullet:
        if(player.player_invulnerability_frames == 0):
            player.player_health_value -= 1
            player.player_invulnerability_frames = 120
        enemy_bullets.remove(collided_enemy_bullet)

    if(player.player_shot_cooldown_frames > 0):
        player.player_shot_cooldown_frames -= 1

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and player.player_pos.x > 0:
        player.player_pos.x -= 300 * dt
    if keys[pygame.K_d] and player.player_pos.x < 1280:
        player.player_pos.x += 300 * dt
    if player.player_health_value == 0:
        running = False

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()