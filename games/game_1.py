import random
import pyfiglet
import time

LINE = '-' * 80

def slow_print(text, delay = 0.7):
    print(text)
    time.sleep(delay)

def double_pick(picker, pool):
    candidates = []
    for p in pool:
        if p != picker:
            candidates.append(p)
    picked = random.sample(candidates, 2)
    
    slow_print(f'\n{picker}(이)가 외친다 ! 아싸 너너 ! \n-> {picked[0]}, {picked[1]} 지목 !')
    print()
    return picked


def play(current_player, others):
    pool = [current_player] + others
    
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
            if target == current_player:
                slow_print('>>> 당신이 지목당했습니다 ! 다음 사람을 지목하세요 ! <<<')
                new_target = input('입력 : ')
                print()

                if new_target in pool and new_target != current_player:
                    slow_print(f'{target}이 외친다 ! >>> 아싸 너 ! <<< -> {new_target}')
                    print()
                    count[new_target] = count.get(new_target, 0) + 1
                else:
                    slow_print(f'{target}(이)는 반응하지 못했습니다 . . . 벌칙 !')
                    return {current_player : 1}

            else:
                options = [] # 지목 당한 사람을 제외한 사람들
                for p in pool:
                    if p != target:
                        options.append(p)
                new_target = random.choice(options)
                
                # 25%의 확률로 다른 사람을 선택하지 못함
                if random.random() < 0.25:
                    print()
                    slow_print(f'{target}(이)는 반응하지 못했습니다 . . . 벌칙 !')
                    return {target: 1}
                else:
                    slow_print(f'{target}(이)가 외친다 ! >>> 아싸 너 ! <<< -> {new_target}')
                    print()
                    count[new_target] = count.get(new_target, 0) + 1
            
        double_target = None
        
        for name, cnt in count.items():
            if cnt >= 2:
                double_target = name
        
        if double_target == None:
            pending = list(count.keys()) # 이번에 지목 당한 사람들을 다음 라운드에 반응할 사람들로 이어지게
        else:
            slow_print(f'{double_target}(이)가 동시에 지목당했다 !')
            
            if double_target == current_player:
                slow_print('>>> 당신이 지목당했습니다 ! 3초 안에 >>> 아싸 홍삼 ! <<< 을 외치세요 ! <<<')
                answer = input('입력 : ')
                
                if answer == '아싸 홍삼 !':
                    slow_print('다같이 외친다! >>> 에브리바디 홍삼 ! <<<')
                    pending =  double_pick(double_target, pool)
                else:
                    slow_print(f'{current_player}(이)는 반응하지 못했습니다 . . . 벌칙 !')
                    return {current_player: 1}
                
            else:
                if random.random() < 0.40:
                    slow_print(f'{double_target}(이)는 반응하지 못햇습니다 . . . 벌칙 !')
                    return {double_target: 1}
                else:
                    slow_print(f'{double_target}(이)가 외친다 ! >>> 아싸 홍삼 ! <<<')
                    slow_print('다같이 외친다! >>> 에브리바디 홍삼 ! <<<')
                    pending = double_pick(double_target, pool)
    
    print(LINE)
    print('체인이 너무 길어져서 무승부로 처리합니다')
    print(LINE)
    return {}
                
                
if __name__== "__main__":
    play('보민', ['현민', '지연', '주헌', '희원'])
    