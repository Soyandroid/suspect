from . import c2s
from . import sus

def sus_to_c2s(sus_objects, sus_ticks_per_measure = sus.SUS_TICKS_PER_MEASURE, c2s_ticks_per_measure = c2s.C2S_TICKS_PER_MEASURE):

    c2s_definitions = []
    c2s_notes = []

    def sus_to_c2s_ticks(ticks):
        scaled_ticks = int((ticks / sus_ticks_per_measure) * c2s_ticks_per_measure)
        return scaled_ticks

    for obj in sus_objects:
        if isinstance(obj, sus.ShortNote):
            if obj.note_type == sus.TapNoteType["TAP"]:
                note = c2s.TapNote()
            if obj.note_type == sus.TapNoteType["EXTAP"]:
                note = c2s.ChargeNote()
            if obj.note_type == sus.TapNoteType["FLICK"]:
                note = c2s.FlickNote()
            if obj.note_type == sus.TapNoteType["HELL"]:
                note = c2s.MineNote()
            if obj.note_type == sus.AirNoteType["UP"]:
                note = c2s.AirNote()
                note.isUp = True
                note.direction = 0
            if obj.note_type == sus.AirNoteType["UP_LEFT"]:
                note = c2s.AirNote()
                note.isUp = True
                note.direction = -1
            if obj.note_type == sus.AirNoteType["UP_RIGHT"]:
                note = c2s.AirNote()
                note.isUp = True
                note.direction = 1
            if obj.note_type == sus.AirNoteType["DOWN"]:
                note = c2s.AirNote()
                note.isUp = False
                note.direction = 0
            if obj.note_type == sus.AirNoteType["DOWN_LEFT"]:
                note = c2s.AirNote()
                note.isUp = False
                note.direction = -1
            if obj.note_type == sus.AirNoteType["DOWN_RIGHT"]:
                note = c2s.AirNote()
                note.isUp = False
                note.direction = 1

            note.lane = obj.lane
            note.width = obj.width
            note.measure = obj.measure
            note.tick = sus_to_c2s_ticks(obj.tick)

            c2s_notes.append(note)
            
        if isinstance(obj, sus.LongNote):
            if obj.note_type == sus.LongNoteType["END"]:
                # Ignore end notes, they're handled differently in c2s
                continue

            next_idx = obj.linked.index(obj) + 1
            if next_idx == len(obj.linked):
                print("WARNING: Channel ends with a non-END note, assuming intended END")
                continue

            next_obj = obj.linked[next_idx]
            if next_obj.note_kind != obj.note_kind:
                print("WARNING: Channel switches note kinds (goes from %s:%s to %s:%s at index %s) - Assuming intended END" % (obj.note_kind, obj.note_type, next_obj.note_kind, next_obj.note_type, next_idx))
                continue

            start_measure = obj.measure
            start_ticks = sus_to_c2s_ticks(obj.tick)
            end_measure = next_obj.measure
            end_ticks = sus_to_c2s_ticks(next_obj.tick)

            diff_ticks = ((end_measure - start_measure) * c2s_ticks_per_measure) + (end_ticks - start_ticks)

            if obj.note_kind == sus.LongNoteKind["SLIDE"]:
                note = c2s.SlideNote()
                note.end_lane = next_obj.lane
                note.end_width = next_obj.width
                note.is_curve = (
                    obj.note_type == sus.LongNoteType["CONTROL"] or 
                    obj.note_type == sus.LongNoteType["INVISIBLE"]
                )
            elif obj.note_kind == sus.LongNoteKind["HOLD"]:
                note = c2s.HoldNote()
            elif obj.note_kind == sus.LongNoteKind["AIR_HOLD"]:
                note = c2s.AirHold()
            
            note.measure = start_measure
            note.tick = start_ticks
            note.lane = obj.lane
            note.width = obj.width
            note.length = diff_ticks

            c2s_notes.append(note)

        if isinstance(obj, sus.BpmChange):
            definition = c2s.BpmSetting()
            definition.measure = obj.measure
            definition.tick = 0
            definition.bpm = obj.definition.tempo
            c2s_definitions.append(definition)

        if isinstance(obj, sus.BarLength):
            definition = c2s.MeterSetting()
            definition.measure = obj.measure
            definition.tick = 0
            definition.signature = (obj.length, 4) 
            c2s_definitions.append(definition)

    c2s_notes.sort(key=lambda note: note.measure + note.tick / c2s_ticks_per_measure)
    return (c2s_definitions, c2s_notes)