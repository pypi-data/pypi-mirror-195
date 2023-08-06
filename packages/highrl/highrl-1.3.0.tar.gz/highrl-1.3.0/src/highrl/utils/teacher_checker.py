"""Difficulty computation implementation for the teacher"""
from typing import Tuple, List
import logging
import time
from collections import deque
import numpy as np

from highrl.obstacle.obstacles import Obstacles
from highrl.utils import Position
from highrl.agents.robot import Robot


INF = 256 * 256  # w * h
_LOG = logging.getLogger(__name__)


def check_valid_point(point: np.ndarray, env_size: int) -> bool:
    """check if input point is within input constraints
    Note that that environment width and height are assumed to
    be equal.

    Args:
        point (np.ndarray): Input point coordinates
        env_size (int): Environment size

    Returns:
        bool: Flag whether point satisfies constraints
    """
    is_valid = (point < env_size).all() and (point >= 0).all()
    return is_valid.item()


def check_point_overlap(
    obstacles: Obstacles,
    pos: Position[int],
    omit_first_four: bool = True,
) -> bool:
    """Check if the provided point is not overlapping with any of the obstacles

    Args:
        obstacles (Obstacles): Obstacles in the environemnt. Those might include
        border obstacles.
        pos (Position[int]): Position of the object to be checked for overlapping
        omit_first_four (bool, optional): Whether to ignore the first 4 obstacles
        which are assumed to be the border obstacles. Defaults to True.

    Returns:
        bool: Whether the provided point satisfies the overlapping contraints
    """
    for idx, obstacle in enumerate(obstacles):
        if idx < 4 and omit_first_four:
            continue

        if obstacle.overlap_point(pos):
            return False
    return True


def get_path_bfs(
    obstacles: Obstacles,
    env_size: int,
    robot_pos: Position[int],
    goal_pos: Position[int],
    omit_first_four: bool = True,
) -> Tuple[bool, List[Position[int]]]:
    """Check if there is a valid path in the input segment

    Args:
        obstacles (Obstacles): Obstacles in the environemnt
        env_size (int): Environment size. Note that the environment is
        assumed to be a square here.
        robot_pos (List[int]): Robot position
        goal_pos (List[int]): Goal position
        omit_first_four (bool): Whether to ignore the first four obstacles which usually
        represent the boarder of the env. Defaults to True.

    Returns:
        Tuple[bool, List[Position[int]]]: Flag whether there exists a path, The points along the
        generated path.
    """
    delta_x = [-1, -1, -1, 0, 0, 1, 1, 1]
    delta_y = [-1, 0, 1, -1, 1, -1, 0, 1]
    num_dirs = 8

    # Intializing empty map
    # False represents an empty space in the map
    first_time = time.time()
    default_pos = Position[int](-1, -1)
    env_map = np.full((env_size + 1, env_size + 1), False)
    
    # Parent position stores the parent cell for each cell in the map
    # All of its values are initialized as (-1, -1) to ensure that each
    # point in the generated path MUST have a parent position.
    parent_pos = [
        [default_pos for _ in range(env_size + 1)] for _ in range(env_size + 1)
    ]
    _LOG.warning("Initialized map in %.2f seconds", time.time() - first_time)

    # Breadth first search till you either find the
    # goal or you stop (aka. no valid in this map)
    # Intializing the queue with the robot position
    queue = deque([robot_pos], maxlen=env_size)
    env_map[robot_pos.x][robot_pos.y] = True

    # Loop till you are out of non-visited points
    while len(queue) > 0:
        pos = queue.popleft()

        # If goal is found, STOP
        if pos == goal_pos:
            path: List[Position[int]] = [goal_pos]
            while path[-1] != robot_pos:
                last_pos = path[-1]
                path.append(parent_pos[last_pos.x][last_pos.y])
            return True, path

        # Loop over all directions
        for idx in range(num_dirs):
            new_pos = Position[int](pos.x + delta_x[idx], pos.y + delta_y[idx])
            if (
                check_valid_point(new_pos.get_coords(), env_size)
                and check_point_overlap(obstacles, new_pos, omit_first_four)
                and not env_map[new_pos.x][new_pos.y]
            ):
                # If the new point is inside the rectangle (between robot and goal),
                # it's within the boundaries of the env, and it's not occupied, add it
                # to the list of points to be explored.
                env_map[new_pos.x][new_pos.y] = True
                queue.append(new_pos)
                parent_pos[new_pos.x][new_pos.y] = pos

    # If we reach here, the goal has not been reached
    return False, []


