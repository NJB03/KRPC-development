import krpc
import math
from math import sin, cos, pi
import time



conn = krpc.connect(name='Hello World')
vessel = conn.space_center.active_vessel
srf_frame = vessel.orbit.body.reference_frame


def cross_product(u, v):
    return (u[1]*v[2] - u[2]*v[1],
            u[2]*v[0] - u[0]*v[2],
            u[0]*v[1] - u[1]*v[0])


def dot_product(u, v):
    return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]


def magnitude(v):
    return math.sqrt(dot_product(v, v))


def angle_between_vectors(u, v):
    """ Compute the angle between vector u and v """
    dp = dot_product(u, v)
    if dp == 0:
        return 0
    um = magnitude(u)
    vm = magnitude(v)
    return math.acos(dp / (um*vm)) * (180. / math.pi)

def ascent():
    oldalt = 0
    if alti() <= 10300:
        
        if alti() < 5000:
            if srf_speed() < 60:
                vessel.control.throttle += 0.01
            if srf_speed() > 70:
                vessel.control.throttle -= 0.01
            if srf_speed() > 65 and srf_speed() < 70:
                vessel.control.throttle = 0.5
        if alti() > 5100 and alti() < 5150:
            vessel.control.toggle_action_group(1)
        if alti() > 5200 and alti() < 9000:
            if srf_speed() < 75:
                vessel.control.throttle += 0.08
            if srf_speed() > 80:
                vessel.control.throttle -= 0.01            
        if alti() > 9050 and alti() < 9150:
            vessel.control.toggle_action_group(2)
        if alti() > 9300:
            if srf_speed() < 8:
                vessel.control.throttle += 0.001
            if srf_speed() > 12:       
                vessel.control.throttle -= 0.001
            if alti() < oldalt:
                vessel.control.throttle = 0
                print("ascent omplete")
                vessel.control.toggle_action_group(6)
                ascent_complete = True
        oldalt = alti()
                
def descent():
    '''
    vessel.auto_pilot.auto_tune = True
    vessel.auto_pilot.attenuation_angle = (1, 1, 1)
    vessel.auto_pilot.time_to_peak = (0.1, 0.1, 0.1)
    vessel.auto_pilot.stopping_time = (100, 1, 100)
    vessel.auto_pilot.deceleration_time = (1, 1, 1)     
    vessel.auto_pilot.target_pitch_and_heading(0, 270)
    vessel.control.toggle_action_group(5)
    '''
    while alti() >= 1500:
        vessel.auto_pilot.target_pitch_and_heading(0, 270)
    while alti() <= 1490 and alti() >= 1487:
        vessel.control.toggle_action_group(5)
    while alti() < 1490:
        a = (vessel.mass/vessel.max_thrust) - 9.8
        vi = srf_speed
        stoptime = (vi-vf)/a
        timehit =  alti()/vi 
        vessel.control.sas = True
        vessel.auto_pilot.sas_mode = vessel.auto_pilot.sas_mode.retrograde
        vessel.control.throttle = 1
        if stoptime*-1 > timehit:
            vessel.control.throttle = 0.85
        if stoptime*-1 < timehit:
            vessel.control.throttle = 0.3
        if alti() <= 300:
            vessel.control.gear = True
        if srf_speed < 10:
            vessel.control.throttle = 0        
        

ap = vessel.auto_pilot

ap.reference_frame = vessel.surface_reference_frame
ap.engage()

ascent_complete = False
ut = conn.add_stream(getattr, conn.space_center, 'ut')
maltitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
srf_speed = conn.add_stream(getattr, vessel.flight(srf_frame), 'speed')
dynamic_pressure = conn.add_stream(getattr, vessel.flight(srf_frame), 'dynamic_pressure')
stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
obt_frame = vessel.orbit.body.non_rotating_reference_frame
srf_frame = vessel.orbit.body.reference_frame
orb_speed = conn.add_stream(getattr, vessel.flight(obt_frame), 'speed')
altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')
elevation = conn.add_stream(getattr, vessel.flight(), 'elevation')
alti = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')



vessel.control.activate_next_stage()
#vessel.control.sas = True
vessel.control.rcs = False
vessel.control.throttle = 0.5

angle = 0
time.sleep(2)
vessel.auto_pilot.target_pitch_and_heading(90, 270)
vessel.control.throttle = 0.75
while True:
    while ascent_complete == False:
        ascent()
    vessel.control.rcs = True  
    while ascent_complete == True:
        descent()
    
    

vessel.control.rcs = True

'''
import krpc
import math
from math import sin, cos, pi
import time


conn = krpc.connect(name='Hello World')
vessel = conn.space_center.active_vessel
srf_frame = vessel.orbit.body.reference_frame

ap = vessel.auto_pilot

ap.reference_frame = vessel.surface_reference_frame
ap.engage()

ascent_complete = False
ut = conn.add_stream(getattr, conn.space_center, 'ut')
maltitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
srf_speed = conn.add_stream(getattr, vessel.flight(srf_frame), 'speed')
dynamic_pressure = conn.add_stream(getattr, vessel.flight(srf_frame), 'dynamic_pressure')
stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
obt_frame = vessel.orbit.body.non_rotating_reference_frame
srf_frame = vessel.orbit.body.reference_frame
orb_speed = conn.add_stream(getattr, vessel.flight(obt_frame), 'speed')
altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')
elevation = conn.add_stream(getattr, vessel.flight(), 'elevation')
alti = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')


#essel.auto_pilot.auto_tune = True
vessel.auto_pilot.roll_threshold =  2
vessel.auto_pilot.stopping_time = (100, 1, 100)
#vessel.auto_pilot.deceleration_time = (0.5, 0.5, 1)     
vessel.auto_pilot.target_pitch_and_heading(0, 270)
vessel.auto_pilot.stopping_time

vessel.control.toggle_action_group(6)
vessel.control.rcs = True
toggleflaps = True
time.sleep(3)
vessel.control.toggle_action_group(5)
vessel.control.rcs = True
vf = 0
engoff = False
while True:
    while alti() >= 8000:
        vessel.auto_pilot.target_pitch_and_heading(-3, 270)
        
    while alti() > 0 and alti() < 1000:
        vessel.auto_pilot.target_pitch_and_heading(90, 270)
        if toggleflaps == True:
            #vessel.control.sas = True
            vessel.control.toggle_action_group(3)            
            vessel.control.toggle_action_group(5)
            toggleflaps = False
        a = (vessel.mass/vessel.max_thrust) - 9.8
        vi = srf_speed()
        stoptime = (vi-vf)/a
        timehit =  alti()/vi 
        vessel.auto_pilot.target_pitch_and_heading(90, 270)
        if stoptime*-1 > timehit:
            vessel.control.throttle = 0.85
        if stoptime*-1 < timehit:
            vessel.control.throttle = 0.3
        if alti() <= 100:
             
            if engoff == False:
                vessel.control.toggle_action_group(1)
                engoff = True
            vessel.control.gear = True
            if srf_speed() < 10:
                vessel.control.throttle = 0
                break
                
                
    '''