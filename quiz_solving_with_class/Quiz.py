# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

class quiz:
    def __init__(self, fname):
        import os 
        
        path = os.path.join('./data', fname)
        f = open(path,'r')
        lines = f.readlines()
        f.close()
        
        student_data = []
        
        for line in lines:
            std_no = line[0:6]
            email = line[6:10]
            kor = int(line[10:13])
            eng = int(line[13:16])
            math = int(line[16:19])
            sci = int(line[19:22])
            hist = int(line[22:25])
            tot = int(line[25:28])
            mcode = line[28:29]
            acode = line[29:30]
            lcode = line[30:31]
            temp = [std_no,email,kor,eng,math,sci,hist,tot,mcode,acode,lcode]
            student_data.append(temp)
        
        self.data = student_data
        print(self.data[:10])

    
    def quiz_1(self):
        res = []

        for line in self.data:
            if line[-1] == "B":
                temp = line[2] + line[3]
                temp_res = [line[0], temp]
                res.append(temp_res)
        
        res = sorted(res, key=lambda res: res[1])
        
        self.quiz_1 = int(res[4][0])

        return self.quiz_1


    def quiz_2(self):
        res = []

        for line in self.data:
            if line[10]=='B':
                temp = line[2] + line[3]
                res.append(temp)
        
        self.quiz_2 = max(res)

        return self.quiz_2
    
    def quiz_3(self):
        res = 0

        for line in self.data:
            temp = line[3] + line[4]
            if temp >= 120:
                point = 0
                if line[8]=='A':
                    point = 5
                elif line[8]=='B':
                    point = 15
                else:
                    point = 20
                    
                res += (point + line[7])
        
        self.quiz_3 = res

        return self.quiz_3
    
    def quiz_4(self):
        res = 0
        temp = 0
        
        for line in self.data:
            if line[10] != "C":
                if line[-1] == "A":
                    temp = line[2] + 5
                elif line[-1] == "B":
                    temp = line[2] + 10
                else:
                    temp = line[2] + 15
                
            if temp >= 50:
                res += 1

        self.quiz_4 = res

        return self.quiz_4

    def save(self, fname = 'answers.txt'):
        import os
        
        f = open(fname,'w')
        f.write("{}\n".format(self.quiz_1))
        f.write("{}\n".format(self.quiz_2))
        f.write("{}\n".format(self.quiz_3))
        f.write("{}\n".format(self.quiz_4))
        f.close()

