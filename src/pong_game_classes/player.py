class Player:

    def __init__(self, name:str):
        self.name: str = name
        self.score: int = 0

    def get_name(self):
        return self.name
    
    def get_score(self):
        return self.score

    def increment_score(self):
        self.score += 1

    def reset(self):
        self.score = 0