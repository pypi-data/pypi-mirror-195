import datetime
from struct import unpack


def read_xyz(fp):
    """Read xyz as integers, according to .3d spec"""
    return unpack("<iii", fp.read(12))


def read_len(fp):
    """Read a number as a length according to .3d spec"""
    byte = ord(fp.read(1))
    if byte != 0xFF:
        return byte
    else:
        return unpack("<I", fp.read(4))[0]


def read_label(fp, current_label):
    """Read a string as a label, or part thereof, according to .3d spec"""
    byte = ord(fp.read(1))
    if byte != 0x00:
        ndel = byte >> 4
        nadd = byte & 0x0F
    else:
        ndel = read_len(fp)
        nadd = read_len(fp)
    oldlen = len(current_label)
    return current_label[: oldlen - ndel] + fp.read(nadd).decode("ascii")


def add_days(start_date, days):
    return start_date + datetime.timedelta(days=days)


def read_svx_file(filename):

    exclude_surface_legs = 0
    exclude_duplicate_legs = 0
    exclude_splay_legs = 0
    exclude_surface_stations = 0

    station_list = []
    leg_list = []
    xsect_list = []

    station_xyz = {}

    with open(filename, "rb") as fp:

        line = fp.readline().rstrip()  # File ID check

        if not line.startswith(b"Survex 3D Image File"):
            raise IOError("Not a survex .3d file: " + filename)

        line = fp.readline().rstrip()  # File format version

        if not line.startswith(b"v"):
            raise IOError("Unrecognised survex .3d version in " + filename)

        version = int(line[1:])
        if version < 8:
            raise IOError("Survex .3d version >= 8 required in " + filename)

        line = fp.readline().rstrip()  # Metadata (title and coordinate system)
        fields = line.split(b"\x00")

        previous_title = ""

        if previous_title:
            self_title = previous_title + " + " + fields[0].decode("ascii")
        else:
            self_title = fields[0].decode("ascii")

        self_set_crs = fields[1].decode("ascii") if len(fields) > 1 else None

        line = fp.readline().rstrip()  # Timestamp, unused in present application

        if not line.startswith(b"@"):
            raise IOError("Unrecognised timestamp in " + filename)

        # timestamp = int(line[1:])

        flag = ord(fp.read(1))  # file-wide flag

        if flag & 0x80:  # abort if extended elevation
            raise IOError("Can't deal with extended elevation in " + filename)

        # All file-wide header data read in, now read byte-wise
        # according to .3d spec.  Note that all elements must
        # be processed, in order, otherwise we get out of sync.

        # We first define some baseline dates

        date0 = datetime.date(1900, 1, 1)
        date1 = datetime.date(1900, 1, 1)
        date2 = datetime.date(1900, 1, 1)

        label, style = "", 0xFF  # initialise label and style

        legs = []  # will be used to capture leg data between MOVEs
        xsect = []  # will be used to capture XSECT data
        nlehv = None  # .. remains None if there isn't any error data...

        while True:  # start of byte-gobbling while loop

            char = fp.read(1)

            if not char:  # End of file (reached prematurely?)
                raise IOError("Premature end of file in " + filename)

            byte = ord(char)

            if byte <= 0x05:  # STYLE
                if byte == 0x00 and style == 0x00:  # this signals end of data
                    if legs:  # there may be a pending list of legs to save
                        leg_list.append((legs, nlehv))
                    break  # escape from byte-gobbling while loop
                else:
                    style = byte

            elif byte <= 0x0E:  # Reserved
                continue

            elif byte == 0x0F:  # MOVE
                xyz = read_xyz(fp)
                if legs:
                    leg_list.append((legs, nlehv))
                    legs = []

            elif byte == 0x10:  # DATE (none)
                date1 = date2 = date0

            elif byte == 0x11:  # DATE (single date)
                days = unpack("<H", fp.read(2))[0]
                # date1 = date2 = date0.addDays(days)
                date1 = date2 = add_days(date0, days)

            elif byte == 0x12:  # DATE (date range, short format)
                days, extra = unpack("<HB", fp.read(3))
                date1 = add_days(date0, days)
                date2 = add_days(date0, days + extra + 1)

            elif byte == 0x13:  # DATE (date range, long format)
                days1, days2 = unpack("<HH", fp.read(4))
                date1 = add_days(date0, days1)
                date2 = add_days(date0, days2)

            elif byte <= 0x1E:  # Reserved
                continue

            elif byte == 0x1F:  # Error info
                nlehv = unpack("<iiiii", fp.read(20))

            elif byte <= 0x2F:  # Reserved
                continue

            elif byte <= 0x33:  # XSECT
                label = read_label(fp, label)
                if byte & 0x02:
                    lrud = unpack("<iiii", fp.read(16))
                else:
                    lrud = unpack("<hhhh", fp.read(8))
                xsect.append((label, lrud))
                if byte & 0x01:  # XSECT_END
                    xsect_list.append(xsect)
                    xsect = []

            elif byte <= 0x3F:  # Reserved
                continue

            elif byte <= 0x7F:  # LINE
                flag = byte & 0x3F
                if not (flag & 0x20):
                    label = read_label(fp, label)
                xyz_prev = xyz
                xyz = read_xyz(fp)
                while True:  # code pattern to implement logic
                    if exclude_surface_legs and flag & 0x01:
                        break
                    if exclude_duplicate_legs and flag & 0x02:
                        break
                    if exclude_splay_legs and flag & 0x04:
                        break
                    legs.append(((xyz_prev, xyz), label, style, date1, date2, flag))
                    break

            elif byte <= 0xFF:  # LABEL (or NODE)
                flag = byte & 0x7F
                label = read_label(fp, label)
                xyz = read_xyz(fp)
                while True:  # code pattern to implement logic
                    if exclude_surface_stations and flag & 0x01 and not flag & 0x02:
                        break
                    station_list.append((xyz, label, flag))
                    break
                station_xyz[label] = xyz

    return {
        "station_list": station_list,
        "leg_list": leg_list,
        "xsect_list": xsect_list,
        "station_xyz": station_xyz,
    }
