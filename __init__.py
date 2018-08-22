# -*-coding:utf-8 -*-
#
# Import the libraries we need

from auto_Test.auto_Test import base_Test
from auto_Test.auto_Test import Mytool
from auto_Test.auto_Test import platform_Test

__verison__ = "LDF1.0"

class auto_Test(base_Test, Mytool,platform_Test ):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

# class auto_Test(Mytool):
# 	ROBOT_LIBRARY_SCOPE = 'GLOBAL'


#class auto_Test(platform_Test):
#    ROBOT_LIBRARY_SCOPE = 'GLOBAL'