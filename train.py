import argparse
import functools

import yaml

from ppasr.trainer import PPASRTrainer
from ppasr.utils.utils import add_arguments, print_arguments

parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(add_arguments, argparser=parser)
add_arg('configs',          str,    'configs/conformer_online_zh.yml',       '配置文件')
add_arg("local_rank",       int,    0,                             '多卡训练的本地GPU')
add_arg("use_gpu",          bool,   True,                          '是否使用GPU训练')
add_arg('augment_conf_path',str,    'configs/augmentation.json',   '数据增强的配置文件，为json格式')
add_arg('save_model_path',  str,    'models/',                  '模型保存的路径')
add_arg('resume_model',     str,    None,                       '恢复训练，当为None则不使用预训练模型')
add_arg('pretrained_model', str,    None,                       '预训练模型的路径，当为None则不使用预训练模型')
args = parser.parse_args()

# 读取配置文件
with open(args.configs, 'r', encoding='utf-8') as f:
    configs = yaml.load(f.read(), Loader=yaml.FullLoader)
print_arguments(args, configs)

# 获取训练器
trainer = PPASRTrainer(configs=configs, use_gpu=args.use_gpu)

trainer.train(save_model_path=args.save_model_path,
              resume_model=args.resume_model,
              pretrained_model=args.pretrained_model,
              augment_conf_path=args.augment_conf_path)
