# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2011 Vauxoo - http://www.vauxoo.com/
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
############################################################################
#    Coded by: moylop260 (moylop260@vauxoo.com)
############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "Get info of all branches in your instance",
    "version": "1.0",
    "author": "Vauxoo",
    "category": "Tecnhical Features",
    "description": """
This module is used to know state about your server instance,
it show information about all branches set in your addons_path config.

Features:

Add a new menu in technical information, it menu name is Branch Info, you
need technical permisions to can see,

This menu call an action windows that show a button with Load Info string,
press it to load information about your branchs set in your server
configuration.

This show the following info:
    - Name Branch
    - Absolute path branch
    - Last reviewer branch
    - Revno Branch
    - Parent branch from get pull

This information is show in colors, and each color has a meaning witch is:
    -Blue: If there are changes without commits in the branch
    -Red: If path is not a branch
    -Green: If all is correctly in this branch
    """,

    "website": "http://www.vauxoo.com/",
    "license": "AGPL-3",
    "depends": ["base"],
    "init_xml": [],
    "demo_xml": [],
    "css": ["static/src/css/*.css"],
    "update_xml": [
        'wizard/branch_info_view.xml',
    ],
    "installable": True,
    "active": False,
}
