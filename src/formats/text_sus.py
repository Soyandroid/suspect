from .sus import *
from sys import argv

def output_shortnote(tapnote:ShortNote):
    short_note_chars = {
        TapNoteType["TAP"]: u"-",
        TapNoteType["EXTAP"]: u"=",
        TapNoteType["FLICK"]: u"~",
        TapNoteType["HELL"]: u"X",
        TapNoteType["RESERVED1"]: u"?",
        TapNoteType["RESERVED2"]: u"?",

        AirNoteType["UP"]:u"🢁",
        AirNoteType["DOWN"]:u"🢃",
        AirNoteType["UP_LEFT"]:u"🢄",
        AirNoteType["UP_RIGHT"]:u"🢅",
        AirNoteType["DOWN_LEFT"]:u"🢇",
        AirNoteType["DOWN_RIGHT"]:u"🢆"
    }

    start_lane = tapnote.lane
    char = short_note_chars[tapnote.note_type]

    if tapnote.width == 1:
        retval = "    " * start_lane + " " + char * 2 + " "
    else:
        retval = "    " * start_lane + " " + char * 3 + char * 4 * (tapnote.width - 2) + char * 3 + " "

    if isinstance(tapnote.note_type, AirNoteType):
        return ("", retval)
    else:
        return (retval, "")

def print_note_group(group, buffer, measure_division, ticks_per_measure = SUS_TICKS_PER_MEASURE):
    notes = []
    group = list(group)
    for item in group:
        offset = 2 * (item.measure * measure_division + item.tick // (ticks_per_measure // measure_division))
        notes.append((offset, item))

    min_offset = min(p[0] for p in notes)
    max_offset = max(p[0] for p in notes)

    for offset in range(min_offset, max_offset + 1):
        update = ""
        current = list(n for n in notes if n[0] == offset)
        if len(current) != 0:
            note = current[0][1]
            if note.note_kind == LongNoteKind["AIR_HOLD"]:
                if note.width == 1:
                    update = "    " * note.lane + " [] "
                else:
                    update = "    " * note.lane + " [" + " " * 2 + " " * 4 * (note.width - 2) + " " * 2 + "] "
            else:
                if note.width == 1:
                    update = "    " * note.lane + " " + "|" * 2 + " "
                else:
                    update = "    " * note.lane + "|" + "-" * 3 + "-" * 4 * (note.width - 2) + "-" * 3 + "|"
        else:
            prev = list(n for n in notes if n[0] < offset)
            nxt = list(n for n in notes if n[0] > offset)
            if len(prev) != 0 and len(nxt) != 0:
                prev = prev[-1]
                nxt = nxt[0]
                if prev[1].note_type == LongNoteType["END"]:
                    break
                lerp_amount = (offset - prev[0]) / (nxt[0] - prev[0])
                lerped_lane = int(4 * (prev[1].lane + lerp_amount * (nxt[1].lane - prev[1].lane)))
                lerped_width = int(4 * (prev[1].width + lerp_amount * (nxt[1].width - prev[1].width)))
                if prev[1].note_kind == LongNoteKind["AIR_HOLD"]:
                    print_position = lerped_lane + lerped_width // 2
                    update = " " * (print_position - 1) + "/\\"
                else:
                    update = " " * lerped_lane + "|" + "." * (lerped_width - 2) + "|"
        update_buffer(buffer, offset, update)

def convert(data, measure_division):
    short_notes = list(filter(lambda obj: isinstance(obj, ShortNote), data))
    long_notes = list(filter(lambda obj: isinstance(obj, LongNote), data))
    long_note_groups = set(
        tuple(i) for i in map(
            lambda note: note.linked,
            long_notes
        )
    )

    last_measure = max(map(lambda obj: obj.measure, short_notes + long_notes))
    buffer = [" " * 64 for i in range((last_measure + 1) * measure_division * 2)]

    for note in short_notes:
        offset = note.measure * measure_division + note.tick // (SUS_TICKS_PER_MEASURE // measure_division)
        update = output_shortnote(note)
        update_buffer(buffer, offset * 2, update[0])
        update_buffer(buffer, offset * 2 + 1, update[1])

    for group in long_note_groups:
        print_note_group(group, buffer, measure_division)

    buffer.reverse()

    return "┃" + "┃\n┃".join(buffer) + "┃"

def update_buffer(buffer, offset, update):
    line = list(buffer[offset])

    for i in range(len(update)):
        if update[i] != " ":
            line[i] = update[i]

    buffer[offset] = "".join(line)