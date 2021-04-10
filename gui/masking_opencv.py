import cv2


def redactImage(json_data, path):
    success_check = 0
    for i in range(len(json_data['images'][0]['fields'])):
        id_num = json_data['images'][0]['fields'][i]['inferText']
        if '-' in id_num:
            coordinates = []
            replace_num = id_num.replace("-", "")
            if replace_num.isdigit():
                if len(replace_num) != 13:
                    continue
            else:
                continue
            s_i_n = list(replace_num)
            multiple = 2
            total = 0
            for j in range(len(s_i_n) - 1):
                total = total + (int(s_i_n[j]) * multiple)
                multiple += 1
                if multiple > 9:
                    multiple = 2
            parity_check = 11 - (total % 11)
            if parity_check >= 10:
                parity_check = parity_check - 10
            if int(s_i_n[-1]) == parity_check and 0 < int(s_i_n[6]) < 5 and int(
                    s_i_n[4] + s_i_n[5]) < 32:
                for k in range(2):
                    coordinates.append(
                        json_data['images'][0]['fields'][i]['boundingPoly'][
                            'vertices'][k]['x'])
                    coordinates.append(
                        json_data['images'][0]['fields'][i]['boundingPoly'][
                            'vertices'][k]['y'])
            else:
                raise ValueError

            if abs(coordinates[0] - coordinates[2]) > abs(
                    coordinates[1] - coordinates[3]):
                coordinates[0] = (coordinates[0] + coordinates[2]) / 2
                print("isVertical", coordinates)
                im = cv2.imread(path)
                pecentage = int(abs(coordinates[0] - coordinates[2]) * 0.3)
                cv2.rectangle(im, (
                    int(coordinates[0]), int(coordinates[1] - 10)), (
                                  int(coordinates[2]),
                                  int(coordinates[3]) + pecentage), (255, 0, 0),
                              -1)
                try:
                    cv2.imwrite(path, im)
                    success_check += 1
                except cv2.error as e:
                    print(e, "파일 경로에 한글은 입력할 수 없습니다.")
                    return 1
            elif abs(coordinates[0] - coordinates[2]) < abs(
                    coordinates[1] - coordinates[3]):
                coordinates[1] = (coordinates[1] + coordinates[3]) / 2
                print("isNotVertical", coordinates)
                im = cv2.imread(path)
                pecentage = int(abs(coordinates[1] - coordinates[3]) * 0.3)
                cv2.rectangle(im,
                              (int(coordinates[0] - 10), int(coordinates[1])),
                              (int(coordinates[2] + pecentage),
                               int(coordinates[3])),
                              (255, 0, 0), -1)
                try:
                    cv2.imwrite(path, im)
                    success_check += 1
                except cv2.error as e:
                    print(e, "파일 경로에 한글은 입력할 수 없습니다.")
                    return 1
            else:
                pass
    return success_check
