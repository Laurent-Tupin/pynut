#-----------------------------------------------------------------
# Generic Lib
#-----------------------------------------------------------------
def os():
    try:    import os
    except  Exception as err:
        print('  IMPORT FAIL |os|, err:|{}|'.format(err))
        return None
    return os

def time():
    try:    import time
    except  Exception as err:
        print('  IMPORT FAIL |time|, err:|{}|'.format(err))
        return None
    return time

def sys():
    try:    import sys
    except  Exception as err:
        print('  IMPORT FAIL |sys|, err:|{}|'.format(err))
        return None
    return sys

def math():
    try:    import math
    except  Exception as err:
        print('  IMPORT FAIL |math|, err:|{}|'.format(err))
        return None
    return math

def collections():
    try:    import collections
    except  Exception as err:
        print('  IMPORT FAIL |collections|, err:|{}|'.format(err))
        return None
    return collections

def contextlib():
    try:    import contextlib
    except  Exception as err:
        print('  IMPORT FAIL |contextlib|, err:|{}|'.format(err))
        return None
    return contextlib

def threading():
    try:    import threading
    except  Exception as err:
        print('  IMPORT FAIL |threading|, err:|{}|'.format(err))
        return None
    return threading

def ThreadPoolExecutor():
    try:    from concurrent.futures import ThreadPoolExecutor
    except  Exception as err:
        print('  IMPORT FAIL |ThreadPoolExecutor|, err:|{}|'.format(err))
        return None
    return ThreadPoolExecutor

def as_completed():
    try:    from concurrent.futures import as_completed
    except  Exception as err:
        print('  IMPORT FAIL |as_completed|, err:|{}|'.format(err))
        return None
    return as_completed


#-----------------------------------------------------------------
# dataframe
#-----------------------------------------------------------------
def numpy():
    try:    import numpy
    except  Exception as err:
        print('  IMPORT FAIL |numpy|, err:|{}|'.format(err))
        return None
    return numpy

def pandas():
    try:    import pandas
    except  Exception as err:
        print('  IMPORT FAIL |pandas|, err:|{}|'.format(err))
        return None
    return pandas


#-----------------------------------------------------------------
# Date
#-----------------------------------------------------------------
def datetime():
    try:    import datetime
    except  Exception as err:
        print('  IMPORT FAIL |datetime|, err:|{}|'.format(err))
        return None
    return datetime

def BDay():
    try:    from pandas.tseries.offsets import BDay
    except  Exception as err:
        print('  IMPORT FAIL |BDay|, err:|{}|'.format(err))
        return None
    return BDay

def relativedelta():
    try:    from dateutil.relativedelta import relativedelta
    except  Exception as err:
        print('  IMPORT FAIL |relativedelta|, err:|{}|'.format(err))
        return None
    return relativedelta


#-----------------------------------------------------------------
# DB
#-----------------------------------------------------------------
def pyodbc():
    try:    import pyodbc
    except  Exception as err:
        print('  IMPORT FAIL |pyodbc|, err:|{}|'.format(err))
        return None
    return pyodbc

def sqlite3():
    try:    import sqlite3
    except  Exception as err:
        print('  IMPORT FAIL |sqlite3|, err:|{}|'.format(err))
        return None
    return sqlite3

def sqlalchemy():
    try:    import sqlalchemy
    except  Exception as err:
        print('  IMPORT FAIL |sqlalchemy|, err:|{}|'.format(err))
        return None
    return sqlalchemy


#-----------------------------------------------------------------
# HTML
#-----------------------------------------------------------------
def re():
    try:    import re
    except  Exception as err:
        print('  IMPORT FAIL |re|, err:|{}|'.format(err))
        return None
    return re

def requests():
    try:    import requests
    except  Exception as err:
        print('  IMPORT FAIL |requests|, err:|{}|'.format(err))
        return None
    return requests

def BeautifulSoup():
    try:    from bs4 import BeautifulSoup
    except  Exception as err:
        print('  IMPORT FAIL |BeautifulSoup|, err:|{}|'.format(err))
        return None
    return BeautifulSoup

def urlopen():
    try:    from urllib.request import urlopen
    except  Exception as err:
        print('  IMPORT FAIL |urlopen|, err:|{}|'.format(err))
        return None
    return urlopen

def urlretrieve():
    try:    from urllib.request import urlretrieve
    except  Exception as err:
        print('  IMPORT FAIL |urlretrieve|, err:|{}|'.format(err))
        return None
    return urlretrieve

def unicodedata():
    try:    import unicodedata
    except  Exception as err:
        print('  IMPORT FAIL |unicodedata|, err:|{}|'.format(err))
        return None
    return unicodedata

def selenium():
    try:    import selenium
    except  Exception as err:
        print('  IMPORT FAIL |selenium|, err:|{}|'.format(err))
        return None
    return selenium


#-----------------------------------------------------------------
# FTP
#-----------------------------------------------------------------
def ftplib():
    try:    import ftplib
    except  Exception as err:
        print('  IMPORT FAIL |ftplib|, err:|{}|'.format(err))
        return None
    return ftplib

def SSLSocket():
    try:    from ssl import SSLSocket
    except  Exception as err:
        print('  IMPORT FAIL |SSLSocket|, err:|{}|'.format(err))
        return None
    return SSLSocket

def paramiko():
    try:    import paramiko
    except  Exception as err:
        print('  IMPORT FAIL |paramiko|, err:|{}|'.format(err))
        return None
    return paramiko

