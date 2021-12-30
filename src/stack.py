
class Stack():
    def __init__(self):
        self.stack = []

    def length(self):
        return len(self.stack)
    
    def top(self):
        if len(self.stack):
            return self.stack[0]
        else:
            return None
    
    def top_color(self):
        if self.top(self):
            return self.stack[0].color