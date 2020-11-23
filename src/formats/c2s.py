from abc import ABC, abstractmethod
from enum import Enum, auto

C2S_TICKS_PER_BEAT = 384

class C2sObject(ABC):
    beat = 0
    tick = 0

class BpmSetting(C2sObject):
    bpm = 0.0
    def __str__(self):
        return "BPM\t%s\t%s\t%s" % (self.beat, self.tick, self.bpm)

class MeterSetting(C2sObject):
    signature = (0, 0)
    def __str__(self):
        return "MET\t%s\t%s\t%s\t%s" % (self.beat, self.tick, self.signature[0], self.signature[1])

class SpeedSetting(C2sObject):
    length = 0
    speed = 1.0
    def __str__(self):
        return "SFL\t%s\t%s\t%s\t%s" % (self.beat, self.tick, self.length, self.speed)

class C2sNote(C2sObject):
    lane = 0
    width = 0

class TapNote(C2sNote):
    def __str__(self):
        return "TAP\t%s\t%s\t%s\t%s" % (self.beat, self.tick, self.lane, self.width)

class MineNote(C2sNote):
    def __str__(self):
        return "MNE\t%s\t%s\t%s\t%s" % (self.beat, self.tick, self.lane, self.width)

class ChargeNote(C2sNote):
    def __str__(self):
        # Seems to always be "UP"
        return "CHR\t%s\t%s\t%s\t%s\tUP" % (self.beat, self.tick, self.lane, self.width)
    pass

class FlickNote(C2sNote):
    def __str__(self):
        # Seems to always be "Left"
        return "FLK\t%s\t%s\t%s\t%s\tL" % (self.beat, self.tick, self.lane, self.width)
    pass

class AirHold(C2sNote):
    length = 0
    def __str__(self):
        return "AHD\t%s\t%s\t%s\t%s\tTAP\t%s" % (self.beat, self.tick, self.lane, self.width, self.length)

class HoldNote(C2sNote):
    length = 0
    def __str__(self):
        return "HLD\t%s\t%s\t%s\t%s\t%s" % (self.beat, self.tick, self.lane, self.width, self.length)

class SlideNote(C2sNote):
    length = 0
    end_lane = 0
    end_width = 0
    is_curve = False

    def __str__(self):
        if self.is_curve:
            tag = "SLC"
        else:
            tag = "SLD"
        return "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (tag, self.beat, self.tick, self.lane, self.width, self.length, self.end_lane, self.end_width)

class AirNote(C2sNote):
    isUp = True
    direction = 0
    linkage = "TAP" # Apparently doesn't matter
    def __str__(self):
        if self.isUp:
            if self.direction > 0:
                tag = "AUR"
            elif self.direction < 0:
                tag = "AUL"
            else:
                tag = "AIR"
        else:
            if self.direction > 0:
                tag = "ADR"
            elif self.direction < 0:
                tag = "ADL"
            else:
                tag = "ADW"

        return "%s\t%s\t%s\t%s\t%s\t%s" % (tag, self.beat, self.tick, self.lane, self.width, self.linkage)

