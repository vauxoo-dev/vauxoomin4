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

from openerp import tools
from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import openerp
import os
import commands
from bzrlib import repository,  branch,  workingtree,  info, status, log


class branch_info_line(osv.osv_memory):

    '''Show info by branch and you can do pull from here'''

    _name = 'branch.info.line'
    _columns = {
        'logs': fields.text('Info', help='This field will be used to show '
                            'specific info branch like log and '
                            'diff or other special info'),
        'path': fields.char('Path', 500,
                            help='Complete branch path in server'),
        'revid': fields.char('Revid', 500, help='Revid for this branch '),
        'parent': fields.char('Parent', 500, help='This is the parent '
                              'branch from get pull'),
        'revno': fields.integer('Revno', help='Branch revno'),
        'name': fields.char('Name', 20, help='Branch Name'),
        'st':fields.selection([('ok','Commited'),('notb','Not Branch'),
                               ('uncommited','Uncommited')],
                               help='True if this branch have diff '
                             'without commiter'), 
        'color':fields.function(_get_color, method=True,
                                string='Color',type='integer',
                                help='Color used in kanban view'), 

    }
    
