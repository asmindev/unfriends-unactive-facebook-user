#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# author: zettamus
# github: zettamus

import requests


class Browser:
    def __init__(self):
        self.__req = requests.get
        self.__post = requests.post
        self.__cookies = {"cookie": None}

    @property
    def cookies(self):
        return "Cookies initialized"

    @cookies.setter
    def setkuki(self, kuki):
        self.__cookies = {"cookie": kuki}

    @cookies.getter
    def showkuki(self):
        return self.__cookies

    def get(self, url, host="https://mbasic.facebook.com"):
        try:
            if self.__cookies["cookie"] is None:
                raise ValueError("Please set your cookie!")
            return self.__req(
                host + check(url), headers=self.__cookies, cookies=self.__cookies
            )
        except requests.exceptions.ConnectionError as f:
            raise ConnectionError(str(f))

    def post(self, url, data, host="https://mbasic.facebook.com"):
        try:
            if self.__cookies["cookie"] is None:
                raise ValueError("Please set your cookie!")
            return self.__post(
                host + check(url),
                data=data,
                headers=self.__cookies,
                cookies=self.__cookies,
            )
        except requests.exceptions.ConnectionError as f:
            raise ConnectionError(str(f))


def check(url):
    try:
        return url if url.startswith("/") else "/" + url
    except AttributeError as f:
        raise ValueError(f"Invalid url : {str(f)} : {str(url)}")
