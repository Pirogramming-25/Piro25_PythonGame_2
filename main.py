# Piro25_PythonGame_2/main.py
from games import game_1, game_2, game_3, game_4, game_5
from players import Player, find_player
import random

game_list = {
    1: ('홍삼게임', game_1),
    2: ('딸기당근수박참외메론게임', game_2),
    3: ('어목조동게임', game_3),
    4: ('숫자게임', game_4),
    5: ('지하철게임', game_5),
}

name_list = ['보민', '현민', '주헌', '지연', '희원']


# 사용자 이름 받기
def get_player_name():
    while True:
        name = input("오늘 거하게 취해볼 당신의 이름은 ? : ")
        if name.strip() != "": # 아무것도 입력하지 않았을 때 다시 물어보기
            return name
        print("이름을 입력해주세요 : ")
        
        
# 주량 선택하기
def get_player_capacity():
    options = {
        1: 2,
        2: 4,
        3: 6,
        4: 8,
        5: 10, 
    }
    
    print('소주 기준 당신의 주량은 ?')
    print('1. 소주 반 병 (2잔)')
    print('2. 소주 반 병에서 한 병 (4잔)')
    print('3. 소주 한 병에서 한 병 반 (6잔)')
    print('4. 소주 한 병 반에서 두 병 (8잔)')
    print('5. 소주 두 병 이상 (10잔)')
    
    while True:
        choice = input('당신의 치사량(주량)은 얼마만큼인가요 ? (1~5를 선택해주세요) : ')
        
        if choice.isdigit() and int(choice) in options: # choice가 숫자인지, 1~5 범위인지 체크
            return options[int(choice)]
        else:
            print('1~5 사이의 숫자를 입력해주세요 : ')
        

# 대결할 사람 초대하기 (최대 3명)
def invite():
    friends = []
    
    while True:
        count = input('함께 취할 친구들은 얼마나 필요하신가요 ? (최대 3명까지 초대할 수 있어요 !) : ')
        
        if count.isdigit() and 1 <= int(count) <= 3: # count가 숫자인지, 1~3 범위인지 체크
            count = int(count)
            break
        else:
            print('1~3 사이의 숫자를 입력해주세요 : ')
    
    friend_names = random.sample(name_list, count)
    
    for friend_name in friend_names:
        capacity = random.choice([2, 4, 6, 8, 10])
        friend = Player(friend_name, capacity)
        print(f'오늘 함께 취할 친구는 {friend_name}입니다! (치사량 : {capacity})')
        friends.append(friend)
    
    return friends


# 현재 상황 출력하기
def print_status(players):
    print("\n" + "~" * 40)
    print(" 현재 플레이어들의 음주 상태 ")
    print("-" * 40)
    for p in players:
        print(f"{p.name}은(는) 지금까지 {p.drunk}잔 | 치사량까지 {p.remaining()}잔")
    print("~" * 40 + "\n")
    
    
# 게임 리스트 출력하기
def print_game_list():
    print("~" * 20)
    print("오늘의 Alcohol GAME")
    print("~" * 20)
    for num, game_info in game_list.items():
        print(f"{num}. {game_info[0]}")
    print("~" * 40)
    
    
# 게임 번호 선택 받고, 리턴 받은 결과 players에 반영
def play_one_round(current_player, players):
    is_human = (current_player == players[0]) 
    
    # 게임 선택 목록 출력
    print_game_list()
    
    choice = None
    if is_human:
        # 내 차례일 때: 직접 입력 받기
        print(f"이번 라운드는 {current_player.name}의 턴입니다! 게임을 선택해 주세요.")
        while True:
            user_input = input("원하는 게임의 번호를 선택하세요 (1~5): ")
            if user_input.strip().lower() == 'exit':
                print("\n게임을 종료합니다.")
                exit()
                
            if user_input.isdigit() and int(user_input) in game_list:
                choice = int(user_input)
                break
            print("올바른 게임 번호를 선택해 주세요.")
    else:
        # 컴퓨터 차례일 때: 랜덤
        print(f"술게임 진행중! 다른 사람의 턴입니다. 그만하고 싶으면 \"exit\"를, 계속하고 싶으면 아무키나 입력해 주세요! : ")
        user_action = input() 
        if user_action.strip().lower() == 'exit':
            print("\n 게임을 종료합니다.")
            exit()
            
        # 컴퓨터가 1~5 중 하나를 랜덤으로 선택
        choice = random.choice(list(game_list.keys()))
        print("~" * 65)
        print(f"{current_player.name}(이)가 좋아하는 랜덤 게임~ 랜덤 게임~ 무슨 게임? : {choice}")
        print("~" * 65)

    # 선택된 게임
    game_name, game_module = game_list[choice]
    print(f"\n{current_player.name} 님이 게임을 선택하셨습니다! \n")
    others = [p for p in players if p != current_player]
    game_result = game_module.play(current_player, others) 
    
    # 결과 반영 및 정산
    if not game_result:
        print("\n아무도 걸리지 않았습니다. 다음 라운드로 이동합니다.")
        return
        
    print("\n 벌칙자 발생")
    for key, drink_count in game_result.items():
        if isinstance(key, str):
            search_name = key.strip()
        else:
            search_name = key.name.strip()

        loser = find_player(players, search_name)
        if loser:
            loser.add_drink(drink_count)  
            print(f"{loser.name}님이 {drink_count}잔을 마십니다! (현재 총 {loser.drunk}잔 마심)")

# main 함수            
def main():
    print("안주 먹을 시간이 없어요 마시면서 배우는 술게임\n")
    
    # 1. 내 정보 입력 받기
    my_name = get_player_name()
    my_capacity = get_player_capacity()
    me = Player(my_name, my_capacity)
    
    # 2. 친구들 초대하기
    players = [me] + invite()
    
    # 게임 루프 시작
    round_count = 1
    while True:
        print(f"\n[ROUND {round_count}] 게임을 시작합니다.")
        print_status(players)
        
        current_player = players[(round_count - 1) % len(players)]
        

        play_one_round(current_player, players)
        
        # 3. 치사량 도달 체크 
        game_over = False
        for p in players:
            if p.is_dead():
                print(f"\n{p.name}이(가) 전사했습니다... 꿈나라에서는 편히 쉬시길..ZZZ")
                game_over = True
                
        if game_over:
            print("\n")
            print("~" * 65)
            print("\n다음에 술마시면 또 불러주세요~ 안녕!\n")
            print("~" * 65)
            break
            
        round_count += 1


if __name__ == "__main__":
    main()