def convex_hull_compute(points: List[Position[int]]) -> List[Position[int]]:
    """Compute convex hull polygen of input points

    Args:
        points (List[List[int]]): input points

    Returns:
        List[List[int]]: points defining convex hull polygen
    """
    points = sorted(points)
    convex_polygen: List[Position[int]] = []
    for _ in range(2):
        num_points = len(convex_polygen)
        for point in points:
            while len(convex_polygen) >= num_points + 2:
                second_point = convex_polygen[-2]
                first_point = convex_polygen[-1]
                if point.triangle_cross(first_point, second_point) <= 0:
                    break
                convex_polygen.pop(-1)
            convex_polygen.append(point)
        convex_polygen.pop(-1)
        points.reverse()
    return convex_polygen


def get_area_of_convex_polygen(points: List[Position[int]]) -> int:
    """Compute the area of a polygen using its points

    Args:
        points (List[List[int]]): Input points for the polygen

    Returns:
        float: Area of input polygen
    """
    assert len(points), "Empty points list"
    num = len(points)
    points.append(points[0])
    area: int = 0
    for i in range(num):
        area += points[i].inner_cross(points[i + 1])
    return abs(area)


def sample_line_points(
    left_pos: Position,
    right_pos: Position,
    step_size: int = 1,
) -> List[Position]:
    """Sample points from a line provided only two points defining the line

    Args:
        left_pos (Position): First point on the line
        right_pos (Position): Second point on the line
        step_size (int): Space between two consecutive samples on the x-axis.
        Defaults to 1.

    Returns:
        List[Position]: Sampled points for the line
    """
    assert isinstance(step_size, int), "step_size must be an integer"
    sampled_points: List[Position[int]] = []
    slope = (right_pos.y - left_pos.y) / (right_pos.x - left_pos.x + 1e-3)
    intercept = right_pos.y - slope * right_pos.x
    min_x = min(left_pos.x, right_pos.x)
    max_x = max(left_pos.x, right_pos.x)

    for sample_x in range(min_x, max_x + 1, step_size):
        sample_y = int(slope * sample_x + intercept)
        sampled_points.append(Position[int](sample_x, sample_y))

    return sampled_points


def compute_difficulty(
    obstacles: Obstacles,
    robot: Robot,
    width: int,
    _: int,
) -> Tuple[float, int]:
    """Calculate env complexity using convex_hull algorithm

    Args:
        obstacles (Obstacles): env obstacles
        robot (Robot): env robot
        width (int): env width
        height (int): env height

    Returns:
        Tuple[float, int]: env area difficulty, env obstacles difficulty
    """
    # Convert robot/goal position to integer for correct operations
    rob_pos = robot.get_position().to_int()
    goal_pos = robot.get_goal_position().to_int()

    # Run BFS to find a path from goal to robot
    is_valid, path = get_path_bfs(
        obstacles,
        width,
        rob_pos,
        goal_pos,
    )

    # If there is no valid path, return infinite difficulty
    if not is_valid:
        return INF, max(0, len(obstacles.obstacles_list) - 4)

    # Sample points on the line between the robot and the goal
    robot_to_goal_points = sample_line_points(rob_pos, goal_pos, step_size=1)

    # Add points sampled from the line between the goal and robot to the path
    path.extend(robot_to_goal_points)

    # Get the points representing the convex polygon
    convex_hull_points = convex_hull_compute(path)

    # Compute the area of the convex polygon
    difficulty_area = get_area_of_convex_polygen(convex_hull_points)

    # Note that "2" here is just a constant, its value would not matter.
    return difficulty_area, 2
