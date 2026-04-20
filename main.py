import random
import time
import pygame
import songinfo
import pathlib

pygame.init()
pygame.font.init()

WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720

BACK_BUTTON_TIME_THRESHOLD = 5
COVER_SIZE = 256
WINDOW_BORDER_MARGIN = 30
NORMAL_MARGIN = 20
UI_MARGIN = 15
COVER_RIGHT = WINDOW_BORDER_MARGIN + COVER_SIZE + NORMAL_MARGIN * 2
TITLE_SIZE = 60
QUEUE_TITLE_SIZE = 40
TEXT_SIZE = 20
TITLE_BOX_MAX_SIZE = WINDOW_WIDTH - COVER_RIGHT - NORMAL_MARGIN - WINDOW_BORDER_MARGIN + NORMAL_MARGIN * 3

songs: list[str] = [str(path).split(".wav")[0].split("songs\\")[1] for path in pathlib.Path("songs").rglob("*.wav")]
for song in songs:
    if song not in songinfo.backgrounds:
        songinfo.backgrounds[song] = (122, 122, 122)
random.shuffle(songs)
next_songs = [*songs]
random.shuffle(next_songs)
songs = [*songs, *next_songs]

song_index = 0
song_playing = pygame.mixer.Sound("startup.wav")
song_playing.play()
song = songs[song_index]
last = "none"

PLAYING_FONT = pygame.font.SysFont("arial", TITLE_SIZE)
QUEUED_FONT = pygame.font.SysFont("arial", TEXT_SIZE)
QUEUED_TITLE_FONT = pygame.font.SysFont("arial", QUEUE_TITLE_SIZE)
TIMER_FONT = pygame.font.SysFont("arial", TEXT_SIZE)
QUEUED_TITLE = QUEUED_TITLE_FONT.render("Up Next", True, (15, 15, 15) if sum(songinfo.backgrounds[song]) / 3 > 122.5 else (240, 240, 240))
QUEUE_WIDTH = max(QUEUED_TITLE.get_width(), *[QUEUED_FONT.render(s, True, (0, 0, 0)).get_width() for s in songs])

song_playing = pygame.mixer.Sound(f"songs/{song}.wav")
text_color = (15, 15, 15) if sum(songinfo.backgrounds[song]) / 3 > 122.5 else (240, 240, 240)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
volume = .7
song_playing.set_volume(volume)
pygame.display.set_caption("Emlore's Time Machine Music")

clock = pygame.time.Clock()

r, g, b = songinfo.backgrounds[last]
red_shift, green_shift, blue_shift = ((c1 - c2) / 500 for c1, c2 in zip(songinfo.backgrounds[song], songinfo.backgrounds[last]))
song_text = PLAYING_FONT.render(song, True, (15, 15, 15) if sum(songinfo.backgrounds[song]) / 3 > 122.5 else (240, 240, 240))
start_time = 0
time_paused = 0

try:
    song_image = pygame.image.load(f"images/{song}.png").convert_alpha()
except FileNotFoundError:
    song_image = pygame.image.load("images/Unknown.png").convert()

def update_screen_size():
    global WINDOW_WIDTH, WINDOW_HEIGHT
    WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_window_size()

def change_color():
    global r, g, b
    if r != songinfo.backgrounds[song][0]:
        r += red_shift
        r = min(r, songinfo.backgrounds[song][0]) if red_shift > 0 else max(r, songinfo.backgrounds[song][0])
    if g != songinfo.backgrounds[song][1]:
        g += green_shift
        g = min(g, songinfo.backgrounds[song][1]) if green_shift > 0 else max(g, songinfo.backgrounds[song][1])
    if b != songinfo.backgrounds[song][2]:
        b += blue_shift
        b = min(b, songinfo.backgrounds[song][2]) if blue_shift > 0 else max(b, songinfo.backgrounds[song][2])

scroll = 0
paused = True

def load_playlist(playlist: str):
    pass

def add_song(song: str):
    pass

