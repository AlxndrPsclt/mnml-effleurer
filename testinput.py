from libinput import LibInput, ContextType, EventType
from math import pi, isclose
from cmath import phase
from json import dump
import random

#li = LibInput(context_type=ContextType.PATH, debug=True)
li = LibInput(context_type=ContextType.PATH)

device = li.add_device('/dev/input/event1')
(X,Y)=device.size
X_GRID_SIZE=3
Y_GRID_SIZE=5

DIRECTION_ANGLES=[0, pi/2, pi, -pi, -pi/2, pi/4, 3*pi/4, -3*pi/4, -pi/4]
#Starting with right, up, left, down, then up-left, up-right, down-left, down-right, to give priority to horizontal and veretical swipe over diagonal (on special cases such as pi/8)
# pi is present alog with -pi to counter problems with disconinuty on borders


gesture_description = {}
last_coords={}
saved_gesture_num=0

def main():
    for e in li.events:
        print(li.next_event_type())
        if e.type.is_touch():

            #print([e.time, e.type, e.device, e.coords, e.transform_coords, e.seat_slot, e.slot])
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

            if e.type==EventType.TOUCH_UP:
                #save_path_for_training(e.slot)
                print(str(saved_gesture_num).zfill(5) + " saved")

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

    #Find closest angle in cardinal direction + up-left etc...
    direction=filter(lambda direction_angle: isclose(direction_angle, motion_angle, abs_tol=pi/8), DIRECTION_ANGLES)
    return int(next(direction)/(pi/4))

#def save_path_for_training(slot):
#    global saved_gesture_num
#    with open('/home/alex/mnml-effleurer-training/shapeLinv/sequence'+str(saved_gesture_num).zfill(5)+'.json', 'w') as outfile:
#        dump(gesture_description[slot]['gesture'], outfile)
#        saved_gesture_num+=1
#


if __name__ == '__main__':
    main()
