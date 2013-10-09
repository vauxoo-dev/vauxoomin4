# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from openerp import modules, pooler, tools, addons
from openerp.osv import osv, fields
from openerp.tools.translate import _
import openerp
import os
import commands
import re
import sys
import jinja2
from pprint import pprint

INFO = '.*INFO '
ERROR = '.*ERROR '
WARNING = '.*WARNING '
PYTHON = '.*File '
TEST = '.*TEST'

class info_log_server(osv.TransientModel):

    '''Show info by branch and you can do pull from here'''

    _name = 'info.log.server'
    
    def RenderThings(self, Data):
        module_path = modules.get_module_path('log_info')
        templateLoader = jinja2.FileSystemLoader( searchpath="%s/static/src/xml" % module_path )
        templateEnv = jinja2.Environment( loader=templateLoader,
                extensions=['jinja2.ext.autoescape'] )
        templateEnv.globals['len'] = len
        TEMPLATE_FILE = "original_template.xml"
        template = templateEnv.get_template( TEMPLATE_FILE )
        outputText = template.render(warnings = Data[3],
            infos = Data[2], pythons = Data[1],
            tests = Data[3], errors = Data[0])
        open('%s/static/src/xml/log_info.xml' % module_path, 'w').write(outputText)
        return True

    def Parselog(self, logFilePath):

        errors = []
        infos = []
        warnings = []
        tests = []
        pythons = []
        logFile = open(logFilePath, 'r')
        F = logFile.xreadlines()
        for l in F:
            if re.match(INFO, l):
                infos.append(unicode(l))
            if re.match(WARNING, l):
                warnings.append(unicode(l))
            if re.match(TEST, l):
                tests.append(unicode(l))
            if re.match(ERROR, l):
                errors.append(unicode(l))
            if re.match(PYTHON, l):
                Text = l
                for k in F:
                    if re.match(PYTHON, k):
                        Text = Text + k
                    else:
                        pythons.append(unicode(Text))
                        break

        return errors, pythons, infos, warnings, tests

    def default_get(self, cr, uid, fields, context=None):
        '''Overwrite default_get method to add branch description'''
        if context is None:
            context = {}
        res = super(info_log_server, self).default_get(cr, uid, fields, context=context)
        log_file = openerp.tools.config.options.get('logfile',False)
        result = self.Parselog(log_file)
        self.RenderThings(result)
        
        return res

    _columns = {
            'name':fields.boolean('Dummy', help='Dummy Field'), 
            
            
            } 
