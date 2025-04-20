import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    DELTA = {pg.K_UP : (0, -5), pg.K_DOWN : (0, +5),pg.K_LEFT : (-5, 0),pg.K_RIGHT : (+5, 0)}
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(100,300), random.randint(100,300)
    vx = 0
    vy = 0
    vx += 5
    vy += 5
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        
        
        kk_rct2 = kk_rct.center
        for key, delta in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += delta[0]
                sum_mv[1] += delta[1]

        kk_rct.move_ip(sum_mv)
        
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)

        def check_bound(re):
            if re.top <= 0 or re.right >= 1100 or re.bottom >= 650 or re.left <= 0:
                return False
            else:
                return True
        if check_bound(kk_rct) == False:
            kk_rct.center = kk_rct2
        if check_bound(bb_rct) == False:
            if bb_rct.bottom >= 650 or bb_rct.top <= 0:
                vy = -vy
            if bb_rct.right >= 1100 or bb_rct.left <= 0:
                vx = -vx

        bb_rct.move_ip(vx, vy)

        def gameover(screen: pg.Surface) -> None:
            """
            ゲームオーバー時に，半透明の黒い画面上に「Game Over」と表
            示し，泣いているこうかとん画像を貼り付ける関数
            """
            gameover_sur = pg.Surface((1100, 650))
            font = pg.font.Font(None, 80)
            cry = pg.image.load("fig/8.png") 
            cry2 = pg.image.load("fig/8.png") 
            gameover_txt = font.render("Game Over",True,(255, 255, 255))
            gameover_sur.set_alpha(130)
            pg.draw.rect(gameover_sur, (0, 0, 0), pg.Rect(0, 0, 1100, 650))
            screen.blit(gameover_sur, [0, 0])
            screen.blit(gameover_txt, [400, 300])
            screen.blit(cry, [340, 290])
            screen.blit(cry2, [723, 290])
            
            

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            time.sleep(5)
            pg.display.update()
            return
        


        pg.display.update()
        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
