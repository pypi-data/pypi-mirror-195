# SPDX-FileCopyrightText: Copyright (c) 2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import requests
import click
import json
import os

@click.command()
@click.option('--ngc-api-key', prompt='ngc_api_key', help='Your NGC API KEY.', required=True)
def login(ngc_api_key):
    base_url = os.getenv('BASE_URL', 'http://localhost/api/v1')
    endpoint = base_url + "/login/" + ngc_api_key
    response = requests.get(endpoint)
    click.echo(json.dumps(response.json()))
