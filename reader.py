# Library to read and write on .wav files


def wavreader(d):
    """ Reads .wav files and saves data in a dictionary.
        Only works for two channels.
        
        d: directory of the .wav file
        returns: dictionary with 'riff', 'fmt' and 'data' """

    with open(d, "rb") as f:
        raw = f.read()

    # creates the dictionary with data
    dic = {
        "riff": {
            "ChunkID": raw[:4].decode("ascii"),
            "ChunkSize": int.from_bytes(raw[4:8], "little"),
            "format": raw[8:12].decode("ascii")
        },
        "fmt": {
            "SubChunk1ID": raw[12:16].decode("ascii"),
            "SubChunk1Size": int.from_bytes(raw[16:20], "little"),
            "AudioFormat": int.from_bytes(raw[20:22], "little"),
            "NumChannels": int.from_bytes(raw[22:24], "little"),
            "SampleRate": int.from_bytes(raw[24:28], "little"),
            "ByteRate": int.from_bytes(raw[28:32], "little"),
            "BlockAlign": int.from_bytes(raw[32:34], "little"),
            "BitsPerSample": int.from_bytes(raw[34:36], "little")
        },
        "data": {
            "SubChunk2ID": raw[36:40].decode("ascii"),
            "SubChunk2Size": int.from_bytes(raw[40:44], "little")
        }
    }

    bytesperframe = int(dic["fmt"]["BitsPerSample"] / 8)

    # creates a list of each channel with data converted into ints
    ch1, ch2 = [], []
    for i in range(len(raw[44:])):
        if i % 4 == 0:
            # a single frame for channel 1
            bytes1 = raw[44+i: 44+i+bytesperframe]
            # a single frame for channel 2
            bytes2 = raw[44+i+bytesperframe: 44+i+(2*bytesperframe)]

            ch1.append(int.from_bytes(bytes1, "little", signed=True))
            ch2.append(int.from_bytes(bytes2, "little", signed=True))

    # saves channels data into the dictionary
    dic["data"]["ch1"] = ch1
    dic["data"]["ch2"] = ch2

    return dic


def wavwriter(data):
    """ Writes .wav files from a dictionary containing data.
        Saves two channel by default.
        
        data: dictionary in the format produced by 'wavreader(d)'
        returns: bytelist containing .wav data """

    # saves all the metadata
    raw = bytes(data["riff"]["ChunkID"], "ascii") + \
        data["riff"]["ChunkSize"].to_bytes(4, byteorder="little") + \
        bytes(data["riff"]["format"], "ascii") + \
        bytes(data["fmt"]["SubChunk1ID"], "ascii") + \
        data["fmt"]["SubChunk1Size"].to_bytes(4, byteorder="little") + \
        data["fmt"]["AudioFormat"].to_bytes(2, byteorder="little") + \
        data["fmt"]["NumChannels"].to_bytes(2, byteorder="little") + \
        data["fmt"]["SampleRate"].to_bytes(4, byteorder="little") + \
        data["fmt"]["ByteRate"].to_bytes(4, byteorder="little") + \
        data["fmt"]["BlockAlign"].to_bytes(2, byteorder="little") + \
        data["fmt"]["BitsPerSample"].to_bytes(2, byteorder="little") + \
        bytes(data["data"]["SubChunk2ID"], "ascii") + \
        data["data"]["SubChunk2Size"].to_bytes(4, byteorder="little")

    # recomposes the sound data according to .wav
    for i in range(len(data["data"]["ch1"])):
        # each channel is temp saved and then merged in a single frame
        b1 = data["data"]["ch1"][i].to_bytes(2, "little", signed=True)
        b2 = data["data"]["ch2"][i].to_bytes(2, "little", signed=True)
        frame = b1 + b2

        raw += frame

    return raw
