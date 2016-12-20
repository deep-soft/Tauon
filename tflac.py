# Tauon Music Box - Tag Module

# Copyright © 2015-2016, Taiko2k captain.gxj@gmail.com

#     This file is part of Tauon Music Box.
#
#     Tauon Music Box is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Tauon Music Box is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Lesser General Public License for more details.
#
#     You should have received a copy of the GNU Lesser General Public License
#     along with Tauon Music Box.  If not, see <http://www.gnu.org/licenses/>.
#
#    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE


# The purpose of this module is to read metadata from FLAC, OGG, OPUS, APE and WV files



import struct


class Flac:

    def __init__(self, file):

        self.filepath = file
        self.has_picture = False
        self.picture = ""

        self.album_artist = ""
        self.artist = ""
        self.genre = ""
        self.date = ""
        self.comment = ""
        self.album = ""
        self.track_number = ""
        self.track_total = ""
        self.title = ""
        self.encoder = ""
        self.disc_number = ""
        self.picture = ""
        self.disc_total = ""
        self.lyrics = ""

        self.sample_rate = 48000
        self.bit_rate = 0
        self.length = 0


    def read_vorbis(self, f):

        #print(f.tell())

        #print("LEN: " + str(z[2]))
        block_position = 0

        buffer = f.read(4)
        block_position += 4
        jump = int.from_bytes(buffer, byteorder='little')

        buffer = f.read(jump)
        block_position += jump

        # f.seek(block_position * -1, 1)
        # print(f.tell())

        buffer = f.read(4)
        block_position += 4
        fields = int.from_bytes(buffer, byteorder='little')
        # print(fields)
        for i in range(fields):
            buffer = f.read(4)
            block_position += 4

            jump = int.from_bytes(buffer, byteorder='little')
            buffer = f.read(jump)
            block_position += jump

            # print(buffer.decode('utf-8'))

            position = 0
            while position < 40:
                # print(sss[position:position+1])
                position += 1

                if buffer[position:position + 1] == b'=':
                    # print(sss[0:position])
                    # print(sss[position + 1:])
                    a = buffer[0:position].decode("utf-8").lower()
                    b = buffer[position + 1:]

                    # print(a)
                    # print(b)

                    if a == "genre":
                        self.genre = b.decode("utf-8")
                    elif a == "date":
                        self.date = b.decode("utf-8")
                    elif a == "comment":
                        self.comment = b.decode("utf-8")
                    elif a == "album":
                        self.album = b.decode("utf-8")
                    elif a == "title":
                        self.title = b.decode("utf-8")
                    elif a == "tracknumber":
                        self.track_number = b.decode("utf-8")
                    elif a == "tracktotal" or a == "totaltracks":
                        self.track_total = b.decode("utf-8")
                    elif a == "encoder":
                        self.encoder = b.decode("utf-8")
                    elif a == "albumartist" or a == "album artist":
                        self.album_artist = b.decode("utf-8")
                    elif a == "artist":
                        self.artist = b.decode("utf-8")
                    elif a == 'disctotal' or a == 'totaldiscs':
                        self.disc_total = b.decode("utf-8")
                    elif a == "discnumber":
                        self.disc_number = b.decode("utf-8")
                    elif a == "metadata_block_picture":
                        print("Tag Scanner: Found picture inside vorbis comment inside a FLAC file. Ignoring")
                        print("      In file: " + self.filepath)
                    elif a == 'lyrics' or a == 'unsyncedlyrics':
                        self.lyrics = b.decode("utf-8")

        #print("len total: " + str(block_position))
        sss = f.seek(block_position * -1, 1)
        #print(f.tell())


    def read_seek_table(self, f):

        f.read(10)
        buffer = f.read(8)
        a = (int.from_bytes(buffer, byteorder='big'))
        k = bin(a)[2:].zfill(64)

        samplerate = int(k[0:20], 2)
        # print(samplerate)
        self.sample_rate = samplerate

        bps = int(k[23:28], 2)
        # print(bps)
        self.sample_rate = samplerate

        samples = int(k[28:64], 2)
        # print(samples)
        self.length = samples / samplerate

        f.seek(-18, 1)


    def read(self, get_picture=False):

        # Very helpful: https://xiph.org/flac/format.html

        f = open(self.filepath, "rb")
        s = f.read(4)
        if s != b'fLaC':
            return

        i = 0
        while i < 7:
            i += 1

            z = self.read_block(f)

            if z[1] == 0:
                self.read_seek_table(f)
            if z[1] == 4:
                self.read_vorbis(f)

            if z[1] == 6 and get_picture:

                a = f.read(4)
                a = int.from_bytes(a, byteorder='big')
                # print("Picture type: " + str(a))

                a = f.read(4)
                b = int.from_bytes(a, byteorder='big')
                # print("MIME len: " + str(b))

                a = f.read(b)
                # print(a)
                # print("MIME: " + a.decode('ascii'))

                a = f.read(4)
                a = int.from_bytes(a, byteorder='big')
                # print("Description len: " + str(a))

                a = f.read(a)
                # print("Description: " + a.decode('utf-8'))

                a = f.read(4)
                # a = int.from_bytes(a, byteorder='big')
                # print("Width: " + str(a))

                a = f.read(4)
                # a = int.from_bytes(a, byteorder='big')
                # print("Height: " + str(a))

                a = f.read(4)
                # a = int.from_bytes(a, byteorder='big')
                # print("BPP: " + str(a))

                a = f.read(4)
                # a = int.from_bytes(a, byteorder='big')
                # print("Index colour: " + str(a))

                a = f.read(4)
                a = int.from_bytes(a, byteorder='big')
                # print("Bin len: " + str(a))

                self.has_picture = True
                self.picture = f.read(a)
                # print(len(data))

            else:
                data = f.read(z[2])

            if z[0] == 1:
                break

        f.close()

    def read_block(self, f):

        q = f.read(1)
        a = (int.from_bytes(q, byteorder='big'))
        k = bin(a)[2:].zfill(8)
        flag = int(k[:1], 2)
        block_type = int(k[1:], 2)
        s = f.read(3)
        a = (int.from_bytes(s, byteorder='big'))
        length = a

        return flag, block_type, length

    def get(self):
        pass


