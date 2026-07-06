import pyfiglet
import random, time

LINES = {
  "1호선": {"온수", "오류동", "개봉", "구일", "구로", "가산디지털단지", "독산",
            "금천구청", "신도림", "영등포", "신길", "대방", "노량진", "용산",
            "남영", "서울역", "시청", "종각", "종로3가", "종로5가", "동대문",
            "동묘앞", "신설동", "제기동", "청량리", "회기", "외대앞", "신이문",
            "석계", "광운대", "월계", "녹천", "창동", "방학", "도봉", "도봉산"
            },
  "2호선": {"까치산", "신정네거리", "양천구청", "도림천", "신도림", "대림",
            "구로디지털단지", "신대방", "신림", "봉천", "서울대입구", "낙성대",
            "사당", "방배", "서초", "교대", "강남", "역삼", "선릉", "삼성",
            "종합운동장", "잠실새내", "잠실", "잠실나루", "강변", "구의", "건대입구",
            "성수", "용답", "신답", "용두", "신설동", "뚝섬", "한양대", "왕십리",
            "상왕십리", "신당", "동대문역사문화공원", "을지로4가", "을지로3가",
            "을지로입구", "시청", "충정로", "아현", "이대", "신촌", "홍대입구",
            "합정", "당산", "영등포구청", "문래"
            },
  "3호선": {"구파발", "연신내", "불광", "녹번", "홍제", "무악재", "독립문",
            "경복궁", "안국", "종로3가", "을지로3가", "충무로", "동대입구",
            "약수", "금호", "옥수", "압구정", "신사", "잠원", "고속터미널",
            "교대", "남부터미널", "양재", "매봉", "도곡", "대치", "학여울",
            "대청", "일원", "수서", "가락시장", "경찰병원", "오금"
          },
  "4호선": {"남태령", "사당", "이수", "동작", "이촌", "신용산", "삼각지",
            "숙대입구", "서울역", "회현", "명동", "충무로", "동대문역사문화공원", "동대문",
            "혜화", "한성대입구", "성신여대입구", "길음", "미아사거리", "미아", "수유",
            "쌍문", "창동", "노원", "상계", "불암산"
          },
  "5호선": {"방화", "개화산", "김포공항", "송정", "마곡", "발산", "우장산", "화곡",
            "까치산", "신정", "목동", "오목교", "양평", "영등포구청", "영등포시장",
            "신길", "여의도", "여의나루", "마포", "공덕", "애오개", "충정로", "서대문",
            "광화문", "종로3가", "을지로4가", "동대문역사문화공원", "청구", "신금호",
            "행당", "왕십리", "마장", "답십리", "장한평", "군자", "아차산", "광나루",
            "천호", "강동", "길동", "굽은다리", "명일", "고덕", "상일동", "강일", "둔촌동",
            "올림픽공원", "방이", "오금", "개롱", "거여", "마천"
          },
  "6호선": {"구산", "연신내", "독바위", "불광", "역촌", "응암", "새절", "증산",
            "디지털미디어시티", "월드컵경기장", "마포구청", "망원", "합정", "상수",
            "광흥창", "대흥", "공덕", "효창공원앞", "삼각지", "녹사평", "이태원", "한강진",
            "버티고개", "약수", "청구", "신당", "동묘앞", "창신", "보문", "안암", "고려대",
            "월곡", "상월곡", "돌곶이", "석계", "태릉입구", "화랑대", "봉화산", "신내"
          },
  "7호선": {"온수", "천왕", "가산디지털단지", "남구로", "대림", "신풍", "보라매", "신대방삼거리",
            "장승배기", "상도", "숭실대입구", "남성", "이수", "내방", "고속터미널", "반포", "논현",
            "학동", "강남구청", "청담", "자양", "건대입구", "어린이대공원", "군자", "중곡",
            "용마산", "사가정", "면목", "상봉", "중화", "먹골", "태릉입구", "공릉", "하계", "중계",
            "노원", "마들", "수락산", "도봉산"
          },
  "8호선": {"복정", "장지", "문정", "가락시장", "송파", "석촌", "잠실", "몽촌토성",
            "강동구청", "천호", "암사", "암사역사공원"
          },
  "9호선": {"개화", "김포공항", "공항시장", "신방화", "마곡나루", "양천향교", "가양",
            "증미", "등촌", "염창", "신목동", "선유도", "당산", "국회의사당", "여의도",
            "샛강", "노량진", "노들", "흑석", "동작", "구반포", "신반포", "고속터미널",
            "사평", "신논현", "언주", "선정릉", "삼성중앙", "봉은사", "종합운동장", "삼전",
            "석촌고분", "석촌", "송파나루", "한성백제", "올림픽공원", "둔촌오륜", "중앙보훈병원"
          },
}
LINE_NAMES = [f"{i}호선" for i in range (1,10)]


BASE_FAIL_RATE = 0    #npc가 틀릴 확률 = 기본 10%
FAILSTEP = 0.01       #한바퀴 돌때마다 5%씩 상승
TRANSFER_LIMIT = 10   #10번동안 환승 안하면 npc가 강제 환승