#-----------------------------------------------------------------
# OUTLOOK
#-----------------------------------------------------------------
def Credentials():
    try:    from exchangelib import Credentials
    except  Exception as err:
        print('  IMPORT FAIL |Credentials|, err:|{}|'.format(err))
        return None
    return Credentials

def Account():
    try:    from exchangelib import Account
    except  Exception as err:
        print('  IMPORT FAIL |Account|, err:|{}|'.format(err))
        return None
    return Account

def Configuration():
    try:    from exchangelib import Configuration
    except  Exception as err:
        print('  IMPORT FAIL |Configuration|, err:|{}|'.format(err))
        return None
    return Configuration

def DELEGATE():
    try:    from exchangelib import DELEGATE
    except  Exception as err:
        print('  IMPORT FAIL |DELEGATE|, err:|{}|'.format(err))
        return None
    return DELEGATE

def FileAttachment():
    try:    from exchangelib import FileAttachment
    except  Exception as err:
        print('  IMPORT FAIL |FileAttachment|, err:|{}|'.format(err))
        return None
    return FileAttachment

def EWSTimeZone():
    try:    from exchangelib import EWSTimeZone
    except  Exception as err:
        print('  IMPORT FAIL |EWSTimeZone|, err:|{}|'.format(err))
        return None
    return EWSTimeZone

def EWSDateTime():
    try:    from exchangelib import EWSDateTime
    except  Exception as err:
        print('  IMPORT FAIL |EWSDateTime|, err:|{}|'.format(err))
        return None
    return EWSDateTime


#-----------------------------------------------------------------
# Files
#-----------------------------------------------------------------
def shutil():
    try:    import shutil
    except  Exception as err:
        print('  IMPORT FAIL |shutil|, err:|{}|'.format(err))
        return None
    return shutil

def psutil():
    try:    import psutil
    except  Exception as err:
        print('  IMPORT FAIL |psutil|, err:|{}|'.format(err))
        return None
    return psutil

def glob():
    try:    import glob
    except  Exception as err:
        print('  IMPORT FAIL |glob|, err:|{}|'.format(err))
        return None
    return glob

def csv():
    try:    import csv
    except  Exception as err:
        print('  IMPORT FAIL |csv|, err:|{}|'.format(err))
        return None
    return csv

def copy():
    try:    import copy
    except  Exception as err:
        print('  IMPORT FAIL |copy|, err:|{}|'.format(err))
        return None
    return copy

def pythoncom():
    try:    import pythoncom
    except  Exception as err:
        print('  IMPORT FAIL |pythoncom|, err:|{}|'.format(err))
        return None
    return pythoncom

def win32():
    try:    import win32com.client as win32
    except  Exception as err:
        print('  IMPORT FAIL |win32|, err:|{}|'.format(err))
        return None
    return win32

def ZipFile():
    try:    from zipfile import ZipFile
    except  Exception as err:
        print('  IMPORT FAIL |ZipFile|, err:|{}|'.format(err))
        return None
    return ZipFile

def xlwings():
    try:    import xlwings
    except  Exception as err:
        print('  IMPORT FAIL |xlwings|, err:|{}|'.format(err))
        return None
    return xlwings

def xlsxwriter():
    try:    import xlsxwriter
    except  Exception as err:
        print('  IMPORT FAIL |xlsxwriter|, err:|{}|'.format(err))
        return None
    return xlsxwriter

def xlrd():
    try:    import xlrd
    except  Exception as err:
        print('  IMPORT FAIL |xlrd|, err:|{}|'.format(err))
        return None
    return xlrd

def openpyxl():
    try:    import openpyxl
    except  Exception as err:
        print('  IMPORT FAIL |openpyxl|, err:|{}|'.format(err))
        return None
    return openpyxl

def openpyxl_styles():
    try:    import openpyxl.styles as openpyxl_styles
    except  Exception as err:
        print('  IMPORT FAIL |openpyxl_styles|, err:|{}|'.format(err))
        return None
    return openpyxl_styles

def openpyxl_Excel():
    try:    import openpyxl.reader.excel as openpyxl_Excel
    except  Exception as err:
        print('  IMPORT FAIL |openpyxl_Excel|, err:|{}|'.format(err))
        return None
    return openpyxl_Excel

def PageSetupProperties():
    try:    from openpyxl.worksheet.properties import PageSetupProperties
    except  Exception as err:
        print('  IMPORT FAIL |PageSetupProperties|, err:|{}|'.format(err))
        return None
    return PageSetupProperties

def NamedStyle():
    try:    from openpyxl.styles import NamedStyle
    except  Exception as err:
        print('  IMPORT FAIL |NamedStyle|, err:|{}|'.format(err))
        return None
    return NamedStyle

def Font():
    try:    from openpyxl.styles import Font
    except  Exception as err:
        print('  IMPORT FAIL |Font|, err:|{}|'.format(err))
        return None
    return Font

def PatternFill():
    try:    from openpyxl.styles import PatternFill
    except  Exception as err:
        print('  IMPORT FAIL |PatternFill|, err:|{}|'.format(err))
        return None
    return PatternFill

def colors():
    try:    from openpyxl.styles import colors
    except  Exception as err:
        print('  IMPORT FAIL |colors|, err:|{}|'.format(err))
        return None
    return colors

def Border():
    try:    from openpyxl.styles import Border
    except  Exception as err:
        print('  IMPORT FAIL |Border|, err:|{}|'.format(err))
        return None
    return Border

def Side():
    try:    from openpyxl.styles import Side # , Alignment, Color
    except  Exception as err:
        print('  IMPORT FAIL |Side|, err:|{}|'.format(err))
        return None
    return Side