# file = 'b.flac'
#
# item = Flac(file)
# item.read()


class Opus:

    def __init__(self, file):

        self.filepath = file
        self.has_picture = False

        self.album_artist = ""
        self.artist = ""
        self.genre = ""
        self.date = ""
        self.comment = ""
        self.album = ""
        self.track_number = ""
        self.track_total = ""
        self.title = ""
        self.encoder = ""
        self.disc_number = ""
        self.disc_total = ""
        self.picture = ""
        self.lyrics = ""

        self.sample_rate = 48000
        self.bit_rate = 0
        self.length = 0

    def read(self):

        f = open(self.filepath, "rb")

        header = struct.unpack('<4sBBqIIiB', f.read(27))
        # print(header)

        segs = struct.unpack('B'*header[7], f.read(header[7]))
        s = f.read(7)

        if s == b'OpusHea':
            f.seek(-7, 1)
        elif s == b'\x01vorbis':

            s = f.read(4)
            a = struct.unpack("<B4i", f.read(17)) # 44100
            self.sample_rate = a[1]
            self.bit_rate = int(a[3] / 1000)
            f.seek(-28, 1)

        else:
            return

        for p in segs:
            f.read(p)

        header = struct.unpack('<4sBBqIIiB', f.read(27))

        s = f.read(header[7])
        s = f.read(7)

        if s == b"OpusTag":
            f.read(1)
        elif s == b"\x03vorbis":
            pass
        else:
            return

        s = f.read(4)
        a = int.from_bytes(s, byteorder='little')
        s = f.read(a)


        s = f.read(4)
        number = int.from_bytes(s, byteorder='little')

        for i in range(number):
            s = f.read(4)
            length = int.from_bytes(s, byteorder='little')
            s = f.read(length)

            position = 0
            while position < 40:

                position += 1

                if s[position:position+1] == b'=':

                    # print(s[0:position])
                    # print(s[position + 1:])
                    a = s[0:position].decode("utf-8").lower()
                    b = s[position + 1:]

                    # print(a)
                    # print(b)

                    if a == "genre":
                        self.genre = b.decode("utf-8")
                    elif a == "date":
                        self.date = b.decode("utf-8")
                    elif a == "comment":
                        self.comment = b.decode("utf-8")
                    elif a == "album":
                        self.album = b.decode("utf-8")
                    elif a == "title":
                        self.title = b.decode("utf-8")
                    elif a == "tracknumber":
                        self.track_number = b.decode("utf-8")
                    elif a == "tracktotal" or a == "totaltracks":
                        self.track_total = b.decode("utf-8")
                    elif a == "encoder":
                        self.encoder = b.decode("utf-8")
                    elif a == "albumartist" or a == "album artist":
                        self.album_artist = b.decode("utf-8")
                    elif a == "artist":
                        self.artist = b.decode("utf-8")
                    elif a == "metadata_block_picture":

                        # This code kind of works but i've disabled it because its very slow

                        print("Tag Scanner: Found picture in OGG/OPUS file. Ignoring")
                        print("      In file: " + self.filepath)

                        # self.has_picture = True
                        # print("Found picture block")
                        # import base64
                        # import io

                        # ee = base64.b64decode(b[0:500])
                        #
                        # # return
                        #
                        # ss = io.BytesIO(ee)
                        # ss.seek(0)
                        #
                        # # z = ss.read(4)
                        # # print(int.from_bytes(z, byteorder='big')) # Type
                        # #
                        # # ss.seek(0)
                        #
                        # qqq = ss.read(4)
                        # qqq = int.from_bytes(qqq, byteorder='big')
                        # print("Picture type: " + str(qqq))
                        # qqq = ss.read(4)
                        # b = int.from_bytes(qqq, byteorder='big')
                        # print("MIME len: " + str(b))
                        #
                        # qqq = ss.read(b)
                        # # print(qqq)
                        # print("MIME: " + qqq.decode('ascii'))
                        #
                        # qqq = ss.read(4)
                        # qqq = int.from_bytes(qqq, byteorder='big')
                        # print("Description len: " + str(qqq))
                        #
                        # qqq = ss.read(qqq)
                        # print("Description: " + qqq.decode('utf-8'))
                        #
                        # qqq = ss.read(4)
                        # qqq = int.from_bytes(qqq, byteorder='big')
                        # print("Width: " + str(qqq))
                        #
                        # qqq = ss.read(4)
                        # qqq = int.from_bytes(qqq, byteorder='big')
                        # print("Height: " + str(qqq))
                        #
                        # qqq = ss.read(4)
                        # qqq = int.from_bytes(qqq, byteorder='big')
                        # print("BPP: " + str(qqq))
                        #
                        # qqq = ss.read(4)
                        # qqq = int.from_bytes(qqq, byteorder='big')
                        # print("Index colour: " + str(qqq))
                        #
                        # qqq = ss.read(4)
                        # qqq = int.from_bytes(qqq, byteorder='big')
                        # print("Bin len: " + str(qqq))
                        # b_len = str(qqq)
                        #
                        # f.seek(start_position_a)
                        # #header = struct.unpack('<4sBBqIIiB', f.read(27))
                        # segs = struct.unpack('B' * header[7], f.read(header[7]))
                        # k = b""
                        # for p in segs:
                        #     k += f.read(p)
                        #
                        # mmp = 0
                        # while k[mmp:mmp+23] != b'METADATA_BLOCK_PICTURE=':
                        #     mmp += 1
                        #     if mmp > 50000:
                        #         return
                        # mmp += 23
                        # k = k[mmp:]
                        #
                        #
                        #
                        # while len(k) < qqq * 1.5:
                        #     header = struct.unpack('<4sBBqIIiB', f.read(27))
                        #     segs = struct.unpack('B' * header[7], f.read(header[7]))
                        #     for p in segs:
                        #         k += f.read(p)
                        #     #print(len(k))
                        #
                        # print(k[0:30]) # Preview start of block
                        # print(k[-30:]) # Preview end of block
                        #
                        #
                        #
                        # # print(len(b) / 4)
                        # # print(len(b) * 8)
                        # print('start decode')
                        # #ee = base64.b64decode(k + b'===')
                        # ss = io.BytesIO(base64.b64decode(k + b'==='))
                        # # return
                        #
                        # #ss = io.BytesIO(ee)
                        # ss.seek(0)
                        #
                        # # z = ss.read(4)
                        # # print(int.from_bytes(z, byteorder='big')) # Type
                        # #
                        # # ss.seek(0)
                        #
                        # qqq = ss.read(4)
                        # qqq = int.from_bytes(qqq, byteorder='big')
                        # print("Picture type: " + str(qqq))
                        # qqq = ss.read(4)
                        # b = int.from_bytes(qqq, byteorder='big')
                        # print("MIME len: " + str(b))
                        #
                        # qqq = ss.read(b)
                        # # print(qqq)
                        # print("MIME: " + qqq.decode('ascii'))
                        #
                        #
                        # qqq = ss.read(4)
                        # qqq = int.from_bytes(qqq, byteorder='big')
                        # print("Description len: " + str(qqq))
                        #
                        # qqq = ss.read(qqq)
                        # print("Description: " + qqq.decode('utf-8'))
                        #
                        # qqq = ss.read(4)
                        # qqq = int.from_bytes(qqq, byteorder='big')
                        # print("Width: " + str(qqq))
                        #
                        # qqq = ss.read(4)
                        # qqq = int.from_bytes(qqq, byteorder='big')
                        # print("Height: " + str(qqq))
                        #
                        #
                        # qqq = ss.read(4)
                        # qqq = int.from_bytes(qqq, byteorder='big')
                        # print("BPP: " + str(qqq))
                        #
                        # qqq = ss.read(4)
                        # qqq = int.from_bytes(qqq, byteorder='big')
                        # print("Index colour: " + str(qqq))
                        #
                        # qqq = ss.read(4)
                        # qqq = int.from_bytes(qqq, byteorder='big')
                        # print("Bin len: " + str(qqq))
                        #
                        #
                        # self.has_picture = True
                        # self.picture = ss.read(qqq)
                        #
                        # print(ss.read(100))
                        #
                        # #print(self.picture)
                        #
                        # print("HAS PICTURE")
                        # #print(self.picture)
                        # # print(len(data))
                        # with open('test.jpg', 'wb') as w:
                        #     w.write(self.picture)
                        #
                        # # print(ss.read(50))
                        # # ss.seek(0)
                        # # print(struct.unpack('>i4s8s', ss.read(16)))
                        # #
                        # # print(ss)

                    elif a == "discnumber":
                        self.disc_number = b.decode("utf-8")
                    elif a == 'disctotal' or a == 'totaldiscs':
                        self.disc_total = b.decode("utf-8")
                    elif a == 'lyrics' or a == 'unsyncedlyrics':
                        self.lyrics = b.decode("utf-8")
                    else:
                        print("Tag Scanner: Found unhandled Vorbis comment field: " + a)
                        print(b.decode("utf-8"))

                    break

        # Find the last Ogg page from end of file to get track length
        f.seek(-1, 2)

        # Crudely seek back for it
        g = 100000
        while g > 0:
            if f.tell() < 10:
                break
            g -= 1
            f.seek(-5, 1)
            s = f.read(4)

            if s == b"OggS":
                f.seek(-4, 1)
                header = struct.unpack('<4sBBqIIiB', f.read(27))
                self.length = header[3] / 48000

                break



