# -*- coding:utf-8 -*-
# Copyright (C) 2023  E.SUN BANK.
# @Author: Hsin-Hsien Ho, Wan-Chu Lin
# @Date: 2023/01
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class CustomException(HTTPException):
    def __init__(self, status_code: int = 400, message: str = "") -> None:
        super().__init__(status_code=status_code)
        self.message = message


def exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code, content={"error": True, "msg": exc.message}
    )