def display(finished: bool = False, scrolling: bool = True):
    global scroll
    update_screen_size()
    screen.fill((int(r), int(g), int(b)))
    color = (255, 255, 255, 51)

    #DRAW TITLE AND IMAGE
    title_box = pygame.Surface((min(song_text.get_width() + NORMAL_MARGIN * 4, TITLE_BOX_MAX_SIZE), TITLE_SIZE + NORMAL_MARGIN * 2), pygame.SRCALPHA)
    pygame.draw.rect(title_box, color, title_box.get_rect(), border_radius=20)
    screen.blit(title_box, (COVER_RIGHT - NORMAL_MARGIN * 2, WINDOW_BORDER_MARGIN))
    if scrolling:
        scroll += 1
        if scroll in range(0, 60):
            screen.blit(song_text, (COVER_RIGHT + NORMAL_MARGIN, WINDOW_BORDER_MARGIN + NORMAL_MARGIN))
        elif scroll in range(60, 180):
            screen.blit(song_text, (COVER_RIGHT + NORMAL_MARGIN - max(0, (scroll - 60) / 120 * (song_text.get_width() - 684)), WINDOW_BORDER_MARGIN + NORMAL_MARGIN))
        elif scroll in range(180, 240):
            screen.blit(song_text, (COVER_RIGHT + NORMAL_MARGIN - max(0, (song_text.get_width() - 684)), WINDOW_BORDER_MARGIN + NORMAL_MARGIN))
        elif scroll in range(240, 360):
            screen.blit(song_text, (COVER_RIGHT + NORMAL_MARGIN - max(0, (360 - scroll) / 120 * (song_text.get_width() - 684)), WINDOW_BORDER_MARGIN + NORMAL_MARGIN))
        else:
            scroll = 0
            screen.blit(song_text, (COVER_RIGHT + NORMAL_MARGIN, WINDOW_BORDER_MARGIN + NORMAL_MARGIN))
    else:
        screen.blit(song_text, (COVER_RIGHT + NORMAL_MARGIN, WINDOW_BORDER_MARGIN + NORMAL_MARGIN))
        scroll = 0

    pygame.draw.rect(screen, (0, 0, 0), (WINDOW_BORDER_MARGIN, WINDOW_BORDER_MARGIN, COVER_SIZE + NORMAL_MARGIN * 2, COVER_SIZE + NORMAL_MARGIN * 2), border_radius=20)
    screen.blit(song_image, (50, 50))

    pygame.draw.rect(screen, (int(r), int(g), int(b)), (WINDOW_WIDTH - WINDOW_BORDER_MARGIN, WINDOW_BORDER_MARGIN + NORMAL_MARGIN, WINDOW_BORDER_MARGIN, TITLE_SIZE))
    pygame.draw.rect(screen, (int(r), int(g), int(b)), (0, WINDOW_BORDER_MARGIN + NORMAL_MARGIN, WINDOW_BORDER_MARGIN, TITLE_SIZE))
    
    #DRAW QUEUE
    queue_box = pygame.Surface((QUEUE_WIDTH + 100, WINDOW_HEIGHT - 140), pygame.SRCALPHA)
    pygame.draw.rect(queue_box, color, queue_box.get_rect(), border_radius=20)
    screen.blit(queue_box, (WINDOW_WIDTH - QUEUE_WIDTH - NORMAL_MARGIN * 4, 160))

    queue_title_box = pygame.Surface((1015 - QUEUE_WIDTH + 30, 70), pygame.SRCALPHA)
    pygame.draw.rect(queue_title_box, color, queue_title_box.get_rect(), border_radius=15)
    screen.blit(queue_title_box, (WINDOW_WIDTH - 65 - QUEUE_WIDTH, 175))

    screen.blit(QUEUED_TITLE, (WINDOW_WIDTH - 35 - QUEUED_TITLE.get_width(), 190))
    
    farthest_song = (WINDOW_HEIGHT - 220) // 50
    for index, s in enumerate(songs[song_index + 1:song_index + farthest_song]):
        queued_text = QUEUED_FONT.render(s, True, (15, 15, 15) if sum(songinfo.backgrounds[song]) / 3 > 122.5 else (240, 240, 240))
        screen.blit(queued_text, (WINDOW_WIDTH - 35 - queued_text.get_width(), 220 + 50 * (songs.index(s, song_index + 1 + index) - song_index)))

    #DRAW PROGRESS BAR
    pause_time = (time.time() - time_paused) if paused else 0
    total_time = TIMER_FONT.render(f"{int(song_playing.get_length()) // 60}:{"0" if int(song_playing.get_length()) % 60 < 10 else ""}{int(song_playing.get_length()) % 60}", True, text_color)
    current_time = TIMER_FONT.render("0:00" if finished else f"{int(time.time() - start_time - pause_time) // 60}:{"0" if int(time.time() - start_time - pause_time) % 60 < 10 else ""}{int(time.time() - start_time - pause_time) % 60}", True, text_color)

    pygame.draw.line(screen, text_color, (346, 189.5), (WINDOW_WIDTH - 100 - QUEUE_WIDTH, 189.5), 4)
    pygame.draw.circle(screen, text_color, (346, 190), 7)
    pygame.draw.circle(screen, text_color, (WINDOW_WIDTH - 100 - QUEUE_WIDTH, 190), 7)

    bar_color = (205, 205, 205) if text_color == (240, 240, 240) else (50, 50, 50)
    pygame.draw.circle(screen, bar_color, (346 + (WINDOW_WIDTH - 100 - QUEUE_WIDTH - 346) * ((time.time() - start_time - pause_time) / song_playing.get_length()) if not finished else 346, 190), 7)

    screen.blit(total_time, (WINDOW_WIDTH - 95 - QUEUE_WIDTH - total_time.get_width(), 200))
    screen.blit(current_time, (341, 200))

    #DRAW PAUSE/PLAY, SKIP, PREVIOUS
    if paused:
        pygame.draw.polygon(screen, text_color, ((421, 240), (391, 225), (391, 255)))
    else:
        pygame.draw.rect(screen, text_color, (396, 225, 7, 30))
        pygame.draw.rect(screen, text_color, (406, 225, 7, 30))
    
    pygame.draw.polygon(screen, text_color, ((346, 240), (361, 225), (361, 255)))
    pygame.draw.polygon(screen, text_color, ((361, 240), (376, 225), (376, 255)))

    pygame.draw.polygon(screen, text_color, ((466, 240), (451, 225), (451, 255)))
    pygame.draw.polygon(screen, text_color, ((451, 240), (436, 225), (436, 255)))

    #DRAW VOLUME CONTROL
    song_playing.set_volume(volume)
    
    pygame.draw.rect(screen, bar_color, (481, 232, 499 - QUEUE_WIDTH, 16))
    pygame.draw.rect(screen, text_color, (481, 232, (min((499 - QUEUE_WIDTH), (499 - QUEUE_WIDTH) * volume)), 16))

    pygame.draw.rect(screen, (122, 122, 122), (485, 238, 8, 4))

    pygame.draw.rect(screen, (122, 122, 122), (969 - QUEUE_WIDTH, 235, 4, 10))
    pygame.draw.rect(screen, (122, 122, 122), (966 - QUEUE_WIDTH, 238, 10, 4))

    pygame.display.update()

