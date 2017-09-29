on_ground = True
class Node()
    def __init__(self, tx,ty,tvx,tvy,tm,tf):
        x=tx
        y=ty   
        vx=tvx
        vy=tvy
        m = tm
        f = tf
    def applyForce(i):
        ni = i
        ni.vx *= .95
        ni.vy *= .95
        ni.y += ni.vy
        ni.x += ni.vx
    def applyGravity(i):
        ni = i
        ni.vy += .005
    def collide(index)
        ni = index
        dif = ni.y + ni.m/2
        if (dif >= 0 and on_ground):
            ni.y = -ni.m/2
            ni.vy = 0
            ni.x -= ni.vx*ni.f
            if(ni.vx > 0):
                ni.vx -= ni.f*dif*4.0
                if(ni.vx < 0):
                    ni.vx = 0
            else:
                ni.vx += ni.f*dif*4.0
                if(ni.vx > 0):
                    ni.vx = 0
        
class Muscle()
    def __init__(self, tperiod, tc1, tc2, tcontract_time, textend_time, tcontract_length, textend_length, tcontracted, trigidity):
        period = tperiod
        c1 = tc1
        c2 = tc2
        contract_time = tcontract_time
        contract_length = tcontract_length
        extend_time = textend_time
        extend_length = textend_length
        contracted = tcontracted
        rigidity = trigidity
    
    def applyForce(i, target):
        
