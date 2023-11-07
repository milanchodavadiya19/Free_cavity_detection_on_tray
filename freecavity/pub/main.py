import argparse
import zmq
import time
# Import Module
import os

# Folder Path
path = "/app/sample"

# Change the directory
os.chdir(path)

# Read text File
already_read = []

time.sleep(10)
def publisher(ip="0.0.0.0", port=5551):
    # ZMQ connection
    url = "tcp://{}:{}".format(ip, port)
    print("Going to connect to: {}".format(url))
    ctx = zmq.Context()
    socket = ctx.socket(zmq.PUB)
    socket.connect(url)  # publisher connects to subscriber
    print("Pub connected to: {}\nSending data...".format(url))
    
    i = 0

    while True:
        topic = 'foo'.encode('ascii')
        # msg = 'test {}'.format(i).encode('ascii')

        # iterate through all file
        for file in os.listdir():
            # Check whether file is in text format or not
            if file.endswith(".tif"):
                file_path = f"{path}/{file}"

                # call read text file function
                if file_path not in already_read:
                    already_read.append(file_path)
                    with open(file_path, 'rb') as f:
                        size = os.stat(file_path).st_size
                        content = f.read(size)
                        if f:
                            # publish data
                            # socket.send_multipart([topic, content])  # 'test'.format(i)
                            socket.send(content)
                            print("On topic {}, send data: {}".format(topic, content[0:50]))
                            time.sleep(10)
        i += 1


if __name__ == "__main__":
    # command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=argparse.SUPPRESS,
                        help="IP of (Docker) machine")
    parser.add_argument("--port", default=argparse.SUPPRESS,
                        help="Port of (Docker) machine")

    args, leftovers = parser.parse_known_args()
    print("The following arguments are used: {}".format(args))
    print("The following arguments are ignored: {}\n".format(leftovers))

    # call function and pass on command line arguments
    publisher(**vars(args))
