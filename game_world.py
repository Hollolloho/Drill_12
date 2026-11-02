#게임월드 리스트 초기화

world = [[], []] # 객체들의 리스트, 빈 리스트

# 객체를 게임월드에 추가하는 함수
def add_object(o, depth=0):
    world[depth].append(o) # 지정한 레이어에 객체를 추가

append = add_object


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return
    raise ValueError('Object not found in game world')


def clear():
    for layer in world:
        layer.clear()

#게임 로직

def update():
    for layer in world:
        for o in layer[:]:
            o.update() # 객체들의 update() 호출

#게임 월드 렌더링

def render():
    for layer in world:
        for o in layer:
            o.draw() # 객체들의 draw() 호출

#객체를 게임월드에 추가

def add_objects(objects, depth=0):
    world[depth].extend(objects)

def remove_objects(objects, depth):
    for o in list(objects):
        world[depth].remove(o)

