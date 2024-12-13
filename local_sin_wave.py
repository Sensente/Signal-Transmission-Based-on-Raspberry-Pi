import queue
import sounddevice as sd
from numpy import *
import numpy as np
import sys
from numpy.fft import fft, ifft, fftshift, ifftshift
import argparse

q = queue.Queue()
local_file = []

class SignalGeneration():
    def __init__(self, N=2400, fc=19000, fs=48000, length=2400):
        self.N = N
        self.fc = fc
        self.fs = fs
        self.length = length

        self.transmitted_data = self.generateMonotonicSignal()

    def generateMonotonicSignal(self):
        t = np.arange(0, self.length) / self.fs
        signal = np.cos(2 * np.pi * self.fc * t)
        return signal

length = 2400
fc = 19000
fs = 48000

monotonic_signal = SignalGeneration(fc=fc, fs=fs, length=length).transmitted_data

mixed_fd = np.zeros([length, ], dtype=complex)
mixed_fd[:] = monotonic_signal[:]
trans_data = (mixed_fd.real / np.max(mixed_fd.real)).astype(np.float32)

def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(indata)

def output_callback(outdata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    outdata[:, 0] = trans_data

global sound_done

def Play(data_id: int, time:int):
    global local_file, sound_done
    parser = argparse.ArgumentParser(add_help=False)
    count = 0
    input_id = 0
    output_id = 0
    device_id = 0
    length = 2400
    for i in sd.query_devices():
        if i['name'][0:5] == 'seeed':
            input_id = device_id
        if i['name'][0:5] == 'ac101':
            output_id = device_id
        device_id += 1
    print(input_id, output_id)
    stream_play = sd.OutputStream(samplerate=48000, blocksize=length, latency=0, channels=1, device=output_id,
                                  callback=output_callback, dtype=np.float32)
    stream_record = sd.InputStream(samplerate=48000, blocksize=length, latency=0, device=input_id,
                                   callback=audio_callback, channels=8, dtype=np.float32)

    try:
        with stream_record, stream_play:
            while count <= time:
                print(count)
                cur_data = q.get()
                local_file.append(cur_data.copy())
                count += 1

                if count > time:
                    local_file = np.array(local_file)
                    print("sound_done!")
                    save_file = []
                    for i in range(len(local_file)):
                        if i < time:
                            save_file.append(local_file[i])
                    save_file = np.array(save_file)
                    print(save_file.shape, save_file.dtype)
                    np.save(str(data_id) + '.npy', save_file)
                    q.queue.clear()
                    break

    except KeyboardInterrupt:
        parser.exit('Interrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))

    finally:
        stream_play.stop()
        stream_play.close()
        stream_record.stop()
        stream_record.close()
        sound_done = True


def only_record(data_id: int, time: int):
    global local_file, sound_done
    parser = argparse.ArgumentParser(add_help=False)
    input_id = 0
    output_id = 0
    device_id = 0
    length = 2400 * 1
    for i in sd.query_devices():
        if i['name'][0:5] == 'seeed':
            input_id = device_id
        if i['name'][0:5] == 'ac101':
            output_id = device_id
        device_id += 1

    try:
        with stream_record:
            while count <= time:
                print(count)
                cur_data = q.get()
                local_file.append(cur_data.copy())
                count += 1

                if count > time:
                    print("sound_done!")
                    local_file = np.array([local_file[i] for i in range(len(local_file)) if i < 50])
                    print(local_file.shape, local_file.dtype)
                    np.save(str(data_id) + '.npy', local_file)
                    q.queue.clear()
                    break

    except KeyboardInterrupt:
        parser.exit('Interrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))

    finally:
        stream_record.stop()
        stream_record.close()
        sound_done = True
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--data_id", help='data_id will be saved')
    parser.add_argument("-t", "--time", help='Record time, calculated by t/fs/length')

    args = parser.parse_args()
    data_id = int(args.data_id)
    t = int(args.time)

    sound_done = False
    
    while(1):
        Play(data_id, t)
        if sound_done:
            break
