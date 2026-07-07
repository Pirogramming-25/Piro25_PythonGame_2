import random
import pyfiglet
import time
import threading

LINE = '-' * 80


# 3초 안에 입력이 없을 때 벌칙
def timed_input(prompt, timeout = 3):
    print(prompt, end = '', flush = True)
    answer = [None]

    def get_input():
        answer[0] = input()

    thread = threading.Thread(target = get_input)
    thread.daemon = True
    thread.start()
    thread.join(timeout = timeout)

    return answer[0]


# 0.7초마다 출력
def slow_print(text, delay = 0.7):
    print(text)
    time.sleep(delay)


# 두 명에게 지목 당했을 때
def double_pick(picker, pool):
    candidates = []
    for p in pool:
        if p != picker:
            candidates.append(p)
    picked = random.sample(candidates, 2)
    
    slow_print(f'\n{picker}(이)가 외친다 ! 아싸 너너 ! \n-> {picked[0]}, {picked[1]} 지목 !')
    print()
    return picked


# 인원이 2명일 경우
def play_two(current_player, other, user_name):
    pool = [current_player, other]
    
    print()
    result = pyfiglet.figlet_format('HONGSAM GAME')
    print(result)
    
    print(LINE)
    print()
    slow_print(f'참가자는 >>> {", ".join(pool)} <<< 입니다 !')
    print()
    print(LINE)
    
    slow_print(f'\n{current_player}(이)가 외친다 ! >>> 아싸 홍삼 ! <<<')
    slow_print(f'{other}(이)가 외친다 ! >>> 에브리바디 홍삼 ! <<<')

    target = other

    for round in range(20):
        if target == current_player: # target이 게임을 진행하는 주체인지, 아닌지
            opponent = other
        else:
            opponent = current_player
            
        if target == user_name:
            slow_print('>>> 당신이 지목당했습니다 ! 3초 안에 상대를 지목하세요 ! <<<')
            new_target = timed_input('-> ')
            print()
            
            if new_target == opponent:
                success = True
            else:
                success = False
                
        else:
            if random.random() < 0.25:
                success = True
            else:
                success = False
                
                
        if success:
            slow_print(f'{target}(이)가 외친다 ! >>> 아싸 너 ! <<< -> {opponent}')
            target = opponent
        else:
            slow_print(f'{target}(이)는 반응하지 못했습니다 . . . 벌칙 !')
            return {target: 1}

    print(LINE)
    print('체인이 너무 길어져서 무승부로 처리합니다')
    print(LINE)
    return {}
    

def play(current_player, others, user_name = None): # user_name은 실제 사람이 조작 중인 플레이어
    if not isinstance(current_player, str): # Player 객체로 들어올 경우를 대비하여 이름만 추출
        current_player = current_player.name
    others = [o if isinstance(o, str) else o.name for o in others]
    if user_name is not None and not isinstance(user_name, str):
        user_name = user_name.name
 
    if user_name is None:
        user_name = current_player
        
            
    pool = [current_player] + others
    
    if len(pool) < 2:
        print("홍삼게임은 상대가 최소 1명 이상 있어야 진행할 수 있습니다")
        return {}
    
    if len(pool) == 2:
        return play_two(current_player, others[0], user_name)
    
    print()
    result = pyfiglet.figlet_format('HONGSAM GAME')
    print(result)
    
    print(LINE)
    print()
    slow_print(f'참가자는 >>> {", ".join(pool)} <<< 입니다 !')
    print()
    print(LINE)
    
    print()
    slow_print(f'{current_player}(이)가 외친다 ! >>> 아싸 홍삼 ! <<<')
    slow_print('다같이 외친다 ! >>> 에브리바디 홍삼 ! <<<')    
    
    
    pending = double_pick(current_player, pool) # pending은 다음 라운드에 반응할 사람

    for round in range(20):
        count = {} # 지목 개수를 저장할 딕셔너리
        
        for target in pending:
            if target == user_name: # target이 진짜 사용자인지
                slow_print('>>> 당신이 지목당했습니다 ! 3초 안에 다음 사람을 지목하세요 ! <<<')
                new_target = timed_input('-> ')
                print()

                if new_target in pool and new_target != target:
                    valid = True
                else:
                    valid = False

            else:
                options = [] # 지목 당한 사람을 제외한 사람들
                for p in pool:
                    if p != target:
                        options.append(p)
                new_target = random.choice(options)
                
                # 10%의 확률로 다른 사람을 선택하지 못함
                if random.random() < 0.1:
                    valid = False
                else:
                    valid = True
            
            if valid:
                slow_print(f'{target}이 외친다 ! >>> 아싸 너 ! <<< -> {new_target}')
                print()
                count[new_target] = count.get(new_target, 0) + 1
            else:
                slow_print(f'{target}(이)는 반응하지 못했습니다 . . . 벌칙 !')
                return {target: 1}
            
                                
        double_target = None
        
        for name, cnt in count.items():
            if cnt >= 2:
                double_target = name
        
        if double_target == None:
            pending = list(count.keys()) # 이번에 지목 당한 사람들을 다음 라운드에 반응할 사람들로 이어지게
        else:
            slow_print(f'{double_target}(이)가 동시에 지목당했다 !')
            
            if double_target == user_name: 
                slow_print('>>> 당신이 지목당했습니다 ! 3초 안에 >>> 아싸 홍삼 ! <<< 을 외치세요 ! <<<')
                answer = timed_input('-> ')
                
                if answer == '아싸 홍삼 !':
                    success = True
                else:
                    success = False
                
            else:
                if random.random() < 0.40:
                    success = False
                else:
                    success = True
                    
            if success:
                slow_print(f'{double_target}(이)가 외친다 ! >>> 아싸 홍삼 ! <<<')
                slow_print('다같이 외친다! >>> 에브리바디 홍삼 ! <<<')
                pending = double_pick(double_target, pool)
            else:
                slow_print(f'{double_target}(이)는 반응하지 못했습니다 . . . 벌칙 !')
                return {double_target: 1}  # current_player -> double_target

    
    print(LINE)
    print('체인이 너무 길어져서 무승부로 처리합니다')
    print(LINE)
    return {}
                               
if __name__== "__main__":
    play('보민', ['현민', '지연', '주헌', '희원'], user_name = '피로')
    