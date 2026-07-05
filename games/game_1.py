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

    pending = []
    count = {}

    for target in targets:
        if target == current_player:
            print('당신이 지목당했습니다 ! 다음 사람을 지목하세요 !')
            new_target = input('이름을 입력해주세요')

            if new_target in pool and new_target != current_player:
                print(f'{target}이 외친다 ! 아싸 너 ! {new_target}')
                count[new_target] = count.get(new_target, 0) + 1
            else:
                pass # 오타, 없는 사람, 본인 지목은 벌칙

        else:
            options = []
            for p in pool:
                if p != target:
                    options.append(p)
            new_target = random.choice(options)

            print(f'{target}(이)가 외친다 ! 아싸 너 ! {new_target}')
            count[new_target] = count.get(new_target, 0) + 1

            
    

if __name__== "__main__":
    play('보민', ['현민', '지연', '주헌', '희원'])
