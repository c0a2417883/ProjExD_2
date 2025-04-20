import os
import sys
import pygame as pg
import random
import time
import math


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
    bb_rct.center = random.randint(0,1100), random.randint(0,650)
    vx = 5
    vy = 5
    
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

        def check_bound(re):
            if re.top <= 0 or re.right >= 1100 or re.bottom >= 650 or re.left <= 0:
                return False
            else:
                return True

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
            pg.display.update()
            time.sleep(5)
        
        def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
            """
            サイズの異なる爆弾Surfaceを要素としたリストと加速度リスト
            を返す
            """
            bb_imgs = []
            
            for r in range(1, 11):
                bb_img = pg.Surface((20*r, 20*r))
                pg.draw.circle(bb_img,(255, 0, 0), (10*r, 10*r), 10*r)
                bb_img.set_colorkey((0, 0, 0))
                bb_imgs.append(bb_img)
            bb_accs = [a for a in range(1, 11)]
            return bb_imgs, bb_accs
        
        def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:

            """
            移動量の合計値タプルに対応する向きの画像Surfaceを返す
            """
            koukaton = {(0, 0) :  pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9), 
                        (0, -5) : pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), False, True), 270, 0.9),
                        (+5, -5) : pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), False, True), 225, 0.9),
                        (+5, 0) : pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), False, True), 180, 0.9),
                        (+5, +5) : pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), False, True), 135, 0.9),
                        (0, +5) : pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), False, True), 90, 0.9),
                        (-5, +5) : pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0.9),
                        (-5, 0) : pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
                        (-5, -5) : pg.transform.rotozoom(pg.image.load("fig/3.png"), 315, 0.9)}
            return koukaton[sum_mv]
        
        
        def calc_orientation(org: pg.Rect, dst: pg.Rect,current_xy: tuple[float, float]) -> tuple[float, float]:
            """
            orgから見て，dstがどこにあるかを計算し，方向ベクトルをタプルで返す
            """
            
            bb_x, bb_y = org.center
            kk_x, kk_y = dst.center
            dx = kk_x - bb_x
            dy = kk_y - bb_y
            norm = math.sqrt(dx**2 + dy**2)
            if norm < 300:
                last_d = (dx / norm , dy / norm )
            else:
                dx = dx / norm
                dy = dy / norm
                now_bb = (dx, dy)
                dx = dx * math.sqrt(50)
                dy = dy * math.sqrt(50)
                last_d = (dx, dy)

            return last_d
        
        vx, vy = calc_orientation(bb_rct, kk_rct, (vx, vy))

        kk_img = get_kk_img((0, 0))
        kk_img = get_kk_img(tuple(sum_mv))

        if check_bound(bb_rct) == False:
            if bb_rct.bottom >= 650 or bb_rct.top <= 0:
                vy = -vy
            if bb_rct.right >= 1100 or bb_rct.left <= 0:
                vx = -vx
        
        bb_imgs, bb_accs = init_bb_imgs()
        # tmrを500で割った商と9を比較し，小さい方を選択
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]

        bb_rct.move_ip(avx, avy)  
        kk_rct.move_ip(sum_mv)

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        
        if check_bound(kk_rct) == False:
            kk_rct.center = kk_rct2
        
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
