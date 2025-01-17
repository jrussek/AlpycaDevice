# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# app.py - Application module
#
# Python Interface Generator for AlpycaDevice
#
# Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
#
# Python Compatibility: Requires Python 3.7 or later
#
# Tools:
# ruamel.yaml (later pyYAML) https://yaml.readthedocs.io/en/latest/index.html
# munch to provide object (dotted) access to the dict made by pyYAML.
#
# -----------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2022-2023 Bob Denny
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------
# Edit History:
# 19-Jan-2023   rbd Initial edit
# 24-May-2023   rbd For upgraded templates with multi-device support
# 31-May-2023   Changes for Alpaca protocol conformance, and connected
# check in templates. Corrct capitalizaton of responder class names.
# Replace dunder naming with real names from YAML. Enhance to provide
# put paraeter handling with names and conversion functions that will
# raise an exception. Major upgrade to the templates.
# 08-Nov-2023   rbd GitHub #6 to_int and to_float are gone, remove from
#               import statements from shr in module template.
# 08-Nov-2023   rbd GitHub #8 Include property Connected/
# 08-Noc-2023   rbd Change other ommon property responder classes to
#               lower case andremove redundant ().
# 08-Nov-2023   rbd GitHub #9 Corrections to avoid adding fragments
#               of on_put() to existinv crrect on_put().
#

import yaml

cls_tmpl = '''@before(PreProcessRequest(maxdev))
class {mname}'''

mod_hdr = '''
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# {devname}.py - Alpaca API responders for {Devname}
#
# Author:   Your R. Name <your@email.org> (abc)
#
# -----------------------------------------------------------------------------
# Edit History:
#   Generated by Python Interface Generator for AlpycaDevice
#
# ??-???-????   abc Initial edit

from falcon import Request, Response, HTTPBadRequest, before
from logging import Logger
from shr import PropertyResponse, MethodResponse, PreProcessRequest, \\
                get_request_field, to_bool
from exceptions import *        # Nothing but exception classes

logger: Logger = None

# ----------------------
# MULTI-INSTANCE SUPPORT
# ----------------------
# If this is > 0 then it means that multiple devices of this type are supported.
# Each responder on_get() and on_put() is called with a devnum parameter to indicate
# which instance of the device (0-based) is being called by the client. Leave this
# set to 0 for the simple case of controlling only one instance of this device type.
#
maxdev = 0                      # Single instance

# -----------
# DEVICE INFO
# -----------
# Static metadata not subject to configuration changes
## EDIT FOR YOUR DEVICE ##
class {Devname}Metadata:
    """ Metadata describing the {Devname} Device. Edit for your device"""
    Name = 'Sample {Devname}'
    Version = '##DRIVER VERSION AS STRING##'
    Description = 'My ASCOM {Devname}'
    DeviceType = '{Devname}'
    DeviceID = '##GENERATE A NEW GUID AND PASTE HERE##' # https://guidgenerator.com/online-guid-generator.aspx
    Info = 'Alpaca Sample Device\\nImplements I{Devname}\\nASCOM Initiative'
    MaxDeviceNumber = maxdev
    InterfaceVersion = ##YOUR DEVICE INTERFACE VERSION##        # I{Devname}Vxxx

# --------------------
# RESOURCE CONTROLLERS
# --------------------

@before(PreProcessRequest(maxdev))
class action:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class commandblind:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class commandbool:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class commandstring:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class connected:
    def on_get(self, req: Request, resp: Response, devnum: int):
            # -------------------------------
            is_conn = ### READ CONN STATE ###
            # -------------------------------
        resp.text = PropertyResponse(is_conn, req).json)

    def on_put(self, req: Request, resp: Response, devnum: int):
        conn_str = get_request_field('Connected', req)
        conn = to_bool(conn_str)              # Raises 400 Bad Request if str to bool fails
        try:
            # --------------------------------
            ### CONNECT/DISCONNECT()PARAM) ###
            # --------------------------------
           resp.text = MethodResponse(req).json
        except Exception as ex:
            DriverException(0x500, '{Devname}.{Memname} failed', ex)).json

@before(PreProcessRequest(maxdev))
class description:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse({Devname}Metadata.Description, req).json

@before(PreProcessRequest(maxdev))
class driverinfo:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse({Devname}Metadata.Info, req).json

@before(PreProcessRequest(maxdev))
class interfaceversion:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse({Devname}Metadata.InterfaceVersion, req).json

@before(PreProcessRequest(maxdev))
class driverversion():
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse({Devname}Metadata.Version, req).json

@before(PreProcessRequest(maxdev))
class name():
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse({Devname}Metadata.Name, req).json

@before(PreProcessRequest(maxdev))
class supportedactions:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse([], req).json  # Not PropertyNotImplemented

'''
cls_tmpl = '''@before(PreProcessRequest(maxdev))
class {memname}:

'''

get_tmpl = '''    def on_get(self, req: Request, resp: Response, devnum: int):
        if not ##IS DEV CONNECTED##:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # ----------------------
            val = ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, '{Devname}.{Memname} failed', ex)).json

'''

put_tmpl = '''    def on_put(self, req: Request, resp: Response, devnum: int):
        if not ## IS DEV CONNECTED ##:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return{GETPARAMS}
        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, '{Devname}.{Memname} failed', ex)).json

'''

