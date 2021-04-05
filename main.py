import re

if __name__ == "__main__":
    REQUEST_TYPE = "GET"
    REQUEST_STATUS_FROM: int = 200
    REQUEST_STATUS_TO: int = 400

    counter_of_lines: int = 0

    with open("access.log.txt", "r") as file:
        list_of_lines = file.readlines()

    for line in list_of_lines:
        is_request_success = False
        is_requested_time = False
        is_request_type_suitable = False

        # Checking if request type is suitable
        if f"\"{REQUEST_TYPE} " in line:
            is_request_type_suitable = True

        # Checking if request is succeed
        for code in range(REQUEST_STATUS_FROM, REQUEST_STATUS_TO, 1):
            if f" {code} " in line:
                is_request_success = True
                break

        # Checking if request is in suitable time range
        full_time = re.findall(r'\d{2}/\w{3}/\d{4}:(\d{2}:\d{2}:\d{2})', line)
        is_hour_suitable = False
        is_minute_suitable = False
        is_second_suitable = False

        if 2 <= int(full_time[0][:2]) <= 11:
            is_hour_suitable = True

        if 2 < int(full_time[0][:2]) < 11:
            is_minute_suitable = True
        elif int(full_time[0][:2]) == 2:
            if int(full_time[0][3:5]) >= 19:
                is_minute_suitable = True
        elif int(full_time[0][:2]) == 11:
            if int(full_time[0][3:5]) <= 9:
                is_minute_suitable = True
        else:
            is_minute_suitable = False

        if 2 < int(full_time[0][:2]) < 11:
            is_second_suitable = True
        elif int(full_time[0][:2]) == 2 and int(full_time[0][3:5]) > 19:
            is_second_suitable = True
        elif int(full_time[0][:2]) == 2 and int(full_time[0][3:5]) == 19:
            if int(full_time[0][2:]) >= 30:
                is_second_suitable = True
        elif int(full_time[0][:2]) == 11 and int(full_time[0][3:5]) < 9:
            is_second_suitable = True
        elif int(full_time[0][:2]) == 11 and int(full_time[0][3:5]) == 9:
            if int(full_time[0][2:]) <= 29:
                is_second_suitable = True

        if is_hour_suitable and is_minute_suitable and is_second_suitable:
            is_requested_time = True

        # Checking if all conditions are 'True'
        if is_request_type_suitable and is_request_success and is_requested_time:
            counter_of_lines += 1

    file.close()
    print(counter_of_lines)
