from taupy.basic.positions import Position

def genp(*, n=10, sentencepool="p:20", d=2, initial_position=None):
    
    if initial_position is None:
        positions = [Position()]
    else:
        positions = [initial_position]

    for i in range(n):
        positions.append()