def from_string(c2s_string:str):
    line = c2s_string.split()
    obj = None
    if len(line) > 0:
        if line[0] == "BPM":
            obj = BpmSetting()
            obj.bpm = float(line[3])
        if line[0] == "MET":
            obj = MeterSetting()
            obj.signature = (int(line[3]), int(line[4]))
        if line[0] == "SFL":
            obj = SpeedSetting()
            obj.length = int(line[3])
            obj.speed = float(line[4])
        if line[0] == "TAP":
            obj = TapNote()
        if line[0] == "MNE":
            obj = MineNote()
        if line[0] == "CHR":
            obj = ChargeNote()
        if line[0] == "FLK":
            obj = FlickNote()
        if line[0] == "AHD":
            obj = AirHold()
            obj.length = int(line[6])
        if line[0] == "HLD":
            obj = HoldNote()
            obj.length = int(line[5])
        if line[0] == "SLD" or line[0] == "SLC":
            obj = SlideNote()
            obj.length = int(line[5])
            obj.end_lane = int(line[6])
            obj.end_width = int(line[7])
            obj.is_curve = line[0] == "SLC"

        if line[0] == "AUL":
            obj = AirNote()
            obj.direction = -1
            obj.isUp = True
        if line[0] == "AUR":
            obj = AirNote()
            obj.direction = 1
            obj.isUp = True
        if line[0] == "AIR":
            obj = AirNote()
            obj.direction = 0
            obj.isUp = True
        if line[0] == "ADL":
            obj = AirNote()
            obj.direction = -1
            obj.isUp = False
        if line[0] == "ADR":
            obj = AirNote()
            obj.direction = 1
            obj.isUp = False
        if line[0] == "ADW":
            obj = AirNote()
            obj.direction = 0
            obj.isUp = False

        if isinstance(obj, C2sObject):
            obj.beat = int(line[1])
            obj.tick = int(line[2])
        if isinstance(obj, C2sNote):
            obj.lane = int(line[3])
            obj.width = int(line[4])

    if obj == None:
        return []

    return [obj]

def create_file(definitions, notes):
    sample_header = """VERSION	1.07.00	1.07.00
MUSIC	0
SEQUENCEID	0
DIFFICULT	00
LEVEL	0.0
CREATOR	Meme
BPM_DEF	132.000	132.000	132.000	132.000
MET_DEF	4	4
RESOLUTION	384
CLK_DEF	384
PROGJUDGE_BPM	240.000
PROGJUDGE_AER	  0.999
TUTORIAL	0
"""
    sample_footer = """T_REC_TAP	999
T_REC_CHR	999
T_REC_FLK	999
T_REC_MNE	999
T_REC_HLD	999
T_REC_SLD	999
T_REC_AIR	999
T_REC_AHD	999
T_REC_ALL	999
T_NOTE_TAP	999
T_NOTE_CHR	999
T_NOTE_FLK	999
T_NOTE_MNE	0
T_NOTE_HLD	999
T_NOTE_SLD	999
T_NOTE_AIR	999
T_NOTE_AHD	999
T_NOTE_ALL	999
T_NUM_TAP	999
T_NUM_CHR	999
T_NUM_FLK	999
T_NUM_MNE	0
T_NUM_HLD	999
T_NUM_SLD	999
T_NUM_AIR	999
T_NUM_AHD	999
T_NUM_AAC	999
T_CHRTYPE_UP	999
T_CHRTYPE_DW	0
T_CHRTYPE_CE	0
T_LEN_HLD	999999
T_LEN_SLD	999999
T_LEN_AHD	999999
T_LEN_ALL	999999
T_JUDGE_TAP	999
T_JUDGE_HLD	999
T_JUDGE_SLD	999
T_JUDGE_AIR	999
T_JUDGE_FLK	999
T_JUDGE_ALL	9999
T_FIRST_MSEC	100
T_FIRST_RES	100
T_FINAL_MSEC	999999
T_FINAL_RES	999999
T_PROG_00	46
T_PROG_05	52
T_PROG_10	57
T_PROG_15	43
T_PROG_20	58
T_PROG_25	56
T_PROG_30	55
T_PROG_35	60
T_PROG_40	88
T_PROG_45	51
T_PROG_50	43
T_PROG_55	43
T_PROG_60	44
T_PROG_65	53
T_PROG_70	64
T_PROG_75	65
T_PROG_80	51
T_PROG_85	84
T_PROG_90	52
T_PROG_95	81
""" 
    if any(filter(lambda d: isinstance(d, MeterSetting), definitions)) == 0:
        setting = MeterSetting()
        setting.signature = (4, 4)
        setting.beat = 0
        setting.tick = 0
        definitions.append(setting)

    return (
        sample_header + "\n" +
        "\n".join(map(str, definitions)) + "\n\n" +
        "\n".join(map(str, notes)) + "\n\n" +
        sample_footer
    )