# Example file showing a circle moving on screen
import pygame


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
#origin is in the top left
player_pos = pygame.Vector2(640,680)
player_health_value = 3
health_colors = [(0,0,0), (255, 200, 200), (255, 100, 100), (255, 0, 0)]
player_health_indicator_position = pygame.Vector2(50, 50)

bullets = [] #gemini suggestion to improve rendering
bullet_move_speed = 10

enemies = []
enemy_hitboxes = []
enemy_locations = [pygame.Vector2(340, 100), pygame.Vector2(440,100), pygame.Vector2(540,100), pygame.Vector2(640,100), pygame.Vector2(740,100), pygame.Vector2(840,100), pygame.Vector2(940, 100)]

class Enemy:
    #instance parameter which is unique to each object
    def __init__(self, enemy_location = pygame.Vector2(340, 100), enemy_health = 2, enemy_rect = None):
        # self.enemy_range = enemy_range
        # self.enemy_size = enemy_size
        self.enemy_location = enemy_location
        self.enemy_health = enemy_health
        self.enemy_rect = enemy_rect

    enemy_range = 200
    enemy_size = 15

    def enemy_die(self):
        print("Enemy dead")


for position in enemy_locations:
    enemy_holder = Enemy(enemy_location = position)
    # enemy_holder.enemy_location = position
    enemies.append(enemy_holder)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # shoot(player_pos + pygame.Vector2(0, -25), screen)
                # player_health_value -= 1   
                new_bullet = pygame.Rect((player_pos + pygame.Vector2(0, -50)), (3, 10))
                bullets.append(new_bullet)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "green4", player_pos, 40)
    player_health_indicator = pygame.draw.circle(screen, health_colors[player_health_value], player_health_indicator_position, 25)

    #AI help to render bullets
    for bullet in bullets:
        bullet.y -= bullet_move_speed
        pygame.draw.rect(screen, "white", bullet) #bullets go forever, which could eat memory

        
        if bullet.bottom < 0:
            bullets.remove(bullet)

    #render enemies (according to AI, it's better to use a Slice of the list to iterate over a copy)
    #BUG the same bullet will hit the enemy multiple times, the bullet 
    for enemy in enemies.copy():
        enemy.enemy_rect = pygame.draw.circle(screen, "blue", enemy.enemy_location, 30)
        #A bullet is just a rectangle, so I can take the enemy rect and compare it with the list of bullets to see if they intersect
        #This method assumes bullets will never collide (technically, they can if someone hit the spacebar fast enough)
        if enemy.enemy_rect.collideobjects(bullets):
            enemy.enemy_health -= 1
            if enemy.enemy_health == 0:
                # enemy.enemy_die()
                #python lets you remove a value from a list by using that value
                enemies.remove(enemy)



    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and player_pos.x > 0:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d] and player_pos.x < 1280:
        player_pos.x += 300 * dt
    if player_health_value == 0:
        running = False

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()