import json
import posix

def write_to_pipe(write_pipe_name, data):
    fifo_fd = posix.open(write_pipe_name, posix.O_WRONLY)
    json_data = json.dumps(data).encode()
    posix.write(fifo_fd, json_data)
    posix.close(fifo_fd)

data = {
    "sendKillSig": False,
    "setBuzzer": False,
    "setSpeaker": False,
    "setBootloader": False,
    "setFlash": 0,
    "setDias": 0,
    "setIndicatorLED": [0,100,60,0]
}

write_pipe_name = "/tmp/io_conf"
write_to_pipe(write_pipe_name, data)