import pygame
import sys
import numpy as np

# 충돌 함수 정의

# 원끼리 부딫히는 경우
def collision_circle(c, p, vxy):
    dl2 = np.array(c) - np.array(p)
    dl2mag = np.sqrt(dl2[0]**2 + dl2[1]**2)
    rl2 = BALL_RADIUS + OBSTACLE_B_R
    if dl2mag < rl2: # 만약 원끼리 부딫힐 경우
        collision_direction = dl2 / dl2mag # 부딫히는 방향 값을 추출해내자.
        vxymag = np.sqrt(vxy[0]**2 + vxy[1]**2) # 그리고 기존 vxy의 mag를 추출해내자.
        vxy  = collision_direction * vxymag # 방향 값에다가 vxy의 mag를 곱해주자.
        # 위와 같은 식을 적용하면 부딫히는 원에 정반대 방향으로 공이 움직이게 된다. 
        return True, vxy
    else:
        return False

# 원과 사각형이 부딫히는 경우
def collision_circle_rect(circle_x, circle_y, rect):
    closest_x = max(rect.left, min(circle_x, rect.right)) # 먼저 원과 가장 가까운 쪽의 사각형의 x좌표를 구한다.
    closest_y = max(rect.top, min(circle_y, rect.bottom)) # 그리고 원과 가장 가까운 쪽의 사각형의 y좌표를 구한다.
    distance_x = circle_x - closest_x # 거리 구한다.
    distance_y = circle_y - closest_y
    is_colliding = (distance_x ** 2 + distance_y ** 2) < (10 ** 2) # 만약 그 거리가 원의 반지름보타 작다면 이제 충돌인것.

    if is_colliding: # 충돌 경우를 나눈다. 
        if closest_x == rect.left:
            return "left"
        elif closest_x == rect.right:
            return "right"
        elif closest_y == rect.top:
            return "top"
        else:  # closest_y == rect.bottom
            return "bottom"
    else:
        return None
    
# 원과 삼각형이 부딫히는 경우
def is_colliding_circle_triangle(circle_x, circle_y, triangle_points, vxy): 
    # 삼각형이 원과 부딫히는지 여부를 알기 위해서,
    # 삼각형의 각 변의 벡터를 구한 다음에 축에 프로젝션 시킴으로써
    # 삼각형의 범위를 구한다.
    # 그리고 삼각형의 범위 안에 원이 존재하는지를 비교함으로써 삼각형이 원 안에 있는지를 판단한다.
    for i in range(3):
        # 삼각형의 한 변과 원을 비교하기 위해, 일단 3개의 변 중 하나를 다룬다.
        point1 = triangle_points[i]
        point2 = triangle_points[(i + 1) % 3]

        # 나중에 프로젝션을 통해 원이 삼각형 안에 있는지 구해 줄 것인데, 그것을 하기 위해서는 먼저 
        # 몇몇 개의 벡터가 필요하다. 
        vec = [circle_x - point1[0], circle_y - point1[1]]

        edge_vec = np.array([point2[0] - point1[0], point2[1] - point1[1]])

        proj_len = (vec[0] * edge_vec[0] + vec[1] * edge_vec[1]) / (edge_vec[0]**2 + edge_vec[1]**2)
        proj = [proj_len * edge_vec[0], proj_len * edge_vec[1]]

        if 0 <= proj_len <= 1:
            closest_point = [point1[0] + proj[0], point1[1] + proj[1]]
        else:
            if proj_len < 0:
                closest_point = point1
            else:
                closest_point = point2

        dist = ((circle_x - closest_point[0])**2 + (circle_y - closest_point[1])**2)**0.5
        if dist <= BALL_RADIUS:
            normal = np.array(closest_point) - np.array([circle_x, circle_y])
            normal /= np.linalg.norm(normal)
            vxy = vxy - 2 * np.dot(vxy, normal) * normal
            return True, vxy

    return False

pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

sound_im = pygame.mixer.Sound("C:\\Users\\eoeld\\Desktop\\impressive.wav")
sound_co = pygame.mixer.Sound("C:\\Users\\eoeld\\Desktop\\collide.wav")
sound_ov = pygame.mixer.Sound("C:\\Users\\eoeld\\Desktop\\gameover.wav")

score = 0

background_screen = pygame.image.load("C:\\Users\\eoeld\\Desktop\\1.png")
background_screen = pygame.transform.scale(background_screen, (WIDTH, HEIGHT))

# 변수들
BALL_RADIUS = 10.

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY  = (200,200,200)
YELLOW = [255,255,0]

# 장애물들
OBSTACLE_B_R = 30. # 장애물 원의 반지름
OBSTACLE_R_WH = 60
Interval_R = OBSTACLE_R_WH + 50

# 삼각형 꼭짓점 좌표
points_1 = [(70, 500), (70, 600), (130, 600)]
points_2 = [(WIDTH - 70, 500), (WIDTH - 70, 600), (WIDTH - 130, 600)]

points = [points_1, points_2]

