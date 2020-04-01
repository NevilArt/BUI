############################################################################
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
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

bl_info = {
	"name": "BUI",
	"description": "BUI for Blender 2.80 ~ 2.83",
	"author": "Naser Merati (Nevil)",
	"version": (0, 1, 0, 20200401),
	"blender": (2, 80, 0),
	"location": "Python Script",
	"wiki_url": "https://github.com/NevilArt/BUI/wiki",
	"doc_url": "https://github.com/NevilArt/BUI/wiki",
	"tracker_url": "https://github.com/NevilArt/BUI/issues",
	"category": "Development"
}

import sys, os

path = os.path.dirname(os.path.realpath(__file__))
if path not in sys.path:
		sys.path.append(path)

import templates

def register():
	templates.register()

def unregister():
	if path not in sys.path:
		sys.path.remove(path)
	templates.unregister()

if __name__ == "__main__":
	register()