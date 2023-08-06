# SPDX-FileCopyrightText: Copyright (c) 2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import json
import requests

from tao_cli.cli_actions.actions import Actions

class Model(Actions):
    def __init__(self):
        super().__init__()

    def model_create(self, network_arch, encryption_key):
        data = json.dumps( {"network_arch": network_arch, "encryption_key": encryption_key} )
        endpoint = self.base_url + "/model"
        response = requests.post(endpoint, data=data, headers=self.headers)
        id = response.json()["id"]
        return id