params_tmpl_bool = '''
        {param}str = get_request_field('{Param}', req)      # Raises 400 bad request if missing
        {param} = to_bool({param}str)                       # Same here
'''

params_tmpl_num = '''
        {param}str = get_request_field('{Param}', req)      # Raises 400 bad request if missing
        try:
            {param} = {cvtfunc}({param}str)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'{Param} " + {param}str + " not a valid number.')).json
            return
'''


def main():
    with open('AlpacaDeviceAPI_v1.yaml') as f:
        toptree = yaml.safe_load(f)

    seendevs = []
    mf = None
    for path, meths in toptree['paths'].items():
        print(f'{path}')
        if(path.startswith('/{device_type}')):
            continue
        bits = path.split('/')
        devname = bits[1]
        Devname = devname.title()
        if not devname in seendevs:
            if not mf is None and not mf.closed:
                mf.close
            mf = open(f'{devname}.py', 'w')
            temp = mod_hdr.replace('{devname}', devname)
            mf.write(temp.replace('{Devname}', Devname))
            seendevs.append(devname)
        memname = bits[3]
        Memname = memname.title()
        mf.write(cls_tmpl.replace('{memname}', memname))
        for meth, meta in meths.items():
            if meth == 'get':
                temp = get_tmpl.replace('{Devname}', Devname)
                mf.write(temp.replace('{Memname}', Memname))
            else:
                temp = put_tmpl.replace('{Devname}', Devname)
                temp = temp.replace('{Memname}', Memname)
                # Create code for getting and converting prameters
                # Please don't laugh
                getparams = ''
                if 'content' in  meths['put']['requestBody']:
                    for param in meths['put']['requestBody']['content']['application/x-www-form-urlencoded']['schema']['allOf'][1]['properties'].items():
                        ptemp = params_tmpl_num
                        ptemp = ptemp.replace('{param}', param[0].lower())    # Parameter name
                        ptemp = ptemp.replace('{Param}', param[0])
                        ptype = param[1]['type']
                        if ptype == 'boolean':
                            ptemp = params_tmpl_bool
                            ptemp = ptemp.replace('{param}', param[0].lower())      # Parameter name
                            ptemp = ptemp.replace('{Param}', param[0])
                        if ptype == 'integer':
                            ptemp = params_tmpl_num
                            ptemp = ptemp.replace('{param}', param[0].lower())      # Parameter name
                            ptemp = ptemp.replace('{Param}', param[0])
                            ptemp = ptemp.replace('{cvtfunc}', 'int')
                            ptemp += '        ### RANGE CHECK AS NEEDED ###          # Raise Alpaca InvalidValueException with details!'
                        if ptype == 'number':
                            ptemp = params_tmpl_num
                            ptemp = ptemp.replace('{param}', param[0].lower())      # Parameter name
                            ptemp = ptemp.replace('{Param}', param[0])
                            ptemp = ptemp.replace('{cvtfunc}', 'float')
                            ptemp += '        ### RANGE CHECK AS NEEDED ###         # Raise Alpaca InvalidValueException with details!'
                        getparams += ptemp
                    #mf.write('#------ 1 ------\n')                                  # Direct RequestBody with parameters
                    mf.write (temp.replace('{GETPARAMS}', getparams))
                elif '$ref' in  meths['put']['requestBody']:
                    ref = meths['put']['requestBody']['$ref']
                    if ref != '#/components/requestBodies/putStandardClientParameters':
                        content = toptree['components']['requestBodies'][ref.split('/')[3]]['content']
                        for param in content['application/x-www-form-urlencoded']['schema']['allOf'][1]['properties'].items():
                            ptemp = ptemp.replace('{param}', param[0].lower())      # Parameter name
                            ptemp = ptemp.replace('{Param}', param[0])
                            ptype = param[1]['type']
                            if ptype == 'boolean':
                                ptemp = params_tmpl_bool
                                ptemp = ptemp.replace('{param}', param[0].lower())  # Parameter name
                                ptemp = ptemp.replace('{Param}', param[0])
                            if ptype == 'integer':
                                ptemp = params_tmpl_num
                                ptemp = ptemp.replace('{param}', param[0].lower())  # Parameter name
                                ptemp = ptemp.replace('{Param}', param[0])
                                ptemp = ptemp.replace('{cvtfunc}', 'int')
                                ptemp += '        ### RANGE CHECK AS NEEDED ###       # Raise Alpaca InvalidValueException with details!'
                            if ptype == 'number':
                                ptemp = params_tmpl_num
                                ptemp = ptemp.replace('{param}', param[0].lower())  # Parameter name
                                ptemp = ptemp.replace('{Param}', param[0])
                                ptemp = ptemp.replace('{cvtfunc}', 'int')
                                ptemp += '        ### RANGE CHECK AS NEEDED ###       # Raise Alpaca InvalidValueException with details!'
                            getparams += ptemp
                        #mf.write('#------ 2 ------\n')                              # Reference with parameters
                        mf.write (temp.replace('{GETPARAMS}', getparams))
                    else:
                        #mf.write('#------ 3 ------\n')                              # Reference but no parameters
                        mf.write (temp.replace('{GETPARAMS}', ''))                  # Remove substitution token

    mf.close()

    print('end')


# ========================
if __name__ == '__main__':
    main()
# ========================
