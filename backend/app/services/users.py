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

import base64
import logging
from app.exceptions import CustomException
from app.schema.users import LoginRequest, UserCreate
from app.models.account import Account
from app.models.login_hist import LoginHist
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from passlib.context import CryptContext

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)


SALT = 'YOUR_SALT'


class HashPlain:
    @staticmethod
    def get_plain_hash(plain):
        encry_str = ""
        for i, j in zip(plain, SALT):
            temp = str(ord(i)+ord(j)) + '_'
            encry_str = encry_str + temp
        s1 = base64.b64encode(encry_str.encode("utf-8"))
        return s1.decode("utf-8")

    @staticmethod
    def dectry(hashed):
        p = base64.b64decode(hashed).decode("utf-8")
        dec_str = ""
        for i, j in zip(p.split("_")[:-1], SALT):
            temp = chr(int(i) - ord(j))
            dec_str = dec_str+temp
        return dec_str


def login(db: Session, request: LoginRequest):

    try:

        user = db.query(Account).filter(Account.account == request.account)
        # Account Not Found
        if not user.first():
            login_hist = LoginHist(account=request.account.lower(),
                                   status="Account Not Found")
            db.add(login_hist)
            db.commit()
            raise CustomException(status_code=400, message="未註冊的帳號")
        # Inactive Account
        if not user.first().is_active:
            login_hist = LoginHist(account=request.account.lower(),
                                   status="Inactive Account")
            db.add(login_hist)
            db.commit()
            raise CustomException(status_code=400, message="該帳號未被啟用")
        # Invalid Password
        if not Hasher.verify_password(request.password, user.first().hashed_password):
            login_hist = LoginHist(account=request.account.lower(),
                                   status="Invalid Password")
            db.add(login_hist)
            db.commit()
            raise CustomException(status_code=400, message="密碼錯誤")
        # Login Success
        login_hist = LoginHist(account=request.account.lower(),
                               status="Login Success")
        db.add(login_hist)
        db.commit()
        return user.first()

    except OperationalError as e:
        logger.error("login db error:{}".format(e))
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")


def add_vote_counter(db: Session, account: str):
    try:
        db.query(Account).filter(Account.account == account).update({'vote_counter': Account.vote_counter + 1})
        db.commit()
    except OperationalError:
        raise CustomException(status_code=424, message="DB error")


def check_if_admin(db: Session, account: str):
    try:
        user = db.query(Account).filter(Account.account == account)
        if user.first():
            return user.first().is_admin
        return False

    except OperationalError:

        raise CustomException(status_code=424, message="DB error")


def create_new_user(user: UserCreate, db: Session):
    try:
        user_query = db.query(Account).filter(Account.account == user.account.lower())
        if user_query.first():
            return '該帳號已註冊過'
        user_insert = Account(
            account=user.account.lower(),
            hashed_password=Hasher.get_password_hash(user.password),
            is_admin=user.is_admin,
            is_active=user.is_active,
        )
        db.add(user_insert)
        db.commit()
        db.refresh(user_insert)
        return '註冊成功'

    except OperationalError:

        raise CustomException(status_code=424, message="DB error")
