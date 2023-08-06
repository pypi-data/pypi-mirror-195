# -*- coding: utf-8 -*-
'''Модели для работы с образами'''
from uuid import UUID
from enum import Enum
from datetime import datetime

from pydantic import Field

from ..base import ResponseWithMeta, BaseResponse, BaseData


class ImageStatus(str, Enum):
    '''Статус образа'''
    NEW = 'new'
    CREATED = 'created'
    FAILED = 'failed'
    DELETED = 'deleted'


class Image(BaseData):
    '''Модель образа'''
    id: UUID | str = Field(..., description='Уникальный идентификатор образа.')
    status: ImageStatus = Field(..., description='Статус образа.')
    created_at: datetime = Field(...,
                                 description='Дата и время создания образа.')
    deleted_at: datetime | None = None
    size: int = Field(..., description='Размер образа в мегабайтах.')
    name: str
    description: str = Field(..., description='Описание образа.')
    disk_id: int = Field(
        ..., description='Идентификатор связанного с образом диска.'
    )
    location: str | None = Field(
        None, description='Локация, в которой создан образ'
    )
    os: str
    progress: int


class ImagesArray(ResponseWithMeta):
    '''Модель ответа образов'''
    images: list[Image] = Field(..., description='Массив образов.')


class ImageResponse(BaseResponse):
    '''Модель ответа на создание образа'''
    image: Image = Field(..., description='Объект образа.')


class URLType(str, Enum):
    '''Тип URL'''
    TIMEWEB = 'timeweb'
    GOOGLE_DRIVE = 'google_drive'
    YANDEX = 'yandex'


class URLStatus(str, Enum):
    '''Статус URL'''
    PROCESS = 'process'
    FAILED = 'failed'
    FINISHED = 'finished'
    ALREADY_EXISTS = 'already_exists'


class Download(BaseData):
    '''Модель ссылки на загрузку'''
    id: UUID | str = Field(..., description='Уникальный идентификатор ссылки.')
    created_at: datetime = Field(
        ..., description='Дата и время создания ссылки.'
    )
    image: UUID | str = Field(..., description='Идентификатор образа.')
    type: URLType = Field(..., description='Тип ссылки.')
    url: str = Field(..., description='Ссылка на скачивание.')
    status: URLStatus = Field(..., description='Статус создания.')
    progress: int


class DownloadsArray(ResponseWithMeta):
    '''Модель ответа ссылок на загрузку'''
    downloads: list[Download] = Field(..., description='Массив ссылок.')


class DownloadResponse(BaseResponse):
    '''Модель ответа на создание ссылки на загрузку'''
    download: Download = Field(..., description='Объект ссылки на загрузку.')
