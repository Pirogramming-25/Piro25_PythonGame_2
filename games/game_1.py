import random

def play(current_player, others):
    pool = [current_player] + others
    print(pool)

    print('=== 홍삼게임 시작 ! ===')
    print('누군가 외친다: "아싸 홍삼 !"')
    print('다같이 외친다: "에브리바디 홍삼 !"')

    starter = current_player
    candidates = []
    for p in pool:
        if p != current_player:
            candidates.append(p)
    targets = random.sample(candidates, 2)
    print(f'{current_player}(이)가 외친다 ! 아싸 너너 ! {targets[0]}, {targets[1]}')

    pending = targets # pending은 다음 라운드에 반응할 사람

    for round in range(20):
        count = {} # 지목 개수를 저장할 딕셔너리
        for target in pending:
            if target == current_player:
                print('당신이 지목당했습니다 ! 다음 사람을 지목하세요 !')
                new_target = input('입력 : ')

                if new_target in pool and new_target != current_player:
                    print(f'{target}이 외친다 ! 아싸 너 ! {new_target}')
                    count[new_target] = count.get(new_target, 0) + 1
                else:
                    print(f'{target}(이)는 반응하지 못했습니다 . . . 벌칙 !')
                    return {current_player : 1}

            else:
                options = [] # 지목 당한 사람을 제외한 사람들
                for p in pool:
                    if p != target:
                        options.append(p)
                new_target = random.choice(options)
                
                # 25%의 확률로 다른 사람을 선택하지 못함
                if random.random() < 0.25:
                    return {target: 1}
                else:
                    print(f'{target}(이)가 외친다 ! 아싸 너 ! {new_target}')
                    count[new_target] = count.get(new_target, 0) + 1
            
        double_target = None
        
        for name, cnt in count.items():
            if cnt >= 2:
                double_target = name
        
        if double_target == None:
            pending = list(count.keys()) # 이번에 지목 당한 사람들을 다음 라운드에 반응할 사람들로 이어지게
        else:
            if double_target == current_player:
                print('당신이 지목당했습니다 ! 3초 안에 "아싸 홍삼 !"을 외치세요 !')
                answer = input('입력 : ')
                
                if answer == '아싸 홍삼 !':
                    print('에브리바디 홍삼 !')
                    return {}
                else:
                    print(f'{current_player}(이)는 반응하지 못했습니다 . . . 벌칙 !')
                    return {current_player: 1}
                
            else:
                if random.random() < 0.40:
                    print(f'{double_target}(이)는 반응하지 못햇습니다 . . . 벌칙 !')
                    return {double_target: 1}
                else:
                    print(f'{double_target}(이)가 외친다 ! 아싸 홍삼 !')
                    print('에브리바디 홍삼 !')
                    return {}
                
                

                    
                
                
        

    

            
    

if __name__== "__main__":
    play('보민', ['현민', '지연', '주헌', '희원'])
    