counter = 0
for _ in range(0, 600):
    counter += 1
    if counter < 600:
        change_color()
        display(finished=True, scrolling=False)
        continue
    screen.fill(songinfo.backgrounds[song])
    song_playing.play()
    start_time = time.time()
    pygame.mixer.pause()
    time_paused = time.time()
    counter = 0
    pygame.display.set_caption(f"Emlore's Time Machine Music: {song}")
    pygame.display.update()
    clock.tick(60)

running = True
counter = 0

def pause_or_play():
    global paused, time_paused, start_time
    paused = not paused
    if paused:
        pygame.mixer.pause()
        time_paused = time.time()
    else:
        pygame.mixer.unpause()
        start_time += time.time() - time_paused
        time_paused = 0

def previous():
    global song_index
    song_index -= 1
    if (time.time() - start_time) < BACK_BUTTON_TIME_THRESHOLD:
        song_index -= 1 
    pygame.mixer.stop()

def next_song():
    pygame.mixer.stop()

def vol_up():
    global volume
    if volume < 1:
        volume += .1

def vol_down():
    global volume
    if volume > 0:
        volume -= .1

regions = [
    (
        (
            (391, 421),
            (225, 255)
        ),
        pause_or_play
    ),
    (
        (
            (346, 376),
            (225, 255)
        ),
        previous
    ),
    (
        (
            (436, 466),
            (225, 255)
        ),
        next_song
    ),
    (
        (
            (481, 497),
            (232, 248)
        ),
        vol_down
    ),
    (
        (
            (964 - QUEUE_WIDTH, 980 - QUEUE_WIDTH),
            (232, 248)
        ),
        vol_up
    )
]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause_or_play()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for region, function in regions:
                if region[0][0] <= event.pos[0] <= region[0][1] and region[1][0] <= event.pos[1] <= region[1][1]:
                    function()
    if not pygame.mixer.get_busy() and not paused:
        counter += 1
        if counter == 1:
            song_index += 1
            if len(songs) / 2 == song_index:
                next_songs = songs[song_index:]
                songs = songs[song_index:]
                song_index = 0
                random.shuffle(next_songs)
                songs = [*songs, *next_songs]
            last = song
            song = songs[song_index]
            song_playing = pygame.mixer.Sound(f"songs/{song}.wav")
            r, g, b = songinfo.backgrounds[last]
            red_shift, green_shift, blue_shift = ((c1 - c2) / 500 for c1, c2 in zip(songinfo.backgrounds[song], songinfo.backgrounds[last]))
            text_color = (15, 15, 15) if sum(songinfo.backgrounds[song]) / 3 > 122.5 else (240, 240, 240)
            song_text = PLAYING_FONT.render(song, True, text_color)
            try:
                song_image = pygame.image.load(f"images/{song}.png").convert_alpha()
            except FileNotFoundError:
                song_image = pygame.image.load("images/Unknown.png").convert()
            continue
        if counter < 600:
            change_color()
            display(finished=True, scrolling=False)
            continue
        screen.fill(songinfo.backgrounds[song])
        song_playing.play()
        start_time = time.time()
        counter = 0
        pygame.display.set_caption(f"Emlore's Time Machine Music: {song}")
    display()
    clock.tick(60)
    
pygame.quit()