# SPDX-FileCopyrightText: Copyright (c) 2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import enum

class dataset_format(str, enum.Enum):
    default = "default"
    kitti = "kitti"
    lprnet = "lprnet"
    coco = "coco"
    raw = "raw"
    coco_raw = "coco_raw"
    ljspeech = "ljspeech"
    hifigan = "hifigan"
    custom = "custom"
    auxillary = "auxillary"
    unet = "unet"

class dataset_type(str, enum.Enum):
    semantic_segmentation = "semantic_segmentation"
    image_classification = "image_classification"
    object_detection = "object_detection"
    character_recognition = "character_recognition"
    instance_segmentation = "instance_segmentation"
    speech = "speech"
    mel_spectrogram = "mel_spectrogram"

class network_type(str, enum.Enum):
    detectnet_v2 = "detectnet_v2"
    efficientdet = "efficientdet"
    lprnet = "lprnet"
    unet = "unet"
    multitask_classification = "multitask_classification"
    classification = "classification"
    mask_rcnn = "mask_rcnn"
    ssd = "ssd"
    retinanet = "retinanet"
    faster_rcnn = "faster_rcnn"
    yolo_v3 = "yolo_v3"
    yolo_v4 = "yolo_v4"
    yolo_v4_tiny = "yolo_v4_tiny"
    spectro_gen = "spectro_gen"
    vocoder = "vocoder"
