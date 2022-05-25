# import requests

# url = 'https://kauth.kakao.com/oauth/token'
# rest_api_key = 'ec6167f7e1f48f114cad1c6350e43212'
# redirect_uri = 'https://example.com/oauth'
# authorize_code = 'YgPWyR1niOUtses_0nWMoPwkKc9UkLks_Nloo2_i7AaA2-fHqzo3tJzKELC_3njVlhCnRAo9cpcAAAGA9VeDAg'

# data = {
#     'grant_type':'authorization_code',
#     'client_id':rest_api_key,
#     'redirect_uri':redirect_uri,
#     'code': authorize_code,
#     }

# response = requests.post(url, data=data)
# tokens = response.json()
# print(tokens)

# # json 저장
# import json
# with open("kakao_code.json","w") as fp:
#     json.dump(tokens, fp)

# import json
# with open("kakao_code.json","r") as fp:
#     ts = json.load(fp)
# print(ts)
# print(ts["access_token"])


# <이상행동 영상데이터-이상행동/상황 정의>
# 0 무단진입            turnstile_trespassing
# 1 출입방향오인        turnstile_wrong_direction
# 2 계단전도            stairway_fall
# 3 기물파손            property_damage
# 4 몰카                spy_camera
# 5 배회                wandering
# 6 실신                fainting
# 7 에스컬레이터 전도   escalator_fall
# 8 유기                unattended
# 9 절도                theft
# 10 주취               public_intoxication
# 11 폭행               assault
# 12 환경전도           surrounding_fall
# classes_dic = { "turnstile_trespassing": 0, "turnstile_wrong_direction": 1, "stairway_fall": 2, \
#     "property_damage": 3, "spy_camera" : 4, "wandering" : 5, "fainting" : 6, \
#     "escalator_fall" : 7, "unattended" : 8, "theft" : 9, "public_intoxication" : 10, \
#     "assault" : 11, "surrounding_fall" : 12 }

# print(classes_dic[0])
import cv2
print(cv2.FONT_HERSHEY_SIMPLEX)
