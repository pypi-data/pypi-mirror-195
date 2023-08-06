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
import os

class Actions:
    def __init__(self):
        self.user = os.getenv('USER', 'nobody')
        self.base_url = os.getenv('BASE_URL', 'http://localhost/api/v1/') + f"/user/{self.user}"
        self.token = os.getenv('TOKEN', 'invalid')
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.sub_action = self.__class__.__name__.lower()

    def get_action_spec(self, id, action):
        endpoint = self.base_url + "/{}/{}/specs/{}/schema".format(self.sub_action, id, action)
        response = requests.get(endpoint, headers=self.headers)
        data = response.json()["default"]
        return data

    def get_automl_defaults(self, id, action):
        endpoint = self.base_url + "/{}/{}/specs/{}/schema".format(self.sub_action, id, action)
        response = requests.get(endpoint, headers=self.headers)
        data = response.json()["automl_default_parameters"]
        return data

    def run_action(self, id, job, action):
        data = json.dumps( { "job": job, "actions": action } )
        endpoint = self.base_url + "/{}/{}/job".format(self.sub_action, id)
        response = requests.post(endpoint, data=data, headers=self.headers)
        job_id = response.json()[0]
        return job_id

    def model_job_cancel(self, id, job):
        endpoint = self.base_url + "/{}/{}/job/{}/cancel".format(self.sub_action, id, job)
        response = requests.post(endpoint, headers=self.headers)

    def model_job_resume(self, id, job):
        endpoint = self.base_url + "/{}/{}/job/{}/resume".format(self.sub_action, id, job)
        response = requests.post(endpoint, headers=self.headers)
