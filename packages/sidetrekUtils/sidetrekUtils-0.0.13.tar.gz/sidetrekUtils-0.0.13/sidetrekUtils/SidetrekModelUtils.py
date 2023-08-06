# -*- coding: utf-8 -*-

"""Sidetrek mlflow wrapper.
"""
# Simple calculator library
import mlflow


class ModelUtils:

    __TRACKING_URI = "https://mlflow.sidetrek.com/p"

    def __set_tracking_uri(self, url: str):
        # from self.__mflow import set_tracking_uri
        # self.__mflow.set_registry_uri
        if (url != self.__TRACKING_URI):
            raise Exception("Tracking uri can't be changed to " + url)

    def __init__(self):
        self.trackingUtil = mlflow
        self.trackingUtil.set_tracking_uri(self.__TRACKING_URI)

        # User should not change the tracking uri
        self.trackingUtil.set_tracking_uri = self.__set_tracking_uri


utils = ModelUtils()
