#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#======================= END GPL LICENSE BLOCK ========================

import bpy
import math
import bmesh
from mathutils.bvhtree import BVHTree

# Version History
# 1.0.0 - 2020-07-14: Initial version
# 1.0.1 - 2022-08-07: Misc formatting cleanup before uploading to GitHub.

bl_info = {
    "name": "Do Objects Intersect",
    "author": "Jeff Boller, VSB",
    "version": (1, 0, 1),
    "blender": (2, 93, 0),
    "location": "",
    "description": "This script will determine if any of the selected mesh objects intersect. " \
                   "To use this, simply select multiple mesh objects and then run the command that launches this code. " \
                   "Look in the Info window for a more detailed result. "\
                   "To run this, make a keyboard shortcut and put in this command: " \
                   "wm.do_objects_intersect " \
                   "Add-on code based partially on the code found here: https://blender.stackexchange.com/questions/71289/using-overlap-to-check-if-two-meshes-are-intersecting",
    "wiki_url": "https://github.com/sundriftproductions/blenderaddon-do-objects-intersect/wiki",
    "tracker_url": "https://github.com/sundriftproductions/blenderaddon-do-objects-intersect",
    "category": "3D View"}

class WM_OT_do_objects_intersect(bpy.types.Operator):
    bl_idname = 'wm.do_objects_intersect'
    bl_label = 'Check if selected objects intersect'
    bl_description = 'Call bpy.ops.wm.do_objects_intersect()'

    def ShowMessageBox(self, message='', title='', icon='INFO'):
        def draw(self, context):
            self.layout.label(text=message)

        bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

    def intersection_check(self, obj_list):
        objectsTouching = False
        # Check every object for intersection with every other object.
        for obj_now in obj_list:
            for obj_next in obj_list:
                print()
                if obj_now == obj_next:
                    continue

                # Create bmesh objects.
                bm1 = bmesh.new()
                bm2 = bmesh.new()

                # Fill bmesh data from objects.
                bm1.from_mesh(bpy.context.scene.objects[obj_now].data)
                bm2.from_mesh(bpy.context.scene.objects[obj_next].data)

                bm1.transform(bpy.context.scene.objects[obj_now].matrix_world)
                bm2.transform(bpy.context.scene.objects[obj_next].matrix_world)

                # Make BVH tree from BMesh of objects.
                obj_now_BVHtree = BVHTree.FromBMesh(bm1)
                obj_next_BVHtree = BVHTree.FromBMesh(bm2)

                # Get intersecting pairs
                inter = obj_now_BVHtree.overlap(obj_next_BVHtree)

                # If list is empty, no objects are touching.
                if inter != []:
                    self.report({'INFO'}, obj_now + " and " + obj_next + " intersect!")
                    objectsTouching = True
                else:
                    self.report({'INFO'}, obj_now + " and " + obj_next + " do NOT intersect!")

        return objectsTouching

    def execute(self, context):
        obj_list = []

        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                obj_list.append(obj.name)

        if len(obj_list) < 2:
            msg = 'Unable to check for intersections. You must select multiple mesh objects to see if they intersect.'
            self.report({'ERROR'}, msg)
            self.ShowMessageBox(msg, 'ERROR', 'ERROR')
            return {'CANCELLED'}

        # Run it!
        objectsTouching = self.intersection_check(obj_list)

        if (objectsTouching):
            self.ShowMessageBox('Objects DO intersect!', 'WARNING', 'ERROR')
        else:
            self.ShowMessageBox('Objects do NOT intersect.')

        return {'FINISHED'}

def register():
    bpy.utils.register_class(WM_OT_do_objects_intersect)

def unregister():
    bpy.utils.unregister_class(WM_OT_do_objects_intersect)

if __name__ == "__main__":
    register()
