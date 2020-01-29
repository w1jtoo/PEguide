import argparse
import time
import struct
import string

parser = argparse.ArgumentParser()

parser.add_argument("file",)
parser.add_argument("--headers",  nargs='?', const=True, default=False)
parser.add_argument("--sections",  nargs='?', type=int)

args = parser.parse_args()


def get_name(_bytes):
    result = []
    decoded = _bytes.decode("cp1251", "ignore")
    for letter in decoded:
        if letter in string.digits or letter in string.ascii_letters or\
           letter in string.punctuation:
            result.append(letter)
    return "".join(result)


def get_hex(_bytes):
    return hex(int.from_bytes(_bytes, "little"))


def get_dos_header(_bytes):
    dos_header = {}
    dos_header["e_magic"] = _bytes[:2]
    dos_header["e_lfanew"] = _bytes[60:64]

    return dos_header


def get_PE_header(_bytes):
    PE_header = {}
    PE_header["Signature"] = _bytes[:4]

    PE_header["Machine"] = _bytes[4:6]
    PE_header["NumberOfSections"] = _bytes[6:8]
    PE_header["TimeDateStamp"] = time.ctime(*struct.unpack("i", _bytes[8:12]))
    PE_header["PointerToSymbolTable"] = _bytes[12:16]
    PE_header["NumberOfSymbols"] = _bytes[16:20]
    PE_header["SizeOfOptionalHeader"] = _bytes[20:22]
    PE_header["Characteristics"] = _bytes[22:24]

    PE_header["Magic"] = _bytes[24:26]
    PE_header["MajorLinkerVersion"] = _bytes[26:27]
    PE_header["MinorLinkerVersion"] = _bytes[27:28]
    PE_header["SizeOfCode"] = _bytes[28:32]
    PE_header["SizeOfInitializedData"] = _bytes[32:36]
    PE_header["SizeOfUninitializedData"] = _bytes[36:40]
    PE_header["AddressOfEntryPoint"] = _bytes[40:44]
    PE_header["BaseOfCode"] = _bytes[44:48]
    PE_header["BaseOfData"] = _bytes[48:52]
    PE_header["ImageBase"] = _bytes[52:56]
    PE_header["SectionAlignment"] = _bytes[56:60]
    PE_header["FileAlignment"] = _bytes[60:64]

    PE_header["MajorOperatingSystemVersion"] = _bytes[64:66]
    PE_header["MinorOperatingSystemVersion"] = _bytes[66:68]
    PE_header["MajorImageVersion"] = _bytes[68:70]
    PE_header["MinorImageVersion"] = _bytes[70:72]
    PE_header["MajorSubsystemVersion"] = _bytes[72:74]
    PE_header["MinorSubsystemVersion"] = _bytes[74:76]

    PE_header["Win32VersionValue"] = _bytes[76:80]
    PE_header["SizeOfImage"] = _bytes[80:84]
    PE_header["SizeOfHeaders"] = _bytes[84:88]
    PE_header["CheckSum"] = _bytes[88:92]

    PE_header["Subsystem"] = _bytes[92:94]
    PE_header["DllCharacteristics"] = _bytes[94:96]

    PE_header["SizeOfStackReserve"] = _bytes[96:100]
    PE_header["SizeOfStackCommit"] = _bytes[100:104]
    PE_header["SizeOfHeapReserve"] = _bytes[104:108]
    PE_header["SizeOfHeapCommit"] = _bytes[108:112]
    PE_header["LoaderFlags"] = _bytes[112:116]
    PE_header["NumberOfRvaAndSizes"] = _bytes[116:120]

    # IMAGE_DATA_DIRECTORY DataDirectory[IMAGE_NUMBEROF_DIRECTORY_ENTRIES];

    return PE_header


def get_parsed_header(_bytes):
    result = {}
    result["Name"] = _bytes[0:8]

    result["PhysicalAddress"] = _bytes[8:12]
    result["VirtualAddress"] = _bytes[12:16]
    result["SizeOfRawData"] = _bytes[16:20]
    result["PointerToRawData"] = _bytes[20:24]
    result["PointerToRelocations"] = _bytes[24:28]
    result["PointerToLinenumbers"] = _bytes[28:32]

    result["NumberOfRelocations"] = _bytes[32:34]
    result["NumberOfLinenumbers"] = _bytes[34:36]

    result["Characteristics"] = _bytes[36:40]
    return result


def get_section_headers(_bytes, number_of_sections):
    result = []
    for index in range(number_of_sections):
        position = index * 40
        result.append(get_parsed_header(_bytes[position: position + 40]))
    return result


def print_dos_header(dos_header):
    print()
    keys = dos_header.keys()
    print("DOS Header")
    for key in keys:
        print(key, get_hex(dos_header[key]))


def print_PE_header(PE_header):
    spesial_fileds = ["NumberOfSections", "TimeDateStamp"]
    print()
    keys = PE_header.keys()
    print("PE Header")
    for key in keys:
        if key not in spesial_fileds:
            print(key, get_hex(PE_header[key]))
        if key == "NumberOfSections":
            print(key, int.from_bytes(PE_header[key], "little"))
        if key == "TimeDateStamp":
            print(key, PE_header[key])


def print_section_header(section_header):
    print()
    for i in range(len(section_header)):
        print("SECTION №", i)
        keys = section_header[i].keys()
        for key in keys:
            if key != "Name":
                print(key, get_hex(section_header[i][key]))
            if key == "Name":
                print(key, get_name(section_header[i][key]))


def get_data_from_section(offset, size):
    result = []
    i_offset = int.from_bytes(offset, "little")
    i_size = int.from_bytes(size, "little")
    _file.seek(i_offset, 0)
    _bytes = _file.read(i_size)
    for i in range(i_size):
        result.append(hex(_bytes[i]))
    return result


def convert(value):
    if 0 <= value <= 9:
        return str(value)
    if value == 10:
        return "A"
    if value == 11:
        return "B"
    if value == 12:
        return "C"
    if value == 13:
        return "D"
    if value == 14:
        return "E"
    if value == 15:
        return "F"


def nice_decode(value):
    i_value = int(value, 16)
    return convert(i_value // 16) + convert(i_value % 16)


def print_section(section, number):
    print()
    print("Data of Section №", number)
    flag = 0
    print("    ", end="")
    for k in range(len(section)):
        print(nice_decode(section[k]), end=" ")
        flag += 1
        if flag == 8:
            print(" ", end="")
        if flag == 16:
            flag = 0
            print()
            print("    ", end="")


with open(args.file, mode="rb") as _file:
    dos_header = get_dos_header(_file.read(64))
    offset = int.from_bytes(dos_header["e_lfanew"], "little")

    _file.seek(offset, 0)
    PE_header = get_PE_header(_file.read(248))  # think about 256->...
    numb_of_sections = int.from_bytes(PE_header["NumberOfSections"], "little")
    section_header = get_section_headers(_file.read(40 * numb_of_sections),
                                         numb_of_sections)  # check constant

    section_data = []
    for i in range(numb_of_sections):
        section_data.append(get_data_from_section(section_header[i]["PointerToRawData"],
                            section_header[i]["SizeOfRawData"]))

    if args.headers:
        print_dos_header(dos_header)
        print_PE_header(PE_header)
        print_section_header(section_header)

    if args.sections:
        if args.sections == -1:
            for i in range(numb_of_sections):
                print_section(section_data[i], i)
        elif 0 <= args.sections < numb_of_sections:
            print_section(section_data[args.sections], args.sections)
        else:
            print("Section with this number doesn't exist, " +
                  "please change number of section")
