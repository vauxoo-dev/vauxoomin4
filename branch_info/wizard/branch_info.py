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
        'path': fields.char('Path', 500,
                            help='Complete branch path in server'),
        'revid': fields.char('Revid', 500, help='Revid for this branch '),
        'parent': fields.char('Parent', 500, help='This is the parent '
                              'branch from get pull'),
        'revno': fields.integer('Revno', help='Branch revno'),
        'name': fields.char('Name', 20, help='Branch Name'),
        'info_id': fields.many2one('branch.info', 'Branch'),
        'st': fields.boolean('Status', help='True if this branch have diff '
                             'without commiter'),
    }

    def show_log(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        r = False
        b = False
        w = False
        line_brw = context.get('ids', False) and self.browse(cr, uid,
                                                             context.get(
                                                                 'ids'),
                                                             context=context)
        st = os.popen('bzr log -l 5 --show-ids --include-merged %s/'
                      % (line_brw and
                         line_brw.path))
        res = {
            'logs': ''.join(st.readlines()),
            'change_id': line_brw.info_id.id,
        }
        res_ids = self.pool.get('branch.info').create(cr, uid, res)
        obj_model = self.pool.get('ir.model.data')
        model_data_ids = obj_model.search(
            cr, uid, [('model', '=', 'ir.ui.view'),
                      ('name', '=', 'branchinfo_form_log')])
        resource_id = obj_model.read(cr, uid,
                                     model_data_ids,
                                     fields=['res_id'])[0]['res_id']
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'branch.info',
            'views': [(resource_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'inline',
            'res_id': res_ids,
            'context': context,
        }

    def show_ch(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        addons_path = openerp.conf.addons_paths
        r = False
        b = False
        w = False
        lines = []
        line_brw = context.get('ids', False) and self.browse(cr, uid,
                                                             context.get(
                                                                 'ids'),
                                                             context=context)
        try:
            r = repository.Repository.open(line_brw and line_brw.path)
            b = branch.Branch.open(line_brw and line_brw.path)
            w = workingtree.WorkingTree.open(line_brw and line_brw.path)
        except:
            pass
        st = False
        if r and b and w:
            status.show_tree_status(w, to_file=open('/tmp/status', 'w'))
            st = commands.getoutput('less /tmp/status')
            commands.getoutput('rm /tmp/status')
        res = {
            'logs': st,
            'change_id': line_brw.info_id.id,
        }
        res_ids = self.pool.get('branch.info').create(cr, uid, res)
        obj_model = self.pool.get('ir.model.data')
        model_data_ids = obj_model.search(cr, uid, [(
            'model', '=', 'ir.ui.view'), ('name', '=', 'branchinfo_form_log')])
        resource_id = obj_model.read(
            cr, uid, model_data_ids, fields=['res_id'])[0]['res_id']
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'branch.info',
            'views': [(resource_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'inline',
            'res_id': res_ids,
            'context': context,
        }


class branch_info(osv.osv_memory):

    '''Show revno info of all branch in your servers, loaded in openerp'''

    def is_branch(self, cr, uid, ids, path, context=None):
        ''' Check if any path is a branch
            return branch path or False if not a branch'''
        if context is None:
            context = {}
        if '.bzr' in os.listdir(path):
            return path
        else:
            up_level = os.path.dirname(path)
            if '.bzr' in os.listdir(up_level):
                return up_level

        return False

    def load(self, cr, uid, ids, fields, context=None):
        '''Overwrite default_get method to add branch description'''
        if context is None:
            context = {}
        if context.get('stop', False):
            return {}
        addons_path = openerp.conf.addons_paths
        msg = '''
        <table border border="1">

        <tr>
     <td>Name</td> <td>Path</td> <td>Revno</td> <td>Revid</td> <td>Parent</td>
        </tr>
        <tr>'''
        lines = []
        for path in addons_path:
            r = False
            b = False
            w = False
            is_branch = False
            try:
                is_branch = self.is_branch(cr, uid, ids, path, context)
                if is_branch:
                    r = repository.Repository.open(is_branch)
                    b = branch.Branch.open(is_branch)
                    w = workingtree.WorkingTree.open(is_branch)
            except:
                pass

            if r and b and w:
                status.show_tree_status(w, to_file=open('/tmp/status', 'w'))
                revno = b.revno()
                name = b.nick
                parent = b.get_parent()
                revd = b.last_revision_info()[1]
                st = commands.getoutput('cat /tmp/status') and True or False
                msg = msg + '''\n
                        <tr>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <tr> ''' % (name, is_branch, revno, revd, parent)

                lines.append((0, 0, {'name': name,
                                     'revid': revd,
                                     'parent': parent,
                                     'revno': revno,
                                     'st': st,
                                     'path': is_branch
                                     }))
            else:
                revno = 0
                name = path.split('/')[-1]
                parent = False
                revd = False
                st = False
                msg = msg + '''\n
                        <tr>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <tr> ''' % (name, path, revno, revd, parent)

                lines.append((0, 0, {'name': name,
                                     'revid': revd,
                                     'parent': parent,
                                     'revno': revno,
                                     'st': st,
                                     'path': path
                                     }))

        msg = msg + '''\n
                   </tr>
                   </table>
                   '''
        res = {'branch_info': msg,
               'jose_way': True,
               'line_ids': lines,
               'load': True,
               }

        try:
            commands.getoutput('rm /tmp/status')
        except:
            pass

        res_ids = self.pool.get('branch.info').create(cr, uid, res)
        obj_model = self.pool.get('ir.model.data')
        model_data_ids = obj_model.search(
            cr, uid, [('model', '=', 'ir.ui.view'),
                      ('name', '=', 'branchinfo_form')])
        resource_id = obj_model.read(cr, uid, model_data_ids,
                                     fields=['res_id'])[0]['res_id']
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'branch.info',
            'views': [(resource_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'inline',
            'res_id': res_ids,
            'context': {'stop': True},
        }

    _name = 'branch.info'

    _columns = {

        'logs': fields.text('Info', help='This field will be used to show '
                            'specific info branch like log and '
                            'diff or other special info'),
        'jose_way': fields.boolean('Jose way', help='Check if you want see '
                                   'the jose did'),
        'load': fields.boolean('Load', help='Use to verifie if you load '
                               'the info branch'),
        'nhomar_way': fields.boolean('Nhomar way', help='Check if you want '
                                     'see the nhomar concept '
                                     ),
        'branch_info': fields.html('Branchs info', help='Show revno info '
                                   'by branch'),
        'line_ids': fields.one2many('branch.info.line',
                                    'info_id',
                                    'Lines', help='Show revno by branch '
                                    'and you can do pull by '
                                    'line'),
        'change_id': fields.integer('Change_id', help='Ids used to windows '
                                    'change'),

    }
    _defaults = {
        'jose_way': True,
    }

    def back_windows(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        wz_brw = context.get('ids', False) and self.browse(cr, uid,
                                                           context.get('ids'),
                                                           context=context)
        obj_model = self.pool.get('ir.model.data')
        model_data_ids = obj_model.search(cr, uid, [(
            'model', '=', 'ir.ui.view'), ('name', '=', 'branchinfo_form')])
        resource_id = obj_model.read(
            cr, uid, model_data_ids, fields=['res_id'])[0]['res_id']
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'branch.info',
            'views': [(resource_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'inline',
            'res_id': wz_brw.change_id,
            'context': context,
        }
