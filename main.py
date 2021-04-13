import re

REQUEST_TYPE = "GET"
REQUEST_STATUS_FROM: int = 200
REQUEST_STATUS_TO: int = 400
HOUR_START: int = 2
MINUTE_START: int = 19
SECOND_START: int = 30
HOUR_END: int = 11
MINUTE_END: int = 9
SECOND_END: int = 29

if __name__ == "__main__":
    try:
        with open("access.log.txt", "r") as file:
            list_of_lines = file.readlines()
    except FileNotFoundError:
        print("File was not found.")
        exit()

    counter_of_lines: int = 0
    for line in list_of_lines:
        is_request_success = False
        is_requested_time = False
        is_request_type_suitable = False

        # Checking if request type is suitable
        request_type_check = re.search(r'\s\"(\w+)', line)
        if request_type_check:
            request_type = request_type_check.group(1)
            if request_type == REQUEST_TYPE:
                is_request_type_suitable = True

        # Checking if request is succeed
        request_status_str = re.search(r'\s\d{3}\s', line)
        if request_status_str:
            request_status_int = int(request_status_str.group())
            if REQUEST_STATUS_FROM <= request_status_int < REQUEST_STATUS_TO:
                is_request_success = True

        # Checking if request is in suitable time range
        full_time = re.findall(r'\d{2}/\w{3}/\d{4}:(\d{2}:\d{2}:\d{2})', line)
        is_hour_suitable = False
        is_minute_suitable = False
        is_second_suitable = False

        if HOUR_START <= int(full_time[0][:2]) <= HOUR_END:
            is_hour_suitable = True

        if HOUR_START < int(full_time[0][:2]) < HOUR_END:
            is_minute_suitable = True
        elif int(full_time[0][:2]) == HOUR_START:
            if int(full_time[0][3:5]) >= MINUTE_START:
                is_minute_suitable = True
        elif int(full_time[0][:2]) == HOUR_END:
            if int(full_time[0][3:5]) <= MINUTE_END:
                is_minute_suitable = True
        else:
            is_minute_suitable = False

        if HOUR_START < int(full_time[0][:2]) < HOUR_END:
            is_second_suitable = True
        elif int(full_time[0][:2]) == HOUR_START and int(full_time[0][3:5]) > MINUTE_START:
            is_second_suitable = True
        elif int(full_time[0][:2]) == HOUR_START and int(full_time[0][3:5]) == MINUTE_START:
            if int(full_time[0][2:]) >= SECOND_START:
                is_second_suitable = True
        elif int(full_time[0][:2]) == HOUR_END and int(full_time[0][3:5]) < MINUTE_END:
            is_second_suitable = True
        elif int(full_time[0][:2]) == HOUR_END and int(full_time[0][3:5]) == MINUTE_END:
            if int(full_time[0][2:]) <= SECOND_END:
                is_second_suitable = True

        if is_hour_suitable and is_minute_suitable and is_second_suitable:
            is_requested_time = True

        # Checking if all conditions are 'True'
        if is_request_type_suitable and is_request_success and is_requested_time:
            counter_of_lines += 1

    print("Number of all " + REQUEST_TYPE + " requests with status code from " + str(REQUEST_STATUS_FROM) + " to " +
          str(REQUEST_STATUS_TO) + " that were executed in the time range of " + str(HOUR_START) + ":" +
          str(MINUTE_START) + ":" + str(SECOND_START) + " to " + str(HOUR_END) + ":" + str(MINUTE_END) + ":" +
          str(SECOND_END) + ":\n" + str(counter_of_lines))
