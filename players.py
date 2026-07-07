class Player:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity # 치사량
        self.drunk = 0 # 지금까지 마신 잔
    def __str__(self):
        return self.name
        
    def add_drink(self, count): # 잔 수 추가하기
        self.drunk += count
        
    def is_dead(self): # 치사량 도달했는지
        return self.drunk >= self.capacity
    
    def remaining(self): # 치사량까지 얼마나 남았는지
        return max(0, self.capacity - self.drunk)
    
    
def find_player(players, name):
    for player in players:
        if player.name == name:
            return player
    return None