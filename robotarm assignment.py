import pygame
import numpy as np

FPS = 60 
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

def draw(screen, P, H, color=(100,200,200)):
    R = H[:2,:2]
    T = H[:2, 2]
    Ptransformed = P @ R.T + T
    pygame.draw.polygon(screen, color=color, points=Ptransformed, width=3)
    return

def Rmat(degree):
    rad = np.deg2rad(degree) 
    c = np.cos(rad)
    s = np.sin(rad)
    R = np.array([ [c, -s, 0],
                   [s,  c, 0], [0,0,1]])
    return R

def Tmat(tx, ty):
    Translation = np.array( [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])
    return Translation

def main():
    pygame.init()

    screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    w, h = 150, 40
    w2, h2 = w-100, h-30
    X= np.array([[0,0], [w,0], [w,h], [0,h]])
    smallX= np.array([[0,0], [w2,0], [w2,h2], [0,h2]])

    position = [WINDOW_WIDTH/2, WINDOW_HEIGHT-100]
    jointangle1= 10
    jointangle2= 50
    jointangle3= 3
    jointangle4=0

    gripangle=0
    grip = False

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_1:
                    jointangle1 +=2
                if event.key == pygame.K_2:
                    jointangle2 +=2
                if event.key == pygame.K_3:
                    jointangle3 +=2
                if event.key == pygame.K_4:
                    jointangle4 +=3

                #gripper's action    
                if event.key == pygame.K_SPACE:
                    if grip == True:
                        gripangle =15
                    else:
                        gripangle =0
                    grip = not grip

        
        pygame.draw.circle(screen, (255,0,0), tuple(position), 8)

        screen.fill( (200, 200, 200) )

        H0 = Tmat(position[0], position[1]) @ Tmat(0, -h)
        draw(screen, X, H0, (0,0,0)) #base rect

        #arm1
        H1 = H0 @ Tmat(w/2,0)
        x,y = H1[0,2], H1[1,2] #joint position
        H11= H1 @ Rmat(-90) @ Tmat(0,-h/2)
        pygame.draw.circle(screen, (255,0,0), (x,y), 8) #joint position
        H12= H11 @Tmat(0, h/2) @ Rmat(jointangle1) @ Tmat(0, -h/2)
        draw(screen, X, H12, (100,100,0))

        #arm2
        H2 = H12 @ Tmat(w,0) @Tmat(0, h/2)
        x,y = H2[0,2], H2[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), 8)
        H21 = H2@ Rmat(jointangle2) @ Tmat(0, -h/2)
        draw(screen, X, H21, (100,100,0))

        #arm3
        H3 = H21 @ Tmat(w,0) @ Tmat(0, h/2)
        x,y = H3[0,2], H3[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), 8)
        H31 = H3@ Rmat(jointangle3) @ Tmat(0, -h/2)
        H32= H31 @Tmat(0, h/2) @ Rmat(jointangle3) @ Tmat(0, -h/2)
        draw(screen, X, H32, (100,100,0))
        
        #drawing hands
        H4 = H32 @ Tmat(w,0) @ Tmat(0, h/2)
        x,y = H4[0,2], H4[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), 8)
        H41 = H4@ Rmat(jointangle4) @ Tmat(0, -h2/2)
        draw(screen, smallX, H41, (100,100,0))

        H5 = H41 @ Tmat(w2+h2,0) @Rmat(90) @ Tmat(-(w2-h2)/2,0)
        x,y = H5[0,2], H5[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), 8)
        draw(screen, smallX, H5, (100,100,0))

        H6 = H5@  Rmat(-90) @ Rmat(gripangle) 
        H7 = H5 @ Rmat(-90) @ Tmat(0, w2-h2)@ Rmat(-gripangle) 

        draw(screen, smallX, H6, (100,100,0))
        draw(screen, smallX, H7, (100,100,0))
            

        pygame.display.flip()
        clock.tick(FPS)
#

if __name__ == "__main__":
    main()