# 입력된 역이 지나는 호선들의 집합 - 2개 이상이면 환승역
def lines_of(station):
  return {line for line in LINE_NAMES if station in LINES[line]}

# 환승역 판단
def is_transfer_station(station):
  return station is not None and len(lines_of(station)) >= 2

# 호선 입력
def line_input():
  while True:
    line = input().strip().replace("호선", "")
    if not line.isdigit():
      print('1~9 사이의 숫자를 입력해주세요!')
      continue
    line = int(line)
    if not 1 <= line <= 9:
      print('1~9 사이로 입력해주세요!')
      continue
    return f"{line}호선"

# 플레이어가 환승역 선택
def choose_transfer_line(who, station, target_lines):
  target_list = sorted(target_lines)
  if len(target_list) == 1:
    return target_list[0]
  while True:
    raw = input(f"'{station}'에서 어느 호선으로? {target_list}: ").strip()
    line = raw if raw.endswith("호선") else f"{raw}호선"
    if line in target_lines:
      return line
    
# 한바퀴 돌았는지 판단
def next_turn(index, n, lap_count):
  index = (index+1)%n
  if index==0:
    lap_count+=1
  return index, lap_count
  

def play(current_player, others):
  players = [current_player] + list(others)
  n = len(players)
  used = set()
  current_station = None
  index = 0   #지금 차례인 참가자 인덱스 : 기본은 플레이어
  lap_count = 0   #몇바퀴 돌았는지
  transfer_counter=0    #마지막 환승 이후 턴 수
  
  print('====================================================================')
  print(pyfiglet.figlet_format('SUBWAY GAME', font='doom'), end='')
  print('====================================================================')
  print('🚇지하철~ 지하철! 지하철~ 지하철! 몇호선~ 몇호선! 몇호선~ 몇호선!🚇 : ', end='')
  current_line = line_input()
  print(f"{current_line}~ {current_line}! {current_line}~ {current_line}!")
  
  while True:
    turn_player = players[index]
    # 플레이어 차례
    if turn_player == current_player:
      tokens = input(f"[{current_line}] {turn_player} 차례! 역 이름 "
                    f"(환승하려면 '역이름 환승'): ").strip().split()
      #입력 예외처리
      if not tokens:
        print('역 이름을 입력해주세요!')
        continue
      if tokens[0] =="환승":
        print('현재 호선의 역을 먼저 대주세요!')
        continue
      # replace나 rstrip은 역 이름에 들어가는 "역" 제거 위험 ex)역삼역, 역촌역 ...
      station = tokens[0].removesuffix("역")
      want_transfer = len(tokens) >= 2 and tokens[1] == "환승"
    
      # 플레이어 탈락처리 : 현재 호선 아닐때, 중복일때
      if station not in LINES[current_line]:
        print(f"❌ '{station}'은(는) {current_line} 역이 아닙니다! {turn_player} 탈락!")
        return {turn_player: 1}
      if station in used:
        print(f"❌ '{station}'은(는) 이미 나온 역! {turn_player} 탈락!")
        return {turn_player: 1}
    
      used.add(station)
      current_station = station
    
      # 플레이어가 환승 외쳤을 때 : 환승역인지 확인
      if want_transfer:
        if not is_transfer_station(station):
          print(f"❌ '{station}'은(는) 환승역이 아닙니다! {turn_player} 탈락!")
          return {turn_player: 1}
        target_lines = lines_of(station) - {current_line}
        current_line = choose_transfer_line(current_player, station, target_lines)
        print(f"🔄 {current_line}으로 환승~ 🔄")
        transfer_counter = 0
        index, lap_count = next_turn(index, n, lap_count)
        continue
    # NPC 차례
    else:
      fail_rate = BASE_FAIL_RATE + FAILSTEP*lap_count # 턴 늘어날 수록 실패확률 증가
      candidates = LINES[current_line] - used
      
      # 실패확률 or 남은 역 없을 때 : NPC 탈락
      if random.random() < fail_rate or not candidates:
        print(f"❌ {turn_player}이(가) 역을 대지 못하고 탈락!")
        return {turn_player: 1}
      
      # 마지막 환승으로부터 10번 지나면 자동 환승
      if transfer_counter >= TRANSFER_LIMIT:
        transfer_stations = [s for s in candidates if is_transfer_station(s)]
        if transfer_stations:
          station = random.choice(transfer_stations)
          used.add(station)
          current_station = station
          print(f"{turn_player} : {station}")
          target_lines = lines_of(station) - {current_line}
          current_line = random.choice(list(target_lines))
          print(f"🔄 {current_line}으로 환승~ 🔄")
          transfer_counter = 0
          index, lap_count = next_turn(index, n, lap_count)
          continue
      
      # 일반 답변
      answer = random.choice(list(candidates))
      used.add(answer)
      current_station = answer
      time.sleep(random.uniform(0.7, 1.5))
      print(f"{turn_player} : {answer}")
    
    # 한 턴 종료
    transfer_counter+=1
    index, lap_count = next_turn(index, n, lap_count)