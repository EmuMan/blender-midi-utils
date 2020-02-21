bl_info = {
    "name": "Midi Utils",
    "description": "Utilities for converting MIDI data into keyframe animation",
    "author": "EmuMan",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "3D View > MIDI Utils",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Animation"
}

import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )
from bpy.utils import register_class, unregister_class

from .properties import GeneralProperties, KeyframePanelProperties, MidiLocProperties, MidiRotProperties, KeyboardProperties
from .utils import MidiKeyframes, add_keyboard

class CreateLocKeyframes(Operator):
    bl_label = "Create Keyframes"
    bl_idname = "wm.create_loc_keyframes"

    def execute(self, context):
        scene = context.scene
        tool = scene.midi_loc_tool
        general_tool = scene.midi_general_tool

        mkf = MidiKeyframes(str(general_tool.midi_filepath), general_tool.track)
        mkf.prime_offset()
        try:
            collection = bpy.data.collections[str(tool.keyboard_collection)]
            mkf.set_keys(collection)
        except KeyError:
            pass
        mkf.set_location(tuple(tool.rest_pos), tuple(tool.strike_pos),
                         (tool.anticipation if tool.anticipation != 0.0 else None),
                         tool.delay, tool.attack_time, tool.release_time)

        return {"FINISHED"}

class CreateRotKeyframes(Operator):
    bl_label = "Create Keyframes"
    bl_idname = "wm.create_rot_keyframes"

    def execute(self, context):
        scene = context.scene
        tool = scene.midi_rot_tool
        general_tool = scene.midi_general_tool

        mkf = MidiKeyframes(str(general_tool.midi_filepath), general_tool.track)
        mkf.set_rotation(tuple(tool.rest_rot), tuple(tool.strike_rot),
                         (tool.anticipation if tool.anticipation != 0.0 else None),
                         tool.delay, tool.attack_time, tool.release_time)

        return {"FINISHED"}

class CreateKeyboard(Operator):
    bl_label = "Create Keyboard"
    bl_idname = "wm.create_keyboard"

    def execute(self, context):
        scene = context.scene
        tool = scene.keyboard_tool
        x_d, y_d, z_d = tuple(tool.displacements)
        add_keyboard(tool.collection_name, tool.start_note, tool.length, (0,0,0), x_d, y_d, z_d, tool.linear)

        return {"FINISHED"}

class GeneralPanel(Panel):
    bl_label = "General"
    bl_idname = "OBJECT_PT_midi_general"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MIDI Utils"
    bl_context = "objectmode"

    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        tool = scene.midi_general_tool

        layout.prop(tool, "midi_filepath")
        layout.prop(tool, "track")

class KeyframesPanel(Panel):
    bl_label = "Keyframes"
    bl_idname = "OBJECT_PT_midi_keyframes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MIDI Utils"
    bl_context = "objectmode"

    @classmethod
    def poll(cls, context):
        return context.object != None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        tool = scene.midi_keyframe_tool
        loc_tool = scene.midi_loc_tool
        rot_tool = scene.midi_rot_tool

        layout.label(text="Keyframe type:")
        layout.prop(tool, "keyframe_type", text="")
        layout.separator()

        if tool.keyframe_type == "loc":
            layout.prop(loc_tool, "keyboard_collection")
            layout.prop(loc_tool, "rest_pos")
            layout.prop(loc_tool, "strike_pos")
            layout.prop(loc_tool, "anticipation")
            layout.prop(loc_tool, "attack_time")
            layout.prop(loc_tool, "release_time")
            layout.prop(loc_tool, "delay")
            layout.operator("wm.create_loc_keyframes")
        else:
            layout.prop(rot_tool, "rest_rot")
            layout.prop(rot_tool, "strike_rot")
            layout.prop(rot_tool, "anticipation")
            layout.prop(rot_tool, "attack_time")
            layout.prop(rot_tool, "release_time")
            layout.prop(rot_tool, "delay")
            layout.operator("wm.create_rot_keyframes")

class CreateKeyboardPanel(Panel):
    bl_label = "Create Keyboard"
    bl_idname = "OBJECT_PT_create_keyboard"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MIDI Utils"
    bl_context = "objectmode"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        tool = scene.keyboard_tool

        layout.prop(tool, "collection_name")
        layout.prop(tool, "start_note")
        layout.prop(tool, "length")
        layout.prop(tool, "displacements")
        layout.prop(tool, "linear")
        layout.operator("wm.create_keyboard")

classes = (
    GeneralProperties,
    KeyframePanelProperties,
    MidiLocProperties,
    MidiRotProperties,
    KeyboardProperties,
    CreateLocKeyframes,
    CreateRotKeyframes,
    CreateKeyboard,
    GeneralPanel,
    KeyframesPanel,
    CreateKeyboardPanel
)

def register():
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.midi_general_tool = PointerProperty(type=GeneralProperties)
    bpy.types.Scene.midi_keyframe_tool = PointerProperty(type=KeyframePanelProperties)
    bpy.types.Scene.midi_loc_tool = PointerProperty(type=MidiLocProperties)
    bpy.types.Scene.midi_rot_tool = PointerProperty(type=MidiRotProperties)
    bpy.types.Scene.keyboard_tool = PointerProperty(type=KeyboardProperties)

def unregister():
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.midi_general_tool
    del bpy.types.Scene.midi_keyframe_tool
    del bpy.types.Scene.midi_loc_tool
    del bpy.types.Scene.midi_rot_tool
    del bpy.types.Scene.keyboard_tool