#원
circle_1 = [WIDTH / 2 + 100, HEIGHT /2 + 100]
circle_2 = [WIDTH / 2, HEIGHT /2 + 150]
circle_3 = [WIDTH / 2 - 100, HEIGHT /2 + 100]

#사각형
ob_rect_1 = pygame.Rect(WIDTH / 2 - Interval_R * 2, HEIGHT / 2 - 200, OBSTACLE_R_WH, OBSTACLE_R_WH)
ob_rect_2 = pygame.Rect(WIDTH / 2 - Interval_R, HEIGHT / 2 - 200, OBSTACLE_R_WH, OBSTACLE_R_WH)
ob_rect_3 = pygame.Rect(WIDTH / 2 , HEIGHT / 2 - 200, OBSTACLE_R_WH, OBSTACLE_R_WH)
ob_rect_4 = pygame.Rect(WIDTH / 2 + Interval_R, HEIGHT / 2 - 200, OBSTACLE_R_WH, OBSTACLE_R_WH)
ob_rect_5 = pygame.Rect(WIDTH / 2 + Interval_R * 2, HEIGHT / 2 - 200, OBSTACLE_R_WH, OBSTACLE_R_WH)

# 전체 리스트
obstacles = [circle_1, circle_2, circle_3, ob_rect_1, ob_rect_2, ob_rect_3, ob_rect_4, ob_rect_5]

# 공 정의하기
ball_pos = np.array([20., 20.])
axy = np.array([0.,0.1])
vxy = np.array([4.,0.])

# 조종 가능한 도형 세팅
paddle_point_1 = [[WIDTH /2 - 130, HEIGHT - 100], [WIDTH/2 - 130, HEIGHT - 80], [WIDTH/2 - 50, HEIGHT -50]]  # 세번쨰 좌표가 모서리
paddle_point_2 = [[WIDTH /2 + 130, HEIGHT - 100], [WIDTH/2 + 130, HEIGHT - 80], [WIDTH/2 + 50, HEIGHT -50]]  # 세번쨰 좌표가 모서리
paddle_move = False

