"""Train your robot with a teacher to guide the process

Usage
------------------
    $ highrl [--options]

Get data about the arguments

    $ highrl -help

Or just run the following to the default
    $ highrl

Do not forget to specify the output dir for models saving
    $ highrl --output_dir=<your-ouput-dir>

Version
------------------
 - highrl v1.4.0
"""
import os
import argparse
from time import time
import logging
from stable_baselines3.ppo.ppo import PPO
from stable_baselines3.common.callbacks import CallbackList

from highrl.policy.feature_extractors import LSTMFeatureExtractor
from highrl.policy.policy_networks import LinearActorCriticPolicy
from highrl.utils.parser import parse_args, generate_agents_config, handle_output_dir
from highrl.callbacks import teacher_callback as t_callback
from highrl.envs.teacher_env import TeacherEnv
from highrl.utils.logger import init_logger

init_logger()
_LOG = logging.getLogger(__name__)


def train_teacher(args: argparse.Namespace) -> None:
    """Training script for the teacher

    Args:
        args (argparse.Namespace): Arguments from argparser
    """
    robot_config, teacher_config, eval_config = generate_agents_config(
        args.robot_config_path,
        args.teacher_config_path,
        args.eval_config_path,
    )

    if args.render_each > -1:
        robot_config.set("render", "render_each", value=args.render_each)

    if args.render_each_eval > -1:
        eval_config.set("render", "render_each", value=args.render_each_eval)

    if args.lidar_mode != "none":
        teacher_config.set("env", "lidar_mode", value=str(args.lidar_mode))

    max_robot_steps = robot_config.getint("timesteps", "max_session_steps")
    max_episode_timesteps = robot_config.getint("timesteps", "max_episode_steps")
    max_sessions = teacher_config.getint("timesteps", "max_sessions")
    teacher_config.set("timesteps", "max_session_timesteps", value=str(max_robot_steps))
    teacher_config.set(
        "timesteps",
        "max_episode_timesteps",
        value=str(max_episode_timesteps),
    )

    args = handle_output_dir(args=args)
    teacher_env = TeacherEnv(
        robot_config=robot_config,
        teacher_config=teacher_config,
        eval_config=eval_config,
        args=args,
    )
    policy_kwargs = {
        "features_extractor_class": LSTMFeatureExtractor,
        "features_extractor_kwargs": {"features_dim": 6},
    }
    logpath = os.path.join(args.teacher_logs_path, "teacher_logs.csv")
    save_model_path = os.path.join(args.teacher_models_path, "during_training")
    if not os.path.isdir(save_model_path):
        os.mkdir(save_model_path)
    teacher_log_callback = t_callback.TeacherLogCallback(
        train_env=teacher_env,
        logpath=logpath,
        save_freq=1,
        verbose=0,
    )
    teacher_max_steps_callback = t_callback.TeacherMaxStepsCallback(
        max_steps=max_sessions
    )
    teacher_save_model_callback = t_callback.TeacherSaveModelCallback(
        train_env=teacher_env,
        save_path=save_model_path,
        save_freq=teacher_env.cfg.teacher_save_model_freq,
    )
    callback = CallbackList(
        [
            teacher_log_callback,
            teacher_max_steps_callback,
            teacher_save_model_callback,
        ]
    )
    if args.initial_teacher_model != "none":
        teacher_model = args.initial_teacher_model
        model = PPO.load(
            path=teacher_model,
            env=teacher_env,
            device=args.device,
        )
    else:
        model = PPO(
            LinearActorCriticPolicy,
            teacher_env,
            verbose=1,
            policy_kwargs=policy_kwargs,
            learning_rate=0.0001,
            batch_size=16,
            device=args.device,
        )
    model.learn(total_timesteps=int(1e7), callback=callback)
    model.save(f"{args.teacher_models_path}/model_{int(time())}")


def main() -> None:
    """Main script implementation"""
    args = parse_args()
    _LOG.info("Starting training %s", args.env_mode)

    if args.env_mode == "teacher":
        train_teacher(args)
    else:
        err_message = "Robot training is not implemented"
        _LOG.critical(err_message)
        raise NotImplementedError(err_message)


if __name__ == "__main__":
    main()
