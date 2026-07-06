import random
import time


CATEGORY_NAMES = {
    "어": "물고기",
    "목": "나무",
    "조": "새",
    "동": "동물",
}


CATEGORY_WORDS = {
    "어": set("""
        고등어 갈치 참치 연어 광어 넙치 우럭 상어 복어 조기 멸치
        방어 농어 도미 참돔 돌돔 가자미 청어 전어 숭어 메기 잉어
        붕어 장어 아귀 쥐치 날치 삼치 꽁치 대구 명태 민어 병어
        송어 가물치 미꾸라지 피라미 다랑어 가다랑어 옥돔 볼락
        도루묵 양미리 홍어 가오리 철갑상어 개복치 해마 쏘가리
        산천어 은어 빙어 전갱이 학꽁치
    """.split()),

    "목": set("""
        소나무 은행나무 단풍나무 느티나무 자작나무 버드나무 참나무
        전나무 밤나무 감나무 벚꽃나무 사과나무 배나무 복숭아나무
        매실나무 살구나무 대추나무 호두나무 잣나무 향나무 측백나무
        편백나무 삼나무 주목 회양목 플라타너스 메타세쿼이아
        아까시나무 목련 동백나무 떡갈나무 신갈나무 상수리나무
        굴참나무 졸참나무 가문비나무 구상나무 후박나무 녹나무
        오동나무 뽕나무 느릅나무 팽나무 물푸레나무 이팝나무
        산수유나무 모과나무 석류나무 유자나무 귤나무 야자나무 대나무
    """.split()),

    "조": set("""
        참새 까치 비둘기 독수리 부엉이 까마귀 두루미 제비 갈매기
        백조 앵무새 공작 오리 기러기 황새 타조 펭귄 닭 칠면조
        메추라기 꿩 원앙 딱따구리 매 솔개 수리부엉이 올빼미 종달새
        꾀꼬리 뻐꾸기 직박구리 박새 동박새 물총새 왜가리 해오라기
        저어새 가마우지 펠리컨 홍학 알바트로스 도요새 물떼새
        논병아리 잉꼬 카나리아 문조 참매 새매 검독수리 큰고니 청둥오리
        쇠오리 후투티 파랑새 멧비둘기 뜸부기 쇠백로 소쩍새
    """.split()),

    "동": set("""
        호랑이 사자 코끼리 기린 원숭이 토끼 개 강아지 고양이 여우
        곰 하마 코뿔소 돼지 말 소 양 염소 사슴 노루 고라니 낙타
        라마 알파카 얼룩말 치타 표범 재규어 퓨마 하이에나 늑대
        코요테 너구리 오소리 족제비 수달 담비 몽구스 판다 코알라
        캥거루 왈라비 나무늘보 아르마딜로 개미핥기 미어캣 두더지
        고슴도치 다람쥐 햄스터 비버 카피바라 쥐 박쥐 고릴라 침팬지
        오랑우탄 북극곰 물개 바다사자 바다코끼리 고래 돌고래 범고래
        악어 거북이 자라 이구아나 카멜레온 도마뱀 뱀 코브라 구렁이
        개구리 두꺼비 청개구리 도롱뇽 달팽이 지렁이 거미 전갈 지네
        사마귀 메뚜기 귀뚜라미 나비 나방 잠자리 무당벌레 개미 벌
        장수풍뎅이 사슴벌레 매미 바퀴벌레 모기 파리 반딧불이
    """.split()),
}


ALIASES = {
    "광어": "넙치",
    "아카시아": "아까시나무",
    "백조": "큰고니",
}


LOG_DELAY = 0.2


def show_log(message="", delay=LOG_DELAY):
    """로그를 출력한 뒤 잠깐 멈춰 게임 진행 순서를 보여준다."""
    print(message, flush=True)

    if delay > 0:
        time.sleep(delay)


def normalize_word(word):
    cleaned_word = word.strip().replace(" ", "")
    return ALIASES.get(cleaned_word, cleaned_word)


def choose_target(caller_name, player_names):
    """
    caller_name: 지목자 이름 (str)
    player_names: 전체 참가자 이름 리스트 (list[str])
    반환값: 지목된 사람 이름 (str)
    """
    candidates = [name for name in player_names if name != caller_name]

    if is_user(caller_name):
        show_log(f"[지목] {caller_name}님이 다음 답변자를 선택합니다.", 0.2)
        print(f"지목 가능한 참가자: {', '.join(candidates)}")

        while True:
            target_name = input("다음 답변자 이름: ").strip()

            if target_name in candidates:
                return target_name

            print("지목 가능한 참가자의 이름을 정확히 입력하세요.")

    show_log(f"[지목] {caller_name}이(가) 다음 답변자를 고르는 중...")
    return random.choice(candidates)


def choose_category(caller_name):
    if is_user(caller_name):
        show_log(f"[선택] {caller_name}님이 카테고리를 선택합니다.", 0.2)

        while True:
            category = input("카테고리 입력 (어/목/조/동): ").strip()

            if category in CATEGORY_WORDS:
                return category

            print("어, 목, 조, 동 중 하나만 입력하세요.")

    return random.choice(list(CATEGORY_WORDS.keys()))


def judge_answer(answer, category, used_words, elapsed_time, time_limit):
    normalized_answer = normalize_word(answer)

    if elapsed_time > time_limit:
        return False, "시간 초과", normalized_answer

    if not normalized_answer:
        return False, "빈 답변", normalized_answer

    if normalized_answer in used_words:
        return False, "이미 나온 단어", normalized_answer

    if normalized_answer not in CATEGORY_WORDS[category]:
        return (
            False,
            f"{CATEGORY_NAMES[category]} 카테고리에 없는 단어",
            normalized_answer,
        )

    return True, "정답", normalized_answer


