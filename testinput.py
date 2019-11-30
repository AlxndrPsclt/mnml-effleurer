from libinput import LibInput, ContextType, EventType
li = LibInput(context_type=ContextType.PATH)

device = li.add_device('/dev/input/event1')


def main():
    list_events=[]
    for e in li.events:
        if e.type.is_touch():
            list_events.append(e)
            if e.type==EventType.TOUCH_FRAME:
                print([e.time, e.type.name])
            if e.type in [EventType.TOUCH_DOWN, EventType.TOUCH_MOTION]:
                print([e.time, e.type.name, e.coords, e.slot])
                #print([e.time, e.type, e.device, e.coords, e.transform_coords, e.seat_slot, e.slot])

# TODO: 

if __name__ == '__main__':
    main()

