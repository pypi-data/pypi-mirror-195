# SPDX-FileCopyrightText: Copyright (c) 2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

#
# SPECTRO_GEN
#
import click
import json

from tao_cli.cli_actions.dataset import Dataset
from tao_cli.cli_actions.model import Model

from tao_cli.constants import dataset_format, dataset_type, network_type

dataset_obj = Dataset()
model_obj = Model()

@click.group()
def spectro_gen():
    pass

@spectro_gen.command()
@click.option('--dataset_type', prompt='dataset_type', type=click.Choice(dataset_type), help='The dataset type.', required=True)
@click.option('--dataset_format', prompt='dataset_format', type=click.Choice(dataset_format), help='The dataset format.', required=True)
def dataset_create(dataset_type, dataset_format):
    id = dataset_obj.dataset_create(dataset_type, dataset_format)
    click.echo(f"{id}")

@spectro_gen.command()
@click.option('--id', prompt='id', help='The dataset ID.', required=True)
@click.option('--action', prompt='action', help='The dataset convert action.', required=True)
def dataset_convert_defaults(id, action):
    data = dataset_obj.get_action_spec(id, action)
    click.echo(json.dumps(data, indent=2))

@spectro_gen.command()
@click.option('--id', prompt='id', help='The dataset ID.', required=True)
@click.option('--action', prompt='action', help='The dataset convert action.', required=True)
def dataset_convert(id, action):
    job_id = dataset_obj.run_action(id=id, job=None, action=[action])
    click.echo(f"{job_id}")

@spectro_gen.command()
@click.option('--id', prompt='id', help='The dataset ID.', required=True)
def dataset_pitch_stats_defaults(id):
    data = dataset_obj.get_action_spec(id, "pitch_stats")
    click.echo(json.dumps(data, indent=2))

@spectro_gen.command()
@click.option('--id', prompt='id', help='The dataset ID.', required=True)
@click.option('--job', help='The dataset convert job ID.', required=False, default=None)
def dataset_pitch_stats(id, job):
    job_id = dataset_obj.run_action(id, job, ["pitch_stats"])
    click.echo(f"{job_id}")

@spectro_gen.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', prompt='job', help='The job ID.', required=True)
def dataset_job_cancel(id, job):
    job = dataset_obj.dataset_job_cancel(id, job)
    click.echo(f"{job}")

@spectro_gen.command()
@click.option('--network_arch', prompt='network_arch', type=click.Choice(network_type), help='Network architecture.', required=True)
@click.option('--encryption_key', prompt='encryption_key', help='Encryption_key.', required=True)
def model_create(network_arch, encryption_key):
    id = model_obj.model_create(network_arch, encryption_key)
    click.echo(f"{id}")

@spectro_gen.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_dataset_convert_defaults(id):
    data = model_obj.get_action_spec(id, "dataset_convert")
    click.echo(json.dumps(data, indent=2))

@spectro_gen.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_dataset_convert(id):
    job_id = model_obj.run_action(id=id, job=None, action=["dataset_convert"])
    click.echo(f"{job_id}")

@spectro_gen.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_finetune_defaults(id):
    data = model_obj.get_action_spec(id, "finetune")
    click.echo(json.dumps(data, indent=2))

@spectro_gen.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The pitch stats job ID.', required=False, default=None)
def model_finetune(id, job):
    job_id = model_obj.run_action(id, job, ["finetune"])
    click.echo(f"{job_id}")

@spectro_gen.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_infer_defaults(id):
    data = model_obj.get_action_spec(id, "infer")
    click.echo(json.dumps(data, indent=2))

@spectro_gen.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The finetune job ID.', required=False, default=None)
def model_infer(id, job):
    job_id = model_obj.run_action(id, job, ["infer"])
    click.echo(f"{job_id}")

@spectro_gen.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', prompt='job', help='The job ID.', required=True)
def model_job_cancel(id, job):
    model_obj.model_job_cancel(id, job)
    click.echo(f"{job}")

@spectro_gen.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', prompt='job', help='The job ID.', required=True)
def model_job_resume(id, job):
    model_obj.model_job_resume(id, job)
    click.echo(f"{job}")