def get_computer_answer(category, used_words, time_limit):
    available_words = [
        word
        for word in CATEGORY_WORDS[category]
        if normalize_word(word) not in used_words
    ]

    if not available_words:
        return "", time_limit + 1

    random_value = random.random()

    # 5% 확률로 시간 초과
    if random_value < 0.05:
        return "", time_limit + random.uniform(0.1, 0.8)

    # 추가 5% 확률로 이미 나온 단어 말하기
    if random_value < 0.10 and used_words:
        answer = random.choice(list(used_words))
        elapsed_time = random.uniform(0.4, min(3.0, time_limit))
        return answer, elapsed_time

    # 추가 5% 확률로 다른 카테고리 단어 말하기
    if random_value < 0.15:
        other_categories = [
            key for key in CATEGORY_WORDS
            if key != category
        ]

        wrong_category = random.choice(other_categories)
        answer = random.choice(list(CATEGORY_WORDS[wrong_category]))
        elapsed_time = random.uniform(0.4, min(3.0, time_limit))

        return answer, elapsed_time

    # 나머지 85% 확률로 정상 답변
    answer = random.choice(available_words)

    max_response_time = max(
        0.8,
        min(3.0, time_limit - 0.1),
    )
    elapsed_time = random.uniform(0.4, max_response_time)

    return answer, elapsed_time


def play(current_player, others):
    """
    어목조동 게임을 진행한다.

    current_player: str (게임을 시작한 사람 이름)
    others: list[str] (나머지 참가자 이름 목록)

    반환값:
        한 명 이상이 마시면 {이름: 잔수}
        아무도 마시지 않으면 {}
    """
    # current_player와 others를 합쳐 전체 참가자 이름 리스트를 만든다.
    # 실수로 current_player가 others에 중복 포함되어도 한 번만 남긴다.
    players = [current_player] + [
        name for name in others if name != current_player
    ]

    if len(players) < 2:
        print("어목조동 게임은 최소 2명이 필요합니다.")
        return {}  # main에서 인원수 검증이 보장되면 없어질 방어 코드

    used_words = set()
    caller = current_player
    success_count = 0
    round_number = 1
    time_limit = 7  # 테스트용

    total_word_count = sum(len(words) for words in CATEGORY_WORDS.values())

    print("\n" + "=" * 52)
    print("                    어목조동 게임")
    print("=" * 52)
    print("어: 물고기 / 목: 나무 / 조: 새 / 동: 그 밖의 동물")
    print("중복, 오답, 빈 답변, 시간 초과 시 패배합니다.")
    print("5번 성공할 때마다 제한 시간이 1초씩 줄어듭니다.")
    print(f"제한시간: {time_limit}초 / 등록 단어: {total_word_count}개")
    print("=" * 52)
    time.sleep(0.7)

    while True:
        print("\n" + "─" * 52)
        show_log(f"[ROUND {round_number}] 현재 지목자: {caller}", 0.4)

        target = choose_target(caller, players)
        show_log(f"[지목 결과] {caller} → {target}")

        category = choose_category(caller)
        show_log(
            f"[카테고리] {category} - {CATEGORY_NAMES[category]}"
        )

        show_log(
            f"[문제] {target}님, "
            f"{CATEGORY_NAMES[category]} 단어를 말하세요!"
        )
        show_log(f"[제한시간] {time_limit}초", 0.35)

        if is_user(target):
            start_time = time.perf_counter()
            answer = input(f"[답변 입력] {target}: ")
            elapsed_time = time.perf_counter() - start_time
        else:
            show_log(f"[생각 중] {target}이(가) 답을 생각합니다...")
            answer, elapsed_time = get_computer_answer(
                category,
                used_words,
                time_limit,
            )

            time.sleep(min(elapsed_time, 0.6))

            if answer:
                show_log(f"[답변] {target}: {answer}")
            else:
                show_log(f"[답변 실패] {target}: 생각이 안 나! 으악!!!")

        show_log("[판정 중] 답변을 확인합니다...", 0.45)

        is_correct, reason, normalized_answer = judge_answer(
            answer,
            category,
            used_words,
            elapsed_time,
            time_limit,
        )

        if not is_correct:
            loser = target
            show_log(f"[판정] 실패 - {reason}")
            break

        used_words.add(normalized_answer)
        success_count += 1

        show_log(
            f"[판정] 정답! "
            f"응답 시간 {elapsed_time:.1f}초"
        )
        show_log(
            f"[진행 상황] 성공 {success_count}회 / "
            f"사용 단어 {len(used_words)}개",
            0.35,
        )

        caller = target
        round_number += 1

        show_log(
            f"[턴 이동] 다음 지목자는 {caller}입니다.",
            0.45,
        )

        if success_count % 5 == 0 and time_limit > 3:
            time_limit -= 1
            show_log(
                f"[난이도 상승] 제한시간이 "
                f"{time_limit}초로 줄었습니다.",
                0.8,
            )

    drink_count = 2 if reason == "시간 초과" else 1
    result = {loser: drink_count}

    print("\n" + "=" * 52)
    show_log("[게임 종료]", 0.3)
    show_log(f"[패배자] {loser}", 0.3)
    show_log(f"[실패 이유] {reason}", 0.3)
    show_log(f"[벌칙] {loser} {drink_count}잔", 0.3)
    print("=" * 52)

    return result

