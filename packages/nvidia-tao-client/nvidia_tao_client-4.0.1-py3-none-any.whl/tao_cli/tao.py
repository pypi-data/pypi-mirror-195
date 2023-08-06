# SPDX-FileCopyrightText: Copyright (c) 2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import click

from tao_cli.login import login

from tao_cli.networks.detectnet_v2 import detectnet_v2
from tao_cli.networks.efficientdet import efficientdet
from tao_cli.networks.lprnet import lprnet
from tao_cli.networks.unet import unet
from tao_cli.networks.multi_task_classification import multitask_classification
from tao_cli.networks.multi_class_classification import classification
from tao_cli.networks.mask_rcnn import mask_rcnn
from tao_cli.networks.ssd import ssd
from tao_cli.networks.retinanet import retinanet
from tao_cli.networks.faster_rcnn import faster_rcnn
from tao_cli.networks.yolo_v3 import yolo_v3
from tao_cli.networks.yolo_v4 import yolo_v4
from tao_cli.networks.yolo_v4_tiny import yolo_v4_tiny
from tao_cli.networks.spectro_gen import spectro_gen
from tao_cli.networks.vocoder import vocoder

@click.group()
@click.version_option(package_name='nvidia-tao-client')
@click.pass_context
def cli(ctx):
    pass

cli.add_command(login)
cli.add_command(detectnet_v2)
cli.add_command(efficientdet)
cli.add_command(lprnet)
cli.add_command(unet)
cli.add_command(multitask_classification)
cli.add_command(classification)
cli.add_command(mask_rcnn)
cli.add_command(ssd)
cli.add_command(retinanet)
cli.add_command(faster_rcnn)
cli.add_command(yolo_v3)
cli.add_command(yolo_v4)
cli.add_command(yolo_v4_tiny)
cli.add_command(spectro_gen)
cli.add_command(vocoder)

if __name__ == '__main__':
    cli()

