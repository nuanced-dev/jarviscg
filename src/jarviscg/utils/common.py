# Copyright [pythonJaRvis] [name of copyright owner]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os


def get_lambda_name(counter):
    return "<lambda{}>".format(counter)

def get_dict_name(counter):
    return "<dict{}>".format(counter)

def get_list_name(counter):
    return "<list{}>".format(counter)

def get_int_name(counter):
    return "<int{}>".format(counter)

def get_if_name(counter):
    return "<if{}>".format(counter)
def get_else_name(counter):
    return "<else{}>".format(counter)
def get_while_name(counter):
    return "<while{}>".format(counter)
def get_while_else_name(counter):
    return "<whileelse{}>".format(counter)
def get_scope_copy_name(counter):
    return "<copy{}>".format(counter)
def join_ns(*args):
    return ".".join([arg for arg in args])

def to_mod_name(name, package=None):
    return os.path.splitext(name)[0].replace("/", ".")

def get_suffix(first:str,second:str):
    if len(first) > len(second):
        first,second = second,first
    return second.replace(first,'')

def closure_2_parameter(a1,func):
    def closure(a2):
        return func(a1,a2)
    return closure
