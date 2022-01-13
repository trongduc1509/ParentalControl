from __future__ import annotations
from datetime import datetime
from typing import Final

NONE: Final = -1

class myTime:
    def __init__(self, start, end, duration, interrupt, sum):
        self.start = start;
        self.end = end;
        self.duration = duration;
        self.interrupt = interrupt;
        self.sum = sum;

    def check(self, checkingTime: datetime):
        tempTime = checkingTime.replace(2001,1,1)
        return self.start < tempTime < self.end

    def __repr__(self) -> str:
        d_str = f' {self.duration}' if self.duration != NONE else ''
        i_str = f' {self.interrupt}' if self.interrupt != NONE else ''
        s_str = f' {self.sum}' if self.sum != NONE else ''
        return f'F{self.start.strftime("%H:%M")} T{self.end.strftime("%H:%M")}{d_str}{i_str}{s_str}'

def str_to_myTime(input_str: str) -> myTime:
    tempDict = {}
    for item in map(lambda splittedStr: (splittedStr[0], splittedStr[1:]), input_str.split()):
        tempDict[item[0]] = item[1]
    start = datetime.strptime(tempDict['F'],'%H:%M').replace(2001,1,1)
    end = datetime.strptime(tempDict['T'],'%H:%M').replace(2001,1,1)
    duration = int(tempDict['D']) if 'D' in tempDict else NONE
    interrupt = int(tempDict['I']) if 'I' in tempDict else NONE
    sum = int(tempDict['S']) if 'S' in tempDict else NONE
    return myTime(start,end,duration,interrupt,sum)


class account:
    currentTF: myTime | None

    def __init__(self,currentTF,userRight,currentUsed=0,usedInTF=0) -> None:
        self.currentTF = currentTF
        self.userRight = userRight
        self.currentUsed = currentUsed
        self.usedInTF = usedInTF

    def __repr__(self) -> str:
        return f'{self.currentTF} cU{self.currentUsed} tU{self.usedInTF} USER.{self.userRight}'

def str_to_account(input_str: str) -> account:
    cU = input_str.find('cU')
    uR = input_str.find('USER.')
    currentTF = str_to_myTime(input_str[:cU-1])
    userRight = input_str[uR+5:]
    tempDict = dict(map(lambda x: (x[:2], x[2:]), input_str[cU:uR-1].split()))
    return account(currentTF,userRight,int(tempDict['cU']),int(tempDict['tU']))
