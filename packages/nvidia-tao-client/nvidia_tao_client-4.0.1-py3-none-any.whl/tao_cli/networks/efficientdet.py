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
# EfficientDet
#
import click
import json

from tao_cli.cli_actions.dataset import Dataset
from tao_cli.cli_actions.model import Model

from tao_cli.constants import dataset_format, dataset_type, network_type

dataset_obj = Dataset()
model_obj = Model()

@click.group()
def efficientdet():
    pass

@efficientdet.command()
@click.option('--dataset_type', prompt='dataset_type', type=click.Choice(dataset_type), help='The dataset type.', required=True)
@click.option('--dataset_format', prompt='dataset_format', type=click.Choice(dataset_format), help='The dataset format.', required=True)
def dataset_create(dataset_type, dataset_format):
    id = dataset_obj.dataset_create(dataset_type, dataset_format)
    click.echo(f"{id}")

@efficientdet.command()
@click.option('--id', prompt='id', help='The dataset ID.', required=True)
@click.option('--action', prompt='action', help='The dataset convert action.', required=True)
def dataset_convert_defaults(id, action):
    data = dataset_obj.get_action_spec(id, action)
    click.echo(json.dumps(data, indent=2))

@efficientdet.command()
@click.option('--id', prompt='id', help='The dataset ID.', required=True)
@click.option('--action', prompt='action', help='The dataset convert action.', required=True)
def dataset_convert(id, action):
    job_id = dataset_obj.run_action(id=id, job=None, action=[action])
    click.echo(f"{job_id}")

@efficientdet.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', prompt='job', help='The job ID.', required=True)
def dataset_job_cancel(id, job):
    job = dataset_obj.dataset_job_cancel(id, job)
    click.echo(f"{job}")

@efficientdet.command()
@click.option('--network_arch', prompt='network_arch', type=click.Choice(network_type), help='Network architecture.', required=True)
@click.option('--encryption_key', prompt='encryption_key', help='Encryption_key.', required=True)
def model_create(network_arch, encryption_key):
    id = model_obj.model_create(network_arch, encryption_key)
    click.echo(f"{id}")

@efficientdet.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_train_defaults(id):
    data = model_obj.get_action_spec(id, "train")
    click.echo(json.dumps(data, indent=2))

@efficientdet.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_automl_defaults(id):
    data = model_obj.get_automl_defaults(id, "train")
    click.echo(json.dumps(data, indent=2))

@efficientdet.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The dataset convert job ID.', required=False, default=None)
def model_train(id, job):
    job_id = model_obj.run_action(id, job, ["train"])
    click.echo(f"{job_id}")

@efficientdet.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_evaluate_defaults(id):
    data = model_obj.get_action_spec(id, "evaluate")
    click.echo(json.dumps(data, indent=2))

@efficientdet.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The train, prune or retrain job ID.', required=False, default=None)
def model_evaluate(id, job):
    job_id = model_obj.run_action(id, job, ["evaluate"])
    click.echo(f"{job_id}")

@efficientdet.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_export_defaults(id):
    data = model_obj.get_action_spec(id, "export")
    click.echo(json.dumps(data, indent=2))

@efficientdet.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The train, prune or retrain job ID.', required=False, default=None)
def model_export(id, job):
    job_id = model_obj.run_action(id, job, ["export"])
    click.echo(f"{job_id}")

@efficientdet.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_convert_defaults(id):
    data = model_obj.get_action_spec(id, "convert")
    click.echo(json.dumps(data, indent=2))

@efficientdet.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The export job ID.', required=False, default=None)
def model_convert(id, job):
    job_id = model_obj.run_action(id, job, ["convert"])
    click.echo(f"{job_id}")

@efficientdet.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_inference_defaults(id):
    data = model_obj.get_action_spec(id, "inference")
    click.echo(json.dumps(data, indent=2))

@efficientdet.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The train, prune, retrain, export or convert job ID.', required=False, default=None)
def model_inference(id, job):
    job_id = model_obj.run_action(id, job, ["inference"])
    click.echo(f"{job_id}")

@efficientdet.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_prune_defaults(id):
    data = model_obj.get_action_spec(id, "prune")
    click.echo(json.dumps(data, indent=2))

@efficientdet.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The train job ID.', required=False, default=None)
def model_prune(id, job):
    job_id = model_obj.run_action(id, job, ["prune"])
    click.echo(f"{job_id}")

@efficientdet.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_retrain_defaults(id):
    data = model_obj.get_action_spec(id, "retrain")
    click.echo(json.dumps(data, indent=2))

@efficientdet.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The prune job ID.', required=False, default=None)
def model_retrain(id, job):
    job_id = model_obj.run_action(id, job, ["retrain"])
    click.echo(f"{job_id}")

@efficientdet.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', prompt='job', help='The job ID.', required=True)
def model_job_cancel(id, job):
    model_obj.model_job_cancel(id, job)
    click.echo(f"{job}")

@efficientdet.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', prompt='job', help='The job ID.', required=True)
def model_job_resume(id, job):
    model_obj.model_job_resume(id, job)
    click.echo(f"{job}")
