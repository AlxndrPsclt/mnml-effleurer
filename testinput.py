from libinput import LibInput, ContextType, EventType
li = LibInput(context_type=ContextType.PATH)

device = li.add_device('/dev/input/event1')

for event in li.events:
    if event.type.is_touch():
        e={'type':event.type}
        if event.type==EventType.TOUCH_DOWN:
            e['coords']=event.coords
            e['slot']=event.slot
        if event.type==EventType.TOUCH_MOTION:
            e['coords']=event.coords
            e['slot']=event.slot
        #if event.type==EventType.TOUCH_FRAME:
        print(e)


