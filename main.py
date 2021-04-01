import re
import datetime

if __name__ == "__main__":
    REQUEST_TYPE = "GET"
    REQUEST_STATUS_FROM: int = 200
    REQUEST_STATUS_TO: int = 400

    counter_of_lines: int = 0
    all_possible_points_in_time = []

    start_time = datetime.datetime(1111, 1, 1, 2, 19, 30)
    end_time = datetime.datetime(1111, 1, 1, 11, 9, 29)
    delta = datetime.timedelta(seconds=1)

    while start_time <= end_time:
        all_possible_points_in_time.append(*re.findall(r'\d{2}:\d{2}:\d{2}', str(start_time)))
        start_time += delta
    with open("access.log.txt", "r") as file:
        list_of_lines = file.readlines()

    for line in list_of_lines:
        is_request_success = False
        is_requested_time = False
        is_request_type_suitable = False

        if f"\"{REQUEST_TYPE} " in line:
            is_request_type_suitable = True

        for code in range(REQUEST_STATUS_FROM, REQUEST_STATUS_TO, 1):
            if f" {code} " in line:
                is_request_success = True
                break

        for point_of_time in all_possible_points_in_time:
            if f":{point_of_time} " in line:
                is_requested_time = True
                break

        if is_request_type_suitable and is_request_success and is_requested_time:
            counter_of_lines += 1

    file.close()
    print(counter_of_lines)
