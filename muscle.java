class Node{
  float x, y, vx, vy, m, f;
  Node(float tx, float ty, float tvx, float tvy, float tm, float tf){
    x = tx;
    y = ty;
    vx = tvx;
    vy = tvy;
    m = tm;
    f = tf;
  }
  void applyForces(int i){
    Node ni = n.get(i);
    ni.vx *= AIR_FRICTION;
    ni.vy *= AIR_FRICTION;
    ni.y += ni.vy;
    ni.x += ni.vx;
  }
  void applyGravity(int i){
    Node ni = n.get(i);
    ni.vy += GRAVITY;
  }
  void hitWalls(int index){
    Node ni = n.get(index);
    float dif = ni.y+ni.m/2;
    if(dif >= 0 && haveGround){
      ni.y = -ni.m/2;
      ni.vy = 0;
      ni.x -= ni.vx*ni.f;
      if(ni.vx > 0){
        ni.vx -= ni.f*dif*FRICTION;
        if(ni.vx < 0){
          ni.vx = 0;
        }
      }else{
        ni.vx += ni.f*dif*FRICTION;
        if(ni.vx > 0){
          ni.vx = 0;
        }
      }
    }
    for(int i = 0; i < rects.size(); i++){
      Rectangle r = rects.get(i);
      boolean flip = false;
      float px, py;
      int section = 0;
      if(abs(ni.x-(r.x1+r.x2)/2) <= (r.x2-r.x1+ni.m)/2 && abs(ni.y-(r.y1+r.y2)/2) <= (r.y2-r.y1+ni.m)/2){
        if(ni.x >= r.x1 && ni.x < r.x2 && ni.y >= r.y1 && ni.y < r.y2){
          float d1 = ni.x-r.x1;
          float d2 = r.x2-ni.x;
          float d3 = ni.y-r.y1;
          float d4 = r.y2-ni.y;
          if(d1 < d2 && d1 < d3 && d1 < d4){
            px = r.x1;
            py = ni.y;
            section = 3;
          }else if(d2 < d3 && d2 < d4){
            px = r.x2;
            py = ni.y;
            section = 5;
          }else if(d3 < d4){
            px = ni.x;
            py = r.y1;
            section = 1;
          }else{
            px = ni.x;
            py = r.y2;
            section = 7;
          }
          flip = true;
        }else{
          if(ni.x < r.x1){
            px = r.x1;
            section = 0;
          }else if(ni.x < r.x2){
            px = ni.x;
            section = 1;
          }else{
            px = r.x2;
            section = 2;
          }
          if(ni.y < r.y1){
            py = r.y1;
            section += 0;
          }else if(ni.y < r.y2){
            py = ni.y;
            section += 3;
          }else{
            py = r.y2;
            section += 6;
          }
        }
        float distance = dist(ni.x,ni.y,px,py);
        float rad = ni.m/2;
        float wallAngle = 0;
        if(distance <= 0.00000001){ // distance is zero, can't use atan2
          if(section <= 2){
            wallAngle = PI/4.0 + section*PI/4.0;
          }else if(section >= 6){
            wallAngle = 5*PI/4.0 + (8-section)*PI/4.0;
          }else if(section == 3){
            wallAngle = PI;
          }else if(section == 5 || section == 4){
            wallAngle = 0;
          }
          flip = false;
        }else{
          wallAngle = atan2(py-ni.y,px-ni.x);
        }
        if(flip){
          wallAngle += PI;
        }
        if(distance < rad || flip){
          dif = rad-distance;
          float multi = rad/distance;
          if(flip){
            multi = -multi;
          }
          ni.x = (ni.x-px)*multi+px;
          ni.y = (ni.y-py)*multi+py;
          float veloAngle = atan2(ni.vy,ni.vx);
          float veloMag = dist(0,0,ni.vx,ni.vy);
          float relAngle = veloAngle-wallAngle;
          float relY = sin(relAngle)*veloMag*dif*FRICTION;
          ni.vx = -sin(relAngle)*relY;
          ni.vy = cos(relAngle)*relY;
        }
      }
    }
  }
  Node copyNode(){
    return (new Node(x,y,0,0,m,f));
  }
  Node modifyNode(float mutability){
    float newX = x+r()*0.5*mutability*MUTABILITY_FACTOR;
    float newY = y+r()*0.5*mutability*MUTABILITY_FACTOR;
    float newM = m+r()*0.1*mutability*MUTABILITY_FACTOR;
    newM = min(max(newM,MINIMUM_NODE_SIZE),MAXIMUM_NODE_SIZE);
    float newF = f+r()*0.1*mutability*MUTABILITY_FACTOR;
    newF = min(max(newF,MINIMUM_NODE_FRICTION),MAXIMUM_NODE_FRICTION);
    return (new Node(newX,newY,0,0,newM,newF));//max(m+r()*0.1,0.2),min(max(f+r()*0.1,0),1)
  }
}
class Muscle{
  int period, c1, c2;
  float contractTime,contractLength, extendTime, extendLength;
  float thruPeriod;
  boolean contracted;
  float rigidity;
  Muscle(int tperiod, int tc1, int tc2, float tcontractTime,
  float textendTime, float tcontractLength, float textendLength, boolean tcontracted, float trigidity){
    period  = tperiod;
    c1 = tc1;
    c2 = tc2;
    contractTime = tcontractTime;
    extendTime = textendTime;
    contractLength = tcontractLength;
    extendLength = textendLength;
    contracted = tcontracted;
    rigidity = trigidity;
  }
  void applyForce(int i, float target){
    Node ni1 = n.get(c1);
    Node ni2 = n.get(c2);
    float distance = dist(ni1.x,ni1.y,ni2.x,ni2.y);
    float angle = atan2(ni1.y-ni2.y,ni1.x-ni2.x);
    force = min(max(1-(distance/target),-0.4),0.4);
    ni1.vx += cos(angle)*force*rigidity/ni1.m;
    ni1.vy += sin(angle)*force*rigidity/ni1.m;
    ni2.vx -= cos(angle)*force*rigidity/ni2.m;
    ni2.vy -= sin(angle)*force*rigidity/ni2.m;
  }
  Muscle copyMuscle(){
    return new Muscle(period,c1,c2,contractTime,extendTime,
    contractLength,extendLength,contracted,rigidity);
  }
  Muscle modifyMuscle(int nodeNum,float mutability){
    int newc1 = c1;
    int newc2 = c2;
    if(random(0,1)<0.02*mutability*MUTABILITY_FACTOR){
      newc1 = int(random(0,nodeNum));
    }
    if(random(0,1)<0.02*mutability*MUTABILITY_FACTOR){
      newc2 = int(random(0,nodeNum));
    }
    float newR = min(max(rigidity*(1+r()*0.9*mutability*MUTABILITY_FACTOR),0.01),0.08);
    float maxMuscleChange = 1+0.025/newR;
    float newCL = min(max(contractLength+r()*mutability*MUTABILITY_FACTOR,0.4),2);
    float newEL = min(max(extendLength+r()*mutability*MUTABILITY_FACTOR,0.4),2);
    float newCL2 = min(newCL,newEL);
    float newEL2 = min(max(newCL,newEL),newCL2*maxMuscleChange);
    float newCT = contractTime;
    float newET = extendTime;
    if(random(0,1) < 0.5){ //contractTime is changed
      newCT = ((contractTime-extendTime)*r()*mutability*MUTABILITY_FACTOR+newCT+1)%1;
    }else{ //extendTime is changed
      newET = ((extendTime-contractTime)*r()*mutability*MUTABILITY_FACTOR+newET+1)%1;
    }
    return new Muscle(max(period+rInt(),0),
    newc1,newc2,newCT,newET,newCL2,newEL2,isItContracted(newCT,newET),newR);
  }
}
