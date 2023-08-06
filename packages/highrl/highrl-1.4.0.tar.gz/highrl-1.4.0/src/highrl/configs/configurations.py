"""Configurations for training and inference"""
robot_config_str = """
[eval]
n_eval_episodes = 4
robot_init_x_pos = 10
robot_init_y_pos = 10
goal_x_pos = 240
goal_y_pos = 240
eval_big_obs_count = 2
eval_med_obs_count = 4
eval_sml_obs_count = 4
eval_big_obs_dim = 40
eval_med_obs_dim = 25
eval_sml_obs_dim = 10

[dimensions]
width = 256
height = 256
robot_radius = 5
goal_radius = 2

[timesteps]
delta_t = 0.2
# 1e3
max_episode_steps = 100
# 1e5
max_session_steps = 200

[lidar]
n_angles = 1080
lidar_angle_increment = 005817764
lidar_min_angle = 0
lidar_max_angle = 6.283185307

[reward]
collision_score = -25
reached_goal_score = 100
minimum_velocity = 0.1
minimum_distance = 0.1
maximum_distance = 1470
velocity_std = 2.0
alpha = 0.4
progress_discount = 0.4

[render]
render_each = 10
save_to_file = False

[env]
epsilon = 1

[statistics]
collect_statistics = True
scenario = train
"""


# ---------------------TEAHCER CONFIGURATIONS-----------------#
teacher_config_str = """
[reward]
alpha = 0.4
terminal_state_reward = 100
max_reward = 3600
base_difficulty = 590
overlap_goal_penality = -100
infinite_difficulty_penality = -100
too_close_to_goal_penality = -50
is_goal_or_robot_overlap_obstacles_penality = -100
gamma = 0.4
diff_increase_factor = 1.15
base_num_successes = 5
num_successes_increase_factor = 1.2

[env]
advance_probability = 0.9
max_hard_obstacles_count = 2
max_medium_obstacles_count = 5
max_small_obstacles_count = 7
hard_obstacles_max_dim = 10
hard_obstacles_min_dim = 9
medium_obstacles_max_dim = 5
medium_obstacles_min_dim = 4
small_obstacles_max_dim = 4
small_obstacles_min_dim = 3
# {flat: 1D, rings: 2D}
lidar_mode = flat

[render]
render_eval = False

[statistics]
scenario = train
collect_statistics = True
robot_log_eval_freq = 5
n_robot_eval_episodes = 5
save_model_freq = 1

[timesteps]
max_sessions = 10
"""

# ---------------------EVALUATIONS CONFIGURATIONS-----------------#
eval_config_str = """
[eval]
n_eval_episodes = 4
robot_init_x_pos = 10
robot_init_y_pos = 10
goal_x_pos = 240
goal_y_pos = 240
eval_big_obs_count = 2
eval_med_obs_count = 4
eval_sml_obs_count = 4
eval_big_obs_dim = 40
eval_med_obs_dim = 25
eval_sml_obs_dim = 10

[dimensions]
width = 256
height = 256
robot_radius = 5
goal_radius = 2

[timesteps]
delta_t = 0.2
# 1e3
max_episode_steps = 100
# 1e5
max_session_steps = 200

[lidar]
n_angles = 1080
lidar_angle_increment = 005817764
lidar_min_angle = 0
lidar_max_angle = 6.283185307

[reward]
collision_score = -25
reached_goal_score = 100
minimum_velocity = 0.1
minimum_distance = 0.1
maximum_distance = 1470
velocity_std = 2.0
alpha = 0.4
progress_discount = 0.4

[render]
render_each = 10
save_to_file = False

[env]
epsilon = 1

[statistics]
collect_statistics = True
scenario = train
"""
