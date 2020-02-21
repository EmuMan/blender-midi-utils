import math
import mido
import bpy

def add_empty(location, name):
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=location)
    obj = bpy.context.object
    obj.name = name
    return obj

def add_keyboard(name, start_note, length, location, x_distance=1.0, y_distance=1.0, z_distance=0.3, linear=False):
    layout = "wbwbwwbwbwbw"
    l_index = 0
    x_disp = 0.0
    y_disp = 0.0
    z_disp = 0.0
    collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(collection)
    for i in range(start_note+length):
        if i >= start_note:
            if not linear:
                y_disp = y_distance if layout[l_index] == "b" else 0.0
                z_disp = z_distance if layout[l_index] == "b" else 0.0
            obj = add_empty((location[0] + x_disp, location[1] + y_disp, location[2] + z_disp), "{}_{}".format(name, str(i)))
            bpy.ops.collection.objects_remove_all()
            bpy.data.collections[name].objects.link(obj)
            if linear:
                x_disp += x_distance
            else:
                x_disp += x_distance if (layout[l_index] == "w" and layout[(l_index+1)%12] == "w") else (x_distance / 2)
        l_index = (l_index + 1) % 12

def time_until_next_note(midi, index, return_note=False):
    i = index + 1
    total_time = 0.0
    try:
        while midi[i].type != "note_on":
            total_time += midi[i].time
            i += 1
    except IndexError:
        return midi[i].note if return_note else total_time
    return midi[i].note if return_note else total_time + midi[i].time

def get_tempo(midi):
    for msg in midi:
        if msg.type == "set_tempo":
            return msg.tempo
    return 120

def flatten_values(vals, limit):
    if sum(vals) < limit:
        return vals
    elif limit < vals[1] * 2:
        return (limit / 2, limit / 2)
    else:
        return (limit - vals[1], vals[1])
    
def set_vector(v, l, offset=None):
    if len(l) >= 1:
        v.x = (offset.x if offset else 0.0) + l[0]
    if len(l) >= 2:
        v.y = (offset.y if offset else 0.0) + l[1]
    if len(l) >= 3:
        v.z = (offset.z if offset else 0.0) + l[2]
    
class MidiKeyframes:
    
    def __init__(self, fname, track=1):
        self.fname = fname
        self.midi_obj = mido.MidiFile(fname)
        self.tempo = get_tempo(self.midi_obj)
        self.ppq = self.midi_obj.ticks_per_beat
        self.midi = list(self.midi_obj.tracks[track])
        print(self.midi)
        self.collection_name = None
        self.keys = None
        self.offset = None
        
    def general_application(self, obj, aspect, aspect_name, rest, strike, anticipation, delay, strike_time, release_time):
        if not self.offset:
            self.offset = obj.location.copy()
        fps = bpy.context.scene.render.fps
        current_time = delay
        last_time = current_time
        rs_diff = [rest[i] - strike[i] for i in range(len(rest))]
        if anticipation:
            anticipate_vals = [rest[i] + rs_diff[i] * anticipation for i in range(len(rest))]
        offset = self.get_offset(time_until_next_note(self.midi, 0, return_note=True)) if aspect_name == "location" else None
        set_vector(aspect, rest, offset)
        obj.keyframe_insert(aspect_name, frame=(max(delay - strike_time, 0))*fps)
        for i, msg in enumerate(self.midi):
            current_time += mido.tick2second(msg.time, self.ppq, self.tempo)
            if msg.type == "note_on":
                print(msg)
                offset = self.get_offset(msg.note) if aspect_name == "location" else None
                if current_time - last_time > release_time + strike_time:
                    # need to add another keyframe to ensure snappyness
                    set_vector(aspect, rest, offset)
                    obj.keyframe_insert(aspect_name, frame=(current_time-strike_time)*fps)
                print(time_until_next_note(self.midi, i), self.ppq, self.tempo)
                next_note_time = mido.tick2second(time_until_next_note(self.midi, i), self.ppq, self.tempo)
                print(next_note_time)
                rel_disp, att_disp = flatten_values((release_time, strike_time), next_note_time)
                if anticipation:
                    set_vector(aspect, anticipate_vals, offset)
                    obj.keyframe_insert(aspect_name, frame=(current_time-att_disp/2)*fps)
                set_vector(aspect, strike, offset)
                obj.keyframe_insert(aspect_name, frame=current_time*fps)
                set_vector(aspect, rest, offset)
                obj.keyframe_insert(aspect_name, frame=(current_time + rel_disp)*fps)
                last_time = current_time
                
    def set_rotation(self, rest, strike, anticipation=1.0, delay=1.0, strike_time=0.2, release_time=0.4):
        obj = bpy.context.object
        self.general_application(obj, obj.rotation_euler, "rotation_euler", [math.radians(d) for d in rest], [math.radians(d) for d in strike], anticipation, delay, strike_time, release_time)
    
    def set_location(self, rest, strike, anticipation=None, delay=1.0, strike_time=0.2, release_time=0.4):
        obj = bpy.context.object
        self.general_application(obj, obj.location, "location", rest, strike, anticipation, delay, strike_time, release_time)
    
    def set_keys(self, collection):
        self.collection_name = collection.name
        self.keys = {}
        for obj in collection.objects:
            self.keys[obj.name] = obj
            
    def get_offset(self, note):
        if self.keys:
            try:
                return self.keys["{}_{}".format(self.collection_name, str(note))].location
            except KeyError:
                pass
        return self.offset
        
    def prime_offset(self):
        self.offset = bpy.context.object.location.copy()