# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
import uuid


def new() -> str:
    """
    new correlation id
    """
    return str(uuid.uuid4().hex)
