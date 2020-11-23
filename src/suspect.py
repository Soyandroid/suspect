from sys import argv
import formats.convert as convert
import formats.text_sus as text_sus
import formats.sus as sus
import formats.c2s as c2s

def help():
    print("Usage: suspect.py [command]")
    print("sustotxt [input] [measure_div] [output]\n\tRenders a .sus file to unicode, using <measure_div> lines per measure")
    print("sustoc2s [input] [output]\n\tConverts a .sus file to c2s format")
    print("c2stoc2s [input] [output]\n\tTests the c2s parser / exporter by outputting a file equivalent to the input")
    # print("sustoxml [input] [output] [id]\n\tExtracts metadata from .sus file into an XML file")
    # print("sus2sus [input] [output]\n\tTests the sus parser by outputting a file equivalent to the input")
    return 1

def read_sus(filename):
    data = []
    f = open(filename, "r")
    lines = f.readlines()
    f.close()
    context = sus.SusContext()
    for line in lines:
        data += sus.from_string(line, context)

    context.fix_channels()

    return data

def read_c2s(filename):
    data = []
    f = open(filename, "r")
    lines = f.readlines()
    f.close()
    for line in lines:
        data += c2s.from_string(line)
    
    return data

def write_output(filename, output):
    f = open(filename, "w")
    f.write(string)
    f.close()
    print("Wrote %s" % filename)

argc = len(argv)

if argc == 1:
    exit(help())

if argv[1] == "sustotxt":
    if argc != 5:
        exit(help())
    string = text_sus.convert(read_sus(argv[2]), int(argv[3]))
    write_output(argv[4], string)
    exit(0)

if argv[1] == "c2stoc2s":
    if argc != 4:
        exit(help())
    c2s_data = read_c2s(argv[2])
    definitions = filter(lambda d: not isinstance(d, c2s.C2sNote), c2s_data)
    notes = filter(lambda d: isinstance(d, c2s.C2sNote), c2s_data)
    string = c2s.create_file(definitions, notes)
    write_output(argv[3], string)
    exit(0)

if argv[1] == "sustoc2s":
    if argc != 4:
        exit(help())
    sus_data = read_sus(argv[2])
    (definitions, notes) = convert.sus_to_c2s(sus_data)
    string = c2s.create_file(definitions, notes)
    write_output(argv[3], string)
    exit(0)

exit(help())