# 나머지 배경용
background_3 = pygame.Rect(40, HEIGHT - 100, 130 , 50)
background_4 = pygame.Rect(WIDTH-170, HEIGHT - 100, 130 , 50)
background_2 = pygame.Rect(0, 50, 180 , 60)
background_5 = [[40, HEIGHT - 150], [40, HEIGHT - 100], [WIDTH/2 - 130, HEIGHT - 100], ]
background_6 = [[WIDTH - 40, HEIGHT - 150], [WIDTH - 40, HEIGHT - 100], [WIDTH/2 + 130, HEIGHT - 100], ]
background = [background_2, background_3, background_4, background_5 ,background_6]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    font = pygame.font.Font(None, 36)
    text = font.render('score is ' + str(score), True, (0,0,0))
    if score > 5000 : 
        sound_im.play()
        

    # 공 움직임 업데이트
    vxy += axy    
    ball_pos += vxy
    
    # 조종가능도형 움직임.
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if paddle_point_1[2][1] < HEIGHT - 130 :
            paddle_move = False
            pass
        else :
            paddle_point_1[2][1] -= 8.
            paddle_move = True
    else :
        paddle_point_1 = [[WIDTH /2 - 130, HEIGHT - 100], [WIDTH/2 - 130, HEIGHT - 80], [WIDTH/2 - 50, HEIGHT -50]]  # 세번쨰 좌표가 모서리
        paddle_move = False

    if keys[pygame.K_RIGHT]:        
        if paddle_point_2[2][1] < HEIGHT - 130 :
            paddle_move = False
            pass
        else :
            paddle_point_2[2][1] -= 8.
            paddle_move = True
    else :
        paddle_point_2 = [[WIDTH /2 + 130, HEIGHT - 100], [WIDTH/2 + 130, HEIGHT - 80], [WIDTH/2 + 50, HEIGHT -50]]  # 세번쨰 좌표가 모서리
        paddle_move = False

            
    # #사이로 빠져나가면 이제 끝.
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        sound_ov.play()
        print('gameover')
        pygame.quit()
        sys.exit()

    # 벽에 부딫힐 경우
    if ball_pos[0] < BALL_RADIUS :
        ball_pos[0] = BALL_RADIUS
        vxy[0] *= -0.9
    if ball_pos[0] > WIDTH - BALL_RADIUS: # 양옆
        ball_pos[0] = WIDTH - BALL_RADIUS 
        vxy[0] *= -0.9
    if ball_pos[1] < BALL_RADIUS :
        ball_pos[1] = BALL_RADIUS
        vxy[1] *= -0.9
    # if ball_pos[1] > HEIGHT - BALL_RADIUS: # 위아래
    #     ball_pos[1] = HEIGHT - BALL_RADIUS 
    #     vxy[1] *= -0.9

    
    # 장애물과 부딫히는 공 처리.
    for ob in obstacles :
        if len(ob) == 2 :
            if collision_circle(ball_pos, ob, vxy) != False : # 원 장애물과 부딫힐 경우
                _, vxy = collision_circle(ball_pos, ob, vxy)
                vxy *= 1.1
                score += 50
                sound_co.play()
                # 방향과 속력을 랜덤 함수를 사용해서 재구성해 보자.
        else : # 사각형 장애물과 부딫힐 경우
            if collision_circle_rect(ball_pos[0], ball_pos[1], ob) == "left" or collision_circle_rect(ball_pos[0], ball_pos[1], ob) == "right" :
                vxy[0] *= -1
                score += 20
                sound_co.play()
            if collision_circle_rect(ball_pos[0], ball_pos[1], ob) == "top" or collision_circle_rect(ball_pos[0], ball_pos[1], ob) == "bottom" :
                vxy[1] *= -1
                score += 20
                sound_co.play()
    for point in points : # 삼각형 장애물과 부딫힐 경우           
        if is_colliding_circle_triangle(ball_pos[0], ball_pos[1], point, vxy) != False :
            sound_co.play()
            _, vxy = is_colliding_circle_triangle(ball_pos[0], ball_pos[1], point, vxy)
            score += 35
            
    # 조종가능도형 부딫힘
    if is_colliding_circle_triangle(ball_pos[0], ball_pos[1], paddle_point_1, vxy) != False :
        sound_co.play()
        score += 100
        _, vxy = is_colliding_circle_triangle(ball_pos[0], ball_pos[1], paddle_point_1, vxy)
        if paddle_move == True : 
            vxy *= 1.1
            vxy += np.array([8,-8]) # 끼이는 현상 방지용 보정
            print(vxy)
        else :
            pass
    if is_colliding_circle_triangle(ball_pos[0], ball_pos[1], paddle_point_2, vxy) != False :
        sound_co.play()
        score += 100
        _, vxy = is_colliding_circle_triangle(ball_pos[0], ball_pos[1], paddle_point_2, vxy)
        if paddle_move == True : 
            vxy *= 1.1
            vxy += np.array([-8,-8])
            print(vxy)
            
        else :
            pass
    
    # 그리기 파트
    screen.blit(background_screen, (0, 0))
    
    # 조종가능 도형 그리기
    pygame.draw.polygon(screen, GRAY, paddle_point_1, 10)
    pygame.draw.polygon(screen, GRAY, paddle_point_2, 10)
    
    # 공
    pygame.draw.circle(screen, GRAY, ball_pos, BALL_RADIUS)
    pygame.draw.circle(screen, [150,150,150], np.array(ball_pos) + np.array([3,0]), 3)
    
    # 삼각형
    pygame.draw.polygon(screen, GRAY, points_1, 10)
    pygame.draw.polygon(screen, GRAY, points_2, 10)
    
    # 장애물 그리기
    for ob in obstacles :
        if len(ob) == 2 :
            pygame.draw.circle(screen, GRAY, [ob[0],ob[1]], OBSTACLE_B_R, 10)
        else :
            pygame.draw.rect(screen, GRAY, ob, 10)
    t = 0
    
    # 배경 그리기와 충돌 한꺼번에 처리
    for ba in background :
        t += 1
        if t <= 3 : # Rectangle
            pygame.draw.rect(screen, GRAY, ba)
            pygame.draw.rect(screen, [150,150,150], ba, 10)
            collision_side = collision_circle_rect(ball_pos[0], ball_pos[1], ba)
            if collision_side == "left" or collision_side == "right":
                vxy[0] *= -1
            if collision_side == "top" or collision_side == "bottom":
                vxy[1] *= -1
        else : # Triangle
            pygame.draw.polygon(screen, [150,150,150], ba)
            if is_colliding_circle_triangle(ball_pos[0], ball_pos[1], ba, vxy) != False :
                _, vxy = is_colliding_circle_triangle(ball_pos[0], ball_pos[1], ba, vxy)
    points_1 = [(70, 500), (70, 600), (130, 600)]
    for i in points_1 :
        pygame.draw.circle(screen, [100,100,100], i, 8)
    points_2 = [(WIDTH - 70, 500), (WIDTH - 70, 600), (WIDTH - 130, 600)]
    for i in points_2 :
        pygame.draw.circle(screen, [100,100,100], i, 8)
    background_5 = [[40, HEIGHT - 150], [40, HEIGHT - 100], [WIDTH/2 - 130, HEIGHT - 100], ]
    for i in background_5 :
        pygame.draw.circle(screen, [100,100,100], i, 8)
    background_6 = [[WIDTH - 40, HEIGHT - 150], [WIDTH - 40, HEIGHT - 100], [WIDTH/2 + 130, HEIGHT - 100], ] 
    for i in background_6 :
        pygame.draw.circle(screen, [100,100,100], i, 8)
    for i in paddle_point_1 :
        pygame.draw.circle(screen, [100,100,100], i, 8)
    for i in paddle_point_2 :
        pygame.draw.circle(screen, [100,100,100], i, 8)
    
    screen.blit(text, (5, 65))

    pygame.display.flip()
    clock.tick(120)
    
pygame.quit()
    
