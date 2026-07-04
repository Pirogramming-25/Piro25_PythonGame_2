# 1. 1~99까지 숫자를 입력함
# 2. 십의 자리 숫자가 겹치면 더 작은 숫자의 플레이어가 마심
# 3. 모든 플레이어의 십의자리 숫자가 다 다르고 일의 자리 숫자가 겹치면 더 큰 숫자의 플레이어가 마심
# 4. 2,3번 규칙에 의해 걸린 사람의 수가 11,22,33,44,55,66,77,88이면 해당 수가 들어간 모두가 1잔 추가 
# 5. 2,3번 규칙에 의해 걸린 사람의 수에 0,9가 들어가면 해당 플레이어만 1잔 추가
# 6. 모든 플레이어의 수가 겹치지 않는다면 모두가 마시지 않고 종료

def play (current_player, others):

    all_players = [current_player] + others
    ten_num = {}
    one_num = {}
    players_num = {}
    drink_count = {}
    original_losers = []

    # 플레이어별로 1~99 사이의 숫자를 입력받음
    for player in all_players:
        while True:
            try:
                num = int(input(f"[{player}] 1부터 99 사이의 숫자를 입력하세요: "))
                if 1 <= num <= 99:
                    players_num[player] = num
                    break
                else:
                    print("1에서 99 사이의 숫자만 입력 가능합니다.")
            except ValueError:
                print("올바른 숫자를 입력해주세요.")

    # 10의 자리와 1의 자리를 분리하여 딕셔너리에 저장       
    for player in all_players:
        num = players_num[player]
        ten_num[player] = num // 10
        one_num[player] = num % 10


    tens_list = list(ten_num.values())
    ones_list = list(one_num.values())
    duplicated_tens = []
    duplicated_ones = []

    # 겹치는 숫자 리스트에 담기
    for t in tens_list:
        if tens_list.count(t) > 1 and t not in duplicated_tens:
            duplicated_tens.append(t)

    for o in ones_list:
        if ones_list.count(o) > 1 and o not in duplicated_ones:
            duplicated_ones.append(o)

    # 플레이어별 벌칙 잔수를 기록할 딕셔너리를 초기화
    for player in all_players:
        drink_count[player] = 0

    # 십의 자리 숫자가 겹치는 경우
    if len(duplicated_tens) > 0:
        for t_val in duplicated_tens:
            print(f"[십의 자리 검사] 십의 자리 '{t_val}'이(가) 겹쳤습니다!")
            min_num = 100
            loser = ""
            for player in all_players:
                if ten_num[player] == t_val:
                    if players_num[player] < min_num:
                        min_num = players_num[player]
                        loser = player
            if loser:
                print(f"십의 자리가 겹쳐서 가장 작은 숫자를 낸 [{loser}]({players_num[loser]}) 님이 패배자로 선정되었습니다. (1잔 추가)")
                drink_count[loser] += 1 

    # 십의 자리는 다 다르고, 일의 자리 숫자가 겹치는 경우
    else:
        print("십의 자리가 겹치는 플레이어가 없어 일의 자리를 검사합니다.")
        
        if len(duplicated_ones) > 0:
            for o_val in duplicated_ones:
                print(f"[일의 자리 검사] 일의 자리 '{o_val}'이(가) 겹쳤습니다!")
                
                max_num = -1
                loser = ""
                for player in all_players:
                    if one_num[player] == o_val:
                        if players_num[player] > max_num:
                            max_num = players_num[player]
                            loser = player
                if loser:
                    print(f"일의 자리가 겹쳐서 가장 큰 숫자를 낸 {loser}님이 패배자로 선정되었습니다. (1잔 추가)")
                    drink_count[loser] += 1  
        else:
            print("일의 자리도 겹치는 플레이어가 없습니다 ㅠㅠ 게임이 종료됩니다 ㅠㅠ")


    
    # 1단계에서 한 번이라도 걸린 원본 벌칙자들을 먼저 찾음
    for player, count in drink_count.items():
        if count > 0:
            original_losers.append(player)

    # 반복되는 숫자의 경우 (11,22,33,44,55,66,77,88)
    if len(original_losers) > 0:
        for loser in original_losers:
            loser_num = players_num[loser]
            if loser_num in [11, 22, 33, 44, 55, 66, 77, 88]:
                target_digit = loser_num // 10
                print(f"{loser}님이 반복되는 수{loser_num}이므로 연대책임~!!!")

                for player in all_players:
                    if ten_num[player] == target_digit or one_num[player] == target_digit:
                        drink_count[player] += 1 
                        print(f"자릿수에 '{target_digit}'이(가) 포함된 {player}님도 1잔 적립! (1잔 추가)")

        # 0, 9가 들어간 경우
        for loser in original_losers:
            loser_num = players_num[loser]
            if '0' in str(loser_num) or '9' in str(loser_num):
                drink_count[loser] += 1
                print(f"패배자 {loser}님의 숫자 {loser_num}에 0 또는 9가 포함되어 1잔 더 적립됩니다! (1잔 추가)")

        # ---- 디버깅용 화면 출력 파트 ----
        single_drinkers = []
        double_drinkers = []
        triple_or_more = {} 

        for player, count in drink_count.items():
            if count == 1:
                single_drinkers.append(player)
            elif count == 2:
                double_drinkers.append(player)
            elif count >= 3:
                triple_or_more[player] = count

        print("\n============= 게임 결과 =============")
        if triple_or_more:
            for p, c in triple_or_more.items():
                print(f"💀 [벌칙 {c}잔] {p} 님은 치사량입니다! 총 {c}잔 마십니다!!!")
        if double_drinkers:
            print(f"🔥 [벌칙 2잔] {', '.join(double_drinkers)} 님은 혼자 2잔 마십니다!")
        if single_drinkers:
            print(f"🍺 [벌칙 1잔] {', '.join(single_drinkers)} 님은 시원하게 1잔 마십니다!")

        # ---- [계약 조건] 최종 딕셔너리 리턴 ----
        result_dict = {}
        for player, count in drink_count.items():
            if count > 0:
                result_dict[player] = count
                
        return result_dict

    # 규칙 6: 아무도 겹치지 않는 경우
    else:
        print("\n============= 게임 결과 =============")
        print("🎉 와우! 아무도 겹치지 않았습니다. 모두 생존 완료!")
        return {}


# 함수가 잘 작동하는지 테스트하기 위한 샘플 실행 코드입니다.
if __name__ == "__main__":
    me = "정우"
    friends = ["철수", "영희", "민수"]
    
    # 디버깅용 리턴값 확인을 원하시면 print(play(me, friends)) 로 감싸서 확인하셔도 됩니다.
    play(me, friends)