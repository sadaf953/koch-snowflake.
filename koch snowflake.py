import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 900
BACKGROUND = (0, 0, 0)
SNOWFLAKE_COLOR = (200, 200, 255)
MIN_DEPTH = 0
MAX_DEPTH = 5

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Koch Snowflake")

def calculate_koch_points(start, end, depth):
    """Calculate points for Koch curve."""
    if depth == 0:
        return [start, end]
    
    # Calculate the vector from start to end
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    
    # Calculate one third and two thirds points
    one_third = (start[0] + dx/3, start[1] + dy/3)
    two_thirds = (start[0] + 2*dx/3, start[1] + 2*dy/3)
    
    # Calculate the peak point of the equilateral triangle
    angle = math.atan2(dy, dx) - math.pi/3  # 60 degrees
    length = math.sqrt(dx*dx + dy*dy) / 3
    peak = (one_third[0] + length * math.cos(angle),
            one_third[1] + length * math.sin(angle))
    
    # Recursively calculate points for each segment
    points = []
    points.extend(calculate_koch_points(start, one_third, depth-1)[:-1])
    points.extend(calculate_koch_points(one_third, peak, depth-1)[:-1])
    points.extend(calculate_koch_points(peak, two_thirds, depth-1)[:-1])
    points.extend(calculate_koch_points(two_thirds, end, depth-1))
    
    return points

def draw_koch_snowflake(depth):
    """Draw the complete Koch snowflake."""
    # Calculate initial triangle points
    size = min(WIDTH, HEIGHT) - 300  # Leave margin
    height = size * math.sqrt(3) / 2
    
    # Calculate center position
    center_x = WIDTH / 2
    center_y = HEIGHT / 2
    
    # Calculate vertices of the initial triangle
    top = (center_x, center_y - height/2)
    bottom_left = (center_x - size/2, center_y + height/2)
    bottom_right = (center_x + size/2, center_y + height/2)
    
    # Get points for each side
    points1 = calculate_koch_points(top, bottom_right, depth)
    points2 = calculate_koch_points(bottom_right, bottom_left, depth)
    points3 = calculate_koch_points(bottom_left, top, depth)
    
    # Draw all segments
    for points in [points1, points2, points3]:
        for i in range(len(points)-1):
            pygame.draw.line(screen, SNOWFLAKE_COLOR, 
                           (int(points[i][0]), int(points[i][1])),
                           (int(points[i+1][0]), int(points[i+1][1])), 2)

def main():
    depth = 0
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    depth = min(MAX_DEPTH, depth + 1)
                elif event.key == pygame.K_DOWN:
                    depth = max(MIN_DEPTH, depth - 1)
                elif event.key == pygame.K_r:
                    depth = 0
        
        # Clear screen
        screen.fill(BACKGROUND)
        
        # Draw snowflake
        draw_koch_snowflake(depth)
        
        # Draw UI text
        font = pygame.font.Font(None, 36)
        depth_text = font.render(f"Depth: {depth}", True, (255, 255, 255))
        help_text = font.render("Up/Down: Change Depth | R: Reset", True, (255, 255, 255))
        
        screen.blit(depth_text, (10, 10))
        screen.blit(help_text, (10, HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()