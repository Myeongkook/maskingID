# 주민등록번호를 마스킹하자 - Python

---

### why?

개인정보호법의 개정으로 기업에서 개인의 주민등록번호 뒷자리를 수집하면 안된다.그럼에도 불구하고 마스킹 처리 없이 서류를 업로드 하는 고객도 존재한다.
이때문에 담당자는 서류를 일일이 확인해야 하는 번거로움이 생겼고, 이를 해소하기 위하여 프로그램을 기획하게 되었다.

### how?

OCR 기능을 사용하여 사용자가 올린 이미지(jpg, png)를 인식, openCV 모듈을 사용하여
마스킹 처리한다.

---

```python
def callAPI(file_path):
    with open('key.yml') as f:
        key = yaml.load(f, Loader=yaml.FullLoader)
        a = key['secret']['a']
        b = key['secret']['b']
    api_url = a
    secret_key = b
    image_file = file_path
    try:
        with open(image_file, 'rb') as f:
            file_data = f.read()
    except FileNotFoundError:
        return False
    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'img',
                'data': base64.b64encode(file_data).decode()
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }
    payload = json.dumps(request_json).encode('UTF-8')
    headers = {
        'X-OCR-SECRET': secret_key,
       'Content-Type': 'application/json'
    }
    response = requests.
								request("POST", api_url, headers=headers, data=payload)
    return response
```

API key는 Github에 개인 API Key를 공개할 수 없기 때문에 별도의 yml파일로 관리하였다

위와 같이 이미지 파일을 API에 요청하면 인식된 결과를 Json 타입으로 응답받게 된다.

---

```python
def maskingImage(json_data, path):
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
            if int(s_i_n[6]) == 5 or int(s_i_n[6]) == 6:
                parity_check = parity_check + 2
            if (int(s_i_n[-1]) == parity_check and 0 < int(s_i_n[6]) < 7 and int(
                    s_i_n[4] + s_i_n[
                        5]) < 32) or (int(s_i_n[0]) == 2 and int(s_i_n[6]) < 2):  # 패리티체크에 성공하고, 7번째 자리수가 6이하(외국인 주민번호 포함), 5~6번째 값이 31일 이하 인경우 주민번호로 판단
                coordinates = [
                    json_data['images'][0]['fields'][i]['boundingPoly'][
                        'vertices']]
            else:
                raise ValueError
            if abs(coordinates[0][0]['x'] - coordinates[0][2]['x']) > abs(
                    coordinates[0][0]['y'] - coordinates[0][2]['y']):
                coordinates_50_percentage = (coordinates[0][0]['x'] +
                                             coordinates[0][2]['x']) / 2
                time.sleep(2)
                im = cv2.imread(path)
                cv2.rectangle(im, (
                    int(coordinates_50_percentage),
                    int(coordinates[0][0]['y'] - 10)), (
                                  int(coordinates[0][2]['x']),
                                  int(coordinates[0][2]['y'] + 10)),
                              (255, 0, 0), -1)
                try:
                    cv2.imwrite(path, im)
                    success_check += 1
                except cv2.error as e:
                    return 1
            elif abs(coordinates[0][0]['x'] - coordinates[0][2]['x']) < abs(
                    coordinates[0][0]['y'] - coordinates[0][2]['y']):
                coordinates_50_percentage = (coordinates[0][0]['y'] +
                                             coordinates[0][2]['y']) / 2
                time.sleep(2)
                im = cv2.imread(path)
                if coordinates[0][0]['x'] - coordinates[0][2]['x'] > 0:
                    cv2.rectangle(im, (
                        int(coordinates[0][0]['x'] + 10),
                        int(coordinates_50_percentage)), (
                                      int(coordinates[0][2]['x'] - 10),
                                      int(coordinates[0][2]['y'])), (255, 0, 0),
                                  -1)
                else:
                    cv2.rectangle(im, (
                        int(coordinates[0][0]['x'] - 10),
                        int(coordinates_50_percentage)), (
                                      int(coordinates[0][2]['x'] + 10),
                                      int(coordinates[0][2]['y'])), (255, 0, 0),
                                  -1)
                try:
                    cv2.imwrite(path, im)
                    success_check += 1
                except cv2.error as e:
                    return 1
            else:
                pass
```

위 과정에서 응답받은 Json 한 블럭씩 주민등록번호 패리티체크를 한 뒤, 적합한 경우 해당 블럭의
좌표를 토대로 주민등록번호 뒷자리에 해당되는 범위만 마스킹처리를 하게 된다.

이미지의 방향을 가로, 세로 구분하여 마스킹하는 방향을 나누었다.

---

Python 코드 그대로 사용하기 좋지 않다고 생각되어 Tkinter GUI를 사용하여 코드를 알지 못해도 이 프로그램을 사용할 수 있도록 디자인하였다. 

![Tkinter 모듈을 사용하여 만든 GUI - 기본적인 틀만 만들어진 형태](%E1%84%8C%E1%85%AE%E1%84%86%E1%85%B5%E1%86%AB%E1%84%83%E1%85%B3%E1%86%BC%E1%84%85%E1%85%A9%2000d71/Screen_Shot_2021-04-11_at_23.41.26.png)

Tkinter 모듈을 사용하여 만든 GUI - 기본적인 틀만 만들어진 형태

파일 또는 폴더를 불러와 마스킹처리하고 처리가 끝난 후 리스트를 비우도록 하였다.

![Tkinter 모듈을 사용하여 만든 GUI - 여러 파일을 추가하여 일괄처리할 수 있다.](%E1%84%8C%E1%85%AE%E1%84%86%E1%85%B5%E1%86%AB%E1%84%83%E1%85%B3%E1%86%BC%E1%84%85%E1%85%A9%2000d71/Screen_Shot_2021-04-11_at_23.44.27.png)

Tkinter 모듈을 사용하여 만든 GUI - 여러 파일을 추가하여 일괄처리할 수 있다.

![프로그램을 사용한 결과 - 스캔한 이미지의 결과물](%E1%84%8C%E1%85%AE%E1%84%86%E1%85%B5%E1%86%AB%E1%84%83%E1%85%B3%E1%86%BC%E1%84%85%E1%85%A9%2000d71/Screen_Shot_2021-04-11_at_23.59.58.png)

프로그램을 사용한 결과 - 스캔한 이미지의 결과물

![프로그램을 사용한 결과 - 스마트폰으로 촬영한 이미지의 결과물](%E1%84%8C%E1%85%AE%E1%84%86%E1%85%B5%E1%86%AB%E1%84%83%E1%85%B3%E1%86%BC%E1%84%85%E1%85%A9%2000d71/Screen_Shot_2021-04-13_at_20.00.09.png)

프로그램을 사용한 결과 - 스마트폰으로 촬영한 이미지의 결과물

위와 같이 스캐너로 스캔한 이미지는 물론 회전돼있거나 비스듬한 이미지도 유의미한 결과를 보여준다.

---
