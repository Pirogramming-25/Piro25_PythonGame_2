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

    pending = targets

    for round in range(20):
        count = {}
        for target in pending:
            if target == current_player:
                print('당신이 지목당했습니다 ! 다음 사람을 지목하세요 !')
                new_target = input('이름을 입력해주세요')

                if new_target in pool and new_target != current_player:
                    print(f'{target}이 외친다 ! 아싸 너 ! {new_target}')
                    count[new_target] = count.get(new_target, 0) + 1
                else:
                    print(f'{target}(이)는 반응하지 못했습니다 . . . 벌칙 !')
                    return {current_player : 1}

            else:
                options = []
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
                
        

    

            
    

if __name__== "__main__":
    play('보민', ['현민', '지연', '주헌', '희원'])
