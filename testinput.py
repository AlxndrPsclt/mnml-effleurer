from libinput import LibInput, ContextType, EventType
from math import pi, isclose
from cmath import phase

li = LibInput(context_type=ContextType.PATH)

device = li.add_device('/dev/input/event1')
(X,Y)=device.size
X_GRID_SIZE=3
Y_GRID_SIZE=5

DIRECTION_ANGLES=[0, pi/2, pi, -pi, -pi/2, pi/4, 3*pi/4, -3*pi/4, -pi/4]   #Starting with right, up, left, down, then up-left, up-right, down-left, down-right, to give priority to horizontal and veretical swipe over diagonal (on special cases such as pi/8)
# pi is present alog with -pi to counter problems with disconinuty on borders

gesture_description = {}
last_coords={}

def main():
    for e in li.events:
        if e.type.is_touch():

            #Some debug info
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
                last_coords[e.slot]=e.coords
                gesture_description[e.slot]["gesture"]=[]

            if e.type==EventType.TOUCH_MOTION:
                gesture_description[e.slot]["gesture"].append(get_direction(e.coords, last_coords[e.slot]))
                last_coords[e.slot]=e.coords

def get_grid_coords(coords):
    (x,y)=coords
    return (int(x/(X/X_GRID_SIZE)), int(y/(Y/Y_GRID_SIZE)))

def get_direction(coords, last_coords):
    (x,y)=coords
    (lx,ly)=last_coords
    delta_x=lx-x
    delta_y=ly-y
    motion_vec=complex(delta_x, delta_y)
    motion_angle=phase(motion_vec)

    #isclose(diag, tm[1], abs_tol=pi/4)
    #Find closesed angle in cardinal direction + up-left etc...
    direction=filter(lambda direction_angle: isclose(direction_angle, motion_angle, abs_tol=pi/8), DIRECTION_ANGLES)
    return int(next(direction)/(pi/4))

    

    # (63.470588235294116, 112.88235294117646)  device.size
    # (13.470588235294118, 15.411764705882353)  top left
    # (53.05882352941177, 18.058823529411764)   top right
    # (11.941176470588236, 108.70588235294117)  bottom left
    # (54.588235294117645, 105.70588235294117)  bottom right


if __name__ == '__main__':
    main()

    #print([e.time, e.type, e.device, e.coords, e.transform_coords, e.seat_slot, e.slot])
