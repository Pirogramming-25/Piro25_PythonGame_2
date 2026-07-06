# Piro25_PythonGame_2/main.py
from games import game_1, game_2, game_3, game_4, game_5
from players import Player, find_player
import random

game_list = {
    1: ('홍삼게임', game_1),
    2: ('홍삼게임', game_2),
    3: ('홍삼게임', game_3),
    4: ('홍삼게임', game_4),
    5: ('홍삼게임', game_5),
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
    pass
    
    
# 게임 리스트 출력하기
def print_game_list():
    pass
    
    
# 게임 번호 선택 받고, 리턴 받은 결과 players에 반영
def play_one_round(current_player, players):
    pass
    

# main 함수            
def main():
    pass


if __name__ == "__main__":
    main()