import pygame
import numpy as np

FPS = 60   # frames per second

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


class Wings():
    def __init__(self, w, h, H, jointangle):
        self.w= w
        self.h= h
        self.X = np.array([[0,0], [w,0], [w,h], [0,h]])

        self.H =H
        self.jointangle= jointangle

        self.Hnew = self.H @ Rmat(self.jointangle) @Tmat(0, -self.h/2)
        self.x, self.y = self.H[0,2], self.H[1,2]

    def draw(self, screen, color):
        pygame.draw.circle(screen, (255,0,0), (self.x,self.y), 8)
        draw(screen, self.X, self.Hnew, color=(0,0,255))

def main():
    pygame.init()

    screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    w, h = 100, 40
    X= np.array([[0,0], [w,0], [w,h], [0,h]])
    position = [WINDOW_WIDTH/3, WINDOW_HEIGHT-50]

    num_joints = 8
    jointangles = [10] * (num_joints+1)
    joint_speed = 3

    gripangle =0
    grip= False

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            for i in range(num_joints+1):
                if pygame.key.get_pressed()[pygame.K_1 + i]:
                    jointangles[i] += joint_speed

            #gripper's action   
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE:
                    grip = not grip
                    if grip == True:
                        gripangle =30
                        print("잡은 위치는",a,b)
                        pygame.draw.circle(screen, (255,182,193), (a,b), radius=5)
                    else:
                        gripangle =0


        pygame.draw.circle(screen, (255,0,0), tuple(position), 8)

        screen.fill( (200, 200, 200) )

        #base rect
        H0 = Tmat(position[0], position[1]) @ Tmat(0, -h)
        draw(screen, X, H0, (0,0,0)) 

        #arms
        arms = []
        H = H0 @ Tmat(w/2,0) @Rmat(-90)
        for i in range(num_joints):
            arms.append(Wings(w, h, H, jointangles[i]))
            H = arms[-1].Hnew @ Tmat(w, 0) @ Tmat(0, h / 2)
        for arm in arms:
            arm.draw(screen, (0, 0, 255))
    

        #hand
        w2, h2 = 50, 10
        smallX= np.array([[0,0], [w2,0], [w2,h2], [0,h2]])
        hand1= Wings(w2, h2, H, jointangles[-1])
        hand1.draw(screen, (0,0,255))

        H5 = hand1.Hnew @ Tmat(w2+h2,0) @Rmat(90) @ Tmat(-(w2-h2)/2,0)
        draw(screen, smallX, H5, (100,100,0))

        H6 = H5 @ Rmat(-90) @ Rmat(gripangle) @ Tmat(0, -h2)
        H7 = H5 @ Tmat(w2,0) @ Rmat(-90) @ Rmat(-gripangle) 
        a,b = (H6 @ Tmat(w2,h2))[0,2], (H6 @ Tmat(w2,h2))[1,2]

        draw(screen, smallX, H6, (100,100,0))
        draw(screen, smallX, H7, (100,100,0))

        pygame.display.flip()
        clock.tick(FPS)
#

if __name__ == "__main__":
    main()