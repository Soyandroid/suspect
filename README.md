# Suspect sus (and c2s) file format tool

Suspect is a tool to convert back and forth between .sus and .c2s, and generally do various things with the file formats used by CHUNITHM, Seaurchin, and various chart editors. It is still in development. 

## Implemented features

- Convert .sus to .c2s
    - The header is placeholder, as CHUNITHM apparently ignores it.
    - The footer is placeholder, because I am lazy CHUNITHM doesn't seem to care about it.
- Render .sus to text
    - Basically just serves as a validity check for .sus files

## Planned features

- Convert .c2s to .sus
    - Because at some point, I might want to show off CHUNITHM without showing arcade data.
    - In case Laverita ever releases (.sus -> .dr2 exists already), or Seaurchin gets revived.
- Convert .sus header metadata to CHUNITHM xml files
    - Because honestly, filling out xml files by hand sucks.
- Implement all the weird shit .sus supports
    - Like speed changes and stuff

## Requirements

- Python 3.8 or newer
- Knowing how to use the command line

## Usage

```
python suspect.py [command]
Available commands:
    sustotxt [input] [measure_div] [output]
        Renders a .sus file to unicode, using <measure_div> lines per measure
    sustoc2s [input] [output]
        Converts a .sus file to c2s format
    c2stoc2s [input] [output]
        Tests the c2s parser / exporter by outputting a file equivalent to the input
```

## Notes

- The code kinda sucks. I don't usually write python.
- The SUS format specification sucks, and not just because it's Google-translated. This format sucks and makes no sense.
- The SUS format supports dumb things that make no sense and CHUNITHM doesn't support, those things obviously get ignored.
    - NotesEditorForD particularly outputs SUS files that suck, but Seaurchin is fine with them for some reason. The files suck, and I have to make them suck less before I can do anything reasonable with them.

- Many thanks to "hahaluckyme" on Discord for the extremely useful .c2s documentation they wrote, and to everyone cited on their doc.
- Thanks to everyone who worked on Seaurchin for the SUS format. I don't like it, but I can't deny that it's useful.