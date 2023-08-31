# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
import numpy as np

webserver = Flask(__name__)

@webserver.route("/")
def a():
    msg = "hello"
    
    return msg


webserver.run(host = '0.0.0.0', port = 2022)