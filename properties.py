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

class GeneralProperties(PropertyGroup):

    midi_filepath: StringProperty(
        name = "MIDI File",
        description = "Choose a MIDI file:",
        default = "",
        maxlen = 1024,
        subtype = 'FILE_PATH'
    )

    track: IntProperty(
        name = "Track",
        description = "The track number of the MIDI data",
        default = 1,
        min = 1
    )

class KeyframePanelProperties(PropertyGroup):

    keyframe_type: EnumProperty(
        name = "Keyframe type:",
        description="The type of keyframe data to apply.",
        items=[ ('loc', "Location", ""),
                ('rot', "Rotation", "")
               ]
        )

class MidiLocProperties(PropertyGroup):

    keyboard_collection: StringProperty(
        name = "Keyboard",
        description = "Name of a keyboard collection to use",
        default = "",
        maxlen = 1024
    )
    
    rest_pos: FloatVectorProperty(
        name = "Rest position",
        description = "The x/y/z coordinates of the object's rest position",
        default = (0.0, 0.0, 0.0)
    )

    strike_pos: FloatVectorProperty(
        name = "Strike position",
        description = "The x/y/z coordinates of the object's strike position",
        default = (0.0, 0.0, 0.0)
    )

    attack_time: FloatProperty(
        name = "Attack time",
        description = "The time it takes an object to strike",
        default = 0.2,
        min = 0.0,
        max = 10.0
    )

    release_time: FloatProperty(
        name = "Release time",
        description = "The time it takes an object to release",
        default = 0.4,
        min = 0.0,
        max = 10.0
    )

    delay: FloatProperty(
        name = "Delay",
        description = "The amount of time before the first strike",
        default = 1.0,
        min = 0.0
    )

    anticipation: FloatProperty(
        name = "Anticipation",
        description = "The amount of anticipation on the object's movements",
        default = 0.0,
        min = 0.0
    )

class MidiRotProperties(PropertyGroup):
    
    rest_rot: FloatVectorProperty(
        name = "Rest rotation",
        description = "The x/y/z euler values of the object's rest rotation",
        default = (0.0, 0.0, 0.0)
    )

    strike_rot: FloatVectorProperty(
        name = "Strike rotation",
        description = "The x/y/z euler values of the object's strike rotation",
        default = (0.0, 0.0, 0.0)
    )

    attack_time: FloatProperty(
        name = "Attack time",
        description = "The time it takes an object to strike",
        default = 0.2,
        min = 0.0,
        max = 10.0
    )

    release_time: FloatProperty(
        name = "Release time",
        description = "The time it takes an object to release",
        default = 0.4,
        min = 0.0,
        max = 10.0
    )

    delay: FloatProperty(
        name = "Delay",
        description = "The amount of time before the first strike",
        default = 1.0,
        min = 0.0
    )

    anticipation: FloatProperty(
        name = "Anticipation",
        description = "The amount of anticipation on the object's movements",
        default = 1.0,
        min = 0.0
    )

class KeyboardProperties(PropertyGroup):

    collection_name: StringProperty(
        name = "Collection name",
        description = "Name for the keyboard collection",
        default = "Keys",
        maxlen = 1024
    )

    start_note: IntProperty(
        name = "Start note",
        description = "MIDI value for the starting note",
        default = 60,
        min = 0,
        max = 131
    )

    length: IntProperty(
        name = "Length",
        description = "The length of the keyboard",
        default = 12,
        min = 1,
        max = 132
    )

    displacements: FloatVectorProperty(
        name = "Key displacements",
        description = "The x/y/z displacements of keys",
        default = (1.0, 1.5, 0.5)
    )

    linear: BoolProperty(
        name = "Linear",
        description = "Lines keys up in chromatic order rather than standard black/white",
        default = False
    )