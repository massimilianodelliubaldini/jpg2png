import os
import glob
import threading
from PIL import Image

print_lock = threading.Lock()
p = print
def print(*a, **b):
    with print_lock:
        p(*a, **b)

total_lock = threading.Lock()
total = 0
def updtotal():
    global total
    with total_lock:
        total += 1
        return total

def jpg2png_t(files, a, b, num_files):

    for i in range(a, b):        
        file = files[i]

        print('Converting ' + file + '...')
        try:
            out = file.replace('.jpg', '.png').replace('.jpeg', '.png')
            img = Image.open(file)
            png = img.save(out, format='PNG', compress_level=0, interlace=False)
            img.close()
            os.remove(file)
            print('Completed (' + str(updtotal()) + '/' + str(num_files) + ').')
        except:
            print('FAILED (' + file + ').')

def jpg2png(path, num_threads):

    files =  glob.glob(os.path.join(path, '**', '*.jpeg'), recursive=True)
    files += glob.glob(os.path.join(path, '**',  '*.jpg'), recursive=True)

    num_files = len(files)

    files_per_thread = num_files // num_threads
    remainder_files  = num_files %  num_threads
    threads = []

    for i in range(0, num_threads):
        a = i * files_per_thread
        b = a + files_per_thread

        if i == num_threads - 1:
            b += remainder_files

        thread = threading.Thread(None, jpg2png_t, 'Thread ' + str(i), (files, a, b, num_files), {})
        threads.append(thread)
        thread.start()
        print('Created Thread ' + str(i) + '.')

    for i in range(0, num_threads):
        threads[i].join()
        print('Joined Thread ' + str(i) + '.')

    global total
    with total_lock:
        total = 0

def jpeg2png(path, num_threads):
    jpg2png(path, num_threads)