"""
game_2.py - 딸기당근수박참외메론 게임
방식: 원래 룰 재현
  순서는 정해져 있음 : 딸기 → 당근 → 수박 → 참외 → 메론 → (반복)
  라운드마다 과일이 하나씩 누적되고(딸기 / 딸기당근 / 딸기당근수박 ...),
  '제한시간' 안에 누적된 순서를 붙여서 입력해야 한다.
  틀리거나 시간을 넘길 때까지 계속 진행 → 걸리면 벌주

  ★ 통과한 라운드는 답을 가려서(●) 컨닝 방지
  ★ 틀려서 걸린 라운드는 답을 그대로 남겨 어디서 틀렸는지 확인 가능
"""

import time
import os
import random

# 정해진 순서
FRUITS = ["딸기", "당근", "수박", "참외", "메론"]

# 제한시간 계산용 (난이도 조절)
BASE_TIME = 1.5        # 기본 여유 시간
TIME_PER_FRUIT = 1.2   # 과일 한 개당 추가되는 시간

COM_FAIL_RATE = 0.3


def enable_ansi():
    """윈도우 콘솔에서 ANSI 이스케이프 코드 활성화 (Git Bash/VS Code 터미널 대응)"""
    if os.name == "nt":
        os.system("")


def mask_last_line(fruit_count):
    print("\033[F\033[2K ▶ " + "●" * fruit_count + "  (입력 완료)")


def build_sequence(length):
    return [FRUITS[i % len(FRUITS)] for i in range(length)]


def play_human(current_player):
    enable_ansi()
    print("=" * 48)
    print("        🍓 딸기당근수박참외메론 게임 🍉")
    print("=" * 48)
    print(" 순서는 정해져 있어요: 딸기 → 당근 → 수박 → 참외 → 메론 → (반복)")
    print(" 라운드마다 과일이 하나씩 늘어납니다.")
    print(" 누적된 순서를 '제한시간 안에' 이어서 입력하세요!")
    print(" (띄어써도 되고 붙여써도 됨 / 예: 딸기당근수박 / 딸기 당근 수박)")
    print(" 걸릴 때까지 계속됩니다! 키보드 한글 입력 상태인지 확인!!")
    print("=" * 48)
    input(" 준비되면 Enter! ")

    round_num = 1

    while True:
        sequence = build_sequence(round_num)
        answer = "".join(sequence)                      
        answer_view = " ".join(sequence)                 
        limit = BASE_TIME + TIME_PER_FRUIT * round_num   

        print(f"\n[{round_num}라운드] 과일 {round_num}개!  (제한시간 {limit:.1f}초)")
        print(" 시작! 순서대로 입력하고 Enter ▼")

        start = time.time()
        user = input(" ▶ ").strip().replace(" ", "")
        elapsed = time.time() - start

        # 1) 답이 틀린 경우 → 걸림
        if user != answer:
            print(" ❌ 땡! 틀렸어요.")
            print(f" 정답 → {answer_view}")
            print(f"🍺 {current_player}, 벌주 1잔 원샷!")
            return {current_player: 1}

        # 2) 답은 맞지만 시간을 넘긴 경우 → 걸림
        if elapsed > limit:
            print(f" ⏰ 시간초과! ({elapsed:.1f}초 걸림 / 제한 {limit:.1f}초)")
            print(f"🍺 {current_player}, 벌주 1잔 원샷!")
            return {current_player: 1}

        # 3) 통과한 경우에만 방금 친 답을 가림 → 다음 라운드로
        mask_last_line(round_num)
        print(f" ✅ 통과! ({elapsed:.1f}초)  다음 라운드로~")
        round_num += 1


def play_computer(current_player):
    """컴퓨터가 플레이하는 버전 (입력 없이 확률로 자동 진행)"""
    print("=" * 48)
    print(f"   🤖 {current_player}(이)가 딸기당근수박참외메론 게임 도전!")
    print("=" * 48)
 
    round_num = 1
    while True:
        sequence = build_sequence(round_num)
        answer_view = " ".join(sequence)
        print(f" [{round_num}라운드] {current_player}: \"{answer_view}\"")
        time.sleep(0.4)
 
        # 확률로 이번 라운드에서 걸리는지 판정
        if random.random() < COM_FAIL_RATE:
            print(f" ❌ {current_player}, 삐끗! 걸렸습니다!")
            print(f"🍺 {current_player}, 벌주 1잔 원샷!")
            return {current_player: 1}
 
        round_num += 1
 
 
def play(current_player, others, user_name):
    if current_player == user_name:
        # 진짜 사람 → 실제로 입력 받아 플레이
        return play_human(current_player)
    else:
        # 컴퓨터 → 입력 없이 확률로 자동 처리
        return play_computer(current_player)
    

# 단독 실행 테스트용
if __name__ == "__main__":
    # 사람으로 테스트: current_player == user_name
    print(play("지연", ["보민", "현민"], "지연"))
    # 컴퓨터로 테스트하려면 아래 주석 해제:
    # print(play("보민", ["지연", "현민"], "지연"))