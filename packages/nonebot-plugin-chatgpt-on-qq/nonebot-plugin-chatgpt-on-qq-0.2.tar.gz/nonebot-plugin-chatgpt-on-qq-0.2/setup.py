#!/usr/bin/env python
# coding:utf-8

from setuptools import find_packages, setup

setup(
    name='nonebot-plugin-chatgpt-on-qq',
    version='0.2',
    description='具有多对话功能的chatGPT聊天插件',
    long_description=open('README.rst').read(),
    author='颜曦',
    author_email='424504326@qq.com',
    maintainer='颜曦',
    maintainer_email='424504326@qq.com',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/Suxmx/nonebot_plugin_chatgpt_turbo_on_qq',
    license='BSD License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)