from setuptools import setup

setup(
name = "banksys",
author = "Akshat Sabharwal",
version = "1.3",
packages = ["banksys"],
author_email = "akshatsabharwal35@gmail.com",
description = "A system for Login and Sign Up with all the necessary functions such as sign_up() and login() with the support of MySql database",
install_requires = [
    'mysql.connector',
    'maskpass',
    'pyttsx3',
    'numpy',
    'SpeechRecognition'
]
)