# file = 'a.ogg'
#
# item = Opus(file)
# item.read()



class Ape:

    def __init__(self, file):

        self.filepath = file
        self.has_picture = False
        self.picture = ""

        self.album_artist = ""
        self.artist = ""
        self.genre = ""
        self.date = ""
        self.comment = ""
        self.album = ""
        self.track_number = ""
        self.track_total = ""
        self.title = ""
        self.encoder = ""
        self.disc_number = ""
        self.disc_total = ""
        self.picture = ""
        self.lyrics = ""
        self.label = ""

        self.sample_rate = 48000
        self.bit_rate = 0
        self.length = 0

    def read(self):

        a = open(self.filepath, 'rb')

        # Check size of file
        a.seek(0, 2)
        file_size = a.tell()

        # Helpful: http://wiki.hydrogenaud.io/index.php?title=APEv2_specification

        # Get last 32 bytes where ape tag footer might be
        a.seek(-32, 1)
        b = a.read(32)
        footer = struct.unpack('<8c6i', b)

        # For use later
        found = 1

        # If its not an ape footer, seek through the file for a bit to see if we find it
        if b"".join(footer[0:8]) != b'APETAGEX':
            found = False
            a.seek(0, 2)
            g = 1000
            while g > 0:
                if a.tell() < 1000:
                    break
                g -= 1
                a.seek(-9, 1)
                s = a.read(8)

                # Found it
                if s == b"APETAGEX":
                    found = 2
                    a.seek(-8, 1)
                    b = a.read(32)
                    footer = struct.unpack('<8c6i', b)

        if found == 0:
            print("Tag Scanner: Cant find APE tag")
        else:

            tag_len = footer[9]  # The size of the tag data (excludes header)
            num_items = footer[10]  # Number of fields in tag

            # print("Tag len: " + str(tag_len))
            # print("Items: " + str(num_items))

            # Seek to start of tag (after any header)
            if found == 1:
                a.seek(tag_len * -1, 2)
            else:
                a.seek(8 + (tag_len * -1), 1)

            # For every field in tag
            for q in range(num_items):

                # (field value length, 0=text 2=binary)
                ta = struct.unpack("<ii", a.read(8))

                # Collect every character until we reach null terminator
                name = b""
                for i in range(100):
                    ch = a.read(1)
                    if ch == b"\x00":
                        break
                    name += ch

                key = name.decode('utf-8')
                # print("Key: " + key)

                value = a.read(ta[0])
                # print(value)

                if ta[1] == 0:
                    value = value.decode('utf-8')
                elif ta[1] == 2:
                    # Avoid decode of binary data
                    pass

                # Fill in the class attributes
                if key.lower() == "title":
                    self.title = value
                elif key.lower() == "artist":
                    self.artist = value
                elif key.lower() == "genre":
                    self.genre = value
                elif key.lower() == "disc":

                    # Ape tags appear to use fraction format 1/10, rather than separate fields for number and total
                    # So we need to handle that
                    if "/" in value:
                        self.disc_number, self.disc_total = value.split('/')
                    else:
                        self.disc_number = value

                elif key.lower() == "comment":
                    self.comment = value
                elif key.lower() == "track":

                    # Same deal as disc number/total
                    if "/" in value:
                        self.track_number, self.track_total = value.split('/')
                    else:
                        self.track_number = value

                elif key.lower() == "year":
                    self.date = value
                elif key.lower() == "album":
                    self.album = value
                elif key.lower() == "artist":
                    self.artist = value
                elif key.lower() == "album artist":
                    self.album_artist = value
                elif key.lower() == "label":
                    self.label = value
                elif key.lower() == "lyrics":
                    self.lyrics = value
                elif key.lower() == "cover art (front)":

                    # Data appears to have a filename at the start of it, we need to remove to recover a valid picture
                    # Im not sure what the actual specification is here

                    off = 0
                    while off < 64:
                        if value[off:off+1] == b'\x00':

                            off += 1
                            break
                        off += 1
                    else:
                        print("Tag Scanner: Error reading APE album art")
                        continue

                    self.picture = value[off:]
                    self.has_picture = True
                    # print(value)

        # Back to start of file to see if we can find sample rate and duration information
        a.seek(0)

        start = a.read(128)
        if start[0:3] == b'MAC':  # Ape files start with MAC

            version = struct.unpack("<h", start[4:6])[0]
            if version > 3980:

                audio_info = struct.unpack("<IIIHHI", start[56:76])
                # print(audio_info)

                self.sample_rate = audio_info[5]

                frames = audio_info[2] - 1
                blocks = audio_info[0]

                self.length = (frames * blocks) / self.sample_rate
            else:
                print("WARNING: Old APE codec version; not supported")

        elif '.wv' in self.filepath:
            #  We can handle WavPack files too here
            #  This code likely wont cover all cases as it is, I only tested it on a few files

            a.seek(0)

            #  I found that some WavPack files have padding and/or id3 tags at the beginning
            #  So here I crudely search for the actual start
            off = 0
            while off < file_size - 100:
                if a.read(4) == b'wvpk':
                    a.seek(-4, 1)
                    b = a.read(32)
                    header = struct.unpack("<4cIH2B5I", b)
                    # print(header)

                    sample_rates = [6000, 8000, 9600, 11025, 12000, 16000, 22050, 24000, 32000, 44100, 48000, 64000,
                                    88200, 96000, 192000]   # Adapted from example in WavPack/cli/wvparser.c
                    n = ((header[11] & (15 << 23)) >> 23)   # Does my head in this
                    self.sample_rate = sample_rates[n]
                    self.length = header[8] / self.sample_rate
                    break
            else:
                print("Tag Scanner: Cannot verify WavPack file")

        else:
            print("Tag Scanner: Does not appear to be an APE file")



# file = 'test2.wv'
#
# item = Ape(file)
# item.read()
