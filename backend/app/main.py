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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.exceptions import CustomException, exception_handler
from app.routers import login, teams, vote, db, docs, users, time


def get_application():
    app = FastAPI(docs_url=None)

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(CustomException, exception_handler)

    app.include_router(docs.router)

    app.include_router(
        db.router,
        prefix="/db",
        tags=["db"],
    )
    
    app.include_router(
        time.router,
        prefix="/time",
        tags=["time"],
    )

    app.include_router(
        login.router,
        prefix="/login",
        tags=["login"],
    )

    app.include_router(
        teams.router,
        prefix="/teams",
        tags=["teams"],
    )

    app.include_router(
        vote.router,
        prefix="/vote",
        tags=["vote"],
    )

    app.include_router(
        users.router,
        prefix="/users",
        tags=["users"],
    )

    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    return app


app = get_application()
