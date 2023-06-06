import os
os.system('pip install pygame')
import pygame
import csv
import codecs
import re
import copy
import sys
pygame.init()
window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption('Story')
window.fill((0,0,0))
keylist = {pygame.K_a: 0, pygame.K_b: 1, pygame.K_c: 2, pygame.K_d: 3}
nowpic = 1
Anx = 0
Avo = 0
Dep = 0
Hel = 0
font1 = pygame.font.SysFont('timesnewroman',36)
#storyline
storyline = []
storyline.append({})
with codecs.open('./story.csv', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f, skipinitialspace=True):
        row['JumptoNum'] = row['JumptoNum'].split('/')
        row['RestrainType'] = row['RestrainType'].split('/')
        row['RestrainNum'] = row['RestrainNum'].split('/')
        row['AddNum'] = row['AddNum'].split('/')
        storyline.append(row)
'''
picnum = 51
piclist = [{}]
for i in range(1, picnum+1):
    piclist.append(pygame.image.load('./img/'+str(i)+'.jpg'))
'''
def equals(x,y,z):
    if y==0:
        return True
    elif y==1:
        return x>z
    else:
        return x<z
def compare(val,s1,s2):
    s1 = s1.split('&')
    s2 = s2.split('&')
    res = True
    for i in range(4):
        res = res and equals(val[i], int(s1[i]), int(s2[i]))
    return res
pics = 0
ppl = []
while True:
    if nowpic == -1:
        continue
    text1 = font1.render('Anxiety  '+str(Anx), True, (0,0,0))
    text2 = font1.render('Avoidance  '+str(Avo), True, (0,0,0))
    text3 = font1.render('Happiness  '+str(Dep), True, (0,0,0))
    text4 = font1.render('Health  '+str(Hel), True, (0,0,0))
    text5 = font1.render(str(nowpic), True, (0,0,0))
    forma = '.jpg'
    if nowpic>175:
        forma = '.png'
    pics = pygame.image.load('./img/'+str(nowpic)+forma)
    pics = pygame.transform.smoothscale(pics, (1280, 720))
    window.blit(pics, (0,0))
    window.blit(text1, (30,30))
    window.blit(text2, (30,80))
    window.blit(text3, (30,130))
    window.blit(text4, (30,180))
    window.blit(text5, (30,230))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                nowpic = ppl[-1][0]
                Anx = ppl[-1][1]
                Avo = ppl[-1][2]
                Dep = ppl[-1][3]
                Hel = ppl[-1][4]
                ppl.pop()
                break
            if storyline[nowpic]['HasSelection'] == '0':
                if event.key != pygame.K_SPACE:
                    continue
                if int(storyline[nowpic]['SelectionNum']) ==1:
                    ppl.append([nowpic, Anx, Avo, Dep, Hel])
                    nowpic = int(storyline[nowpic]['JumptoNum'][0])
                    if nowpic == 194:
                        Dep = 3
                        Anx -= 1
                        Avo -= 1
                        Hel += 1
                else:
                    for i in range(int(storyline[nowpic]['SelectionNum'])):
                        is_ok = compare([Anx, Avo, Dep, Hel], storyline[nowpic]['RestrainType'][i], storyline[nowpic]['RestrainNum'][i])
                        if is_ok:
                            ppl.append([nowpic, Anx, Avo, Dep, Hel])
                            nowpic = int(storyline[nowpic]['JumptoNum'][i])
                            break
            else:
                if event.key not in keylist.keys():
                    continue
                true_key = keylist[event.key]
                if true_key >= int(storyline[nowpic]['SelectionNum']):
                    continue
                is_ok = compare([Anx, Avo, Dep, Hel], storyline[nowpic]['RestrainType'][true_key], storyline[nowpic]['RestrainNum'][true_key])
                if is_ok:
                    ppl.append([nowpic, Anx, Avo, Dep, Hel])
                    addlist = storyline[nowpic]['AddNum'][true_key].split('&')
                    nowpic = int(storyline[nowpic]['JumptoNum'][true_key])
                    Anx += int(addlist[0])
                    Avo += int(addlist[1])
                    Dep += int(addlist[2])
                    Hel += int(addlist[3])

                    