from setuptools import setup

setup(
name = "sqluser",
author = "Akshat Sabharwal",
version = "0.1",
packages = ["sqluser"],
author_email = "akshatsabharwal35@gmail.com",
description = "A system for Login and Sign Up with all the necessary functions such as sign_up() and login() with the support of MySql database",
install_requires = [
    'mysql.connector',
    'random',
    'maskpass',
    'secure-smtplib',
    'random2'
]
)
