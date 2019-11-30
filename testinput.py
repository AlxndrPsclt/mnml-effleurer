from libinput import LibInput, ContextType, EventType
li = LibInput(context_type=ContextType.PATH)

device = li.add_device('/dev/input/event1')


gesture_description = {}
list_events=[]

def main():
    for e in li.events:
        if e.type.is_touch():

            #Some debug info
            list_events.append(e)
            if e.type==EventType.TOUCH_FRAME:
                print([e.time, e.type.name])
            if e.type == EventType.TOUCH_DOWN:
                print([e.time, e.type.name, e.coords, get_grid_coords(e.coords), e.slot])
            if e.type == EventType.TOUCH_MOTION:
                print([e.time, e.type.name, e.coords, e.slot])
            if e.type==EventType.TOUCH_UP:
                print([e.time, e.type.name, e.slot])

            #Real work
            if e.type==EventType.TOUCH_DOWN:
                gesture_description[e.slot]={
                    "start_time":e.time,
                    "start_pos": e.coords,
                    "start_pos_grid": get_grid_coords(e.coords)
                } 

def get_grid_coords(coords):
    (X,Y)=device.size
    (x,y)=coords
    X_grid_size=3
    Y_grid_size=5

    return (int(x/(X/X_grid_size)), int(y/(Y/Y_grid_size)))

    # (63.470588235294116, 112.88235294117646)  device.size
    # (13.470588235294118, 15.411764705882353)  top left
    # (53.05882352941177, 18.058823529411764)   top right
    # (11.941176470588236, 108.70588235294117)  bottom left
    # (54.588235294117645, 105.70588235294117)  bottom right


if __name__ == '__main__':
    main()

    #print([e.time, e.type, e.device, e.coords, e.transform_coords, e.seat_slot, e.slot])
