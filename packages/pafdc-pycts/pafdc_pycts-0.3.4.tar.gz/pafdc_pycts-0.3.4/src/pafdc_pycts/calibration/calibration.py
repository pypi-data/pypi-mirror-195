from pafdc_pycts.connect import Connect
from waiting import wait
import csv
import time
import threading

# Configurations
NUMBER_OF_CONNECTIONS = 5
COM_PORT = "COM9"
BEING_TOUCHED_RANGE = [0, 90, 90, 90, 90]
LOCATION_OF_CALIBRATION_FILES = "C:/Users/ajr439/Documents/Projects/calibration_files"

cts = Connect(connections=NUMBER_OF_CONNECTIONS, data_method='com', com=COM_PORT).init()
calibration_storage = {}
last_touch_cords = None

a = []
b = []
c = []
d = []
e = []
recording = True


def get_if_touched():
    global a, b, c, d, e
    print(b[-1])
    if len(a) > 0:
        return a[-1] >= BEING_TOUCHED_RANGE[0] \
               and b[-1] >= BEING_TOUCHED_RANGE[1] \
               and c[-1] >= BEING_TOUCHED_RANGE[2] \
               and d[-1] >= BEING_TOUCHED_RANGE[3] \
               and e[-1] >= BEING_TOUCHED_RANGE[4]


def calibrate_for_touch_point(x, y):
    global a, b, c, d, e
    print("Touch at x: " + str(x) + " y: " + str(y))
    wait(lambda: get_if_touched(), timeout_seconds=20, waiting_for="a touch")
    calibration_storage[str(x) + ", " + str(y)] = []
    while get_if_touched():
        calibration_storage[str(x) + ", " + str(y)].append([a[-1], b[-1], c[-1], d[-1], e[-1]])


def store_data_points():
    # Store each x, y data point in individual files in x_y.csv
    for placement in calibration_storage:
        tmp_filename = LOCATION_OF_CALIBRATION_FILES + "/" + placement + ".csv"
        with open(tmp_filename, 'w', newline='', encoding='utf-8') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)
            write.writerow([1, 2, 3, 4, 5])
            print(placement)
            print(calibration_storage)
            write.writerows(calibration_storage[placement])
        print("wrote at " + tmp_filename)


def record_thread():
    global recording, a, b, c, d, e, cts

    while True:
        if recording:
            while cts.size() > 30:
                output_array = cts.get_cords()
                if len(output_array) == 5:
                    float_array = list(map(float, output_array))
                    a.append(float_array[0])
                    b.append(float_array[1])
                    c.append(float_array[2])
                    d.append(float_array[3])
                    e.append(float_array[4])
        else:
            break


if __name__ == "__main__":
    threading.Thread(target=record_thread).start()
    for x in range(0, 4):
        for y in range(0, 4):
            calibrate_for_touch_point(x, y)

    store_data_points()
