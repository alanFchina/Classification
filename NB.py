from numpy import *
from fractions import Fraction
from decimal import *

class NaiveBayesClassifier(object):
    def __init__(self,numLab,prpro,step): #以类别个数初始化分类器
        self.seqances=[]
        self.step = step
        self.numLab = numLab
        self.dataMa = zeros((numLab,26,26))    #numLab个26*26矩阵
        self.dataMa3 = zeros((numLab,26,26,26)) #3个字符一组
        self.sumData = zeros(numLab)       #numLab个矩阵的各自的和
        self.labelMa = prpro               #先验概率

        self.P = []


    def loadDataSet(self,seqs): #输入训练数据，字符串数组
        i = 0
        for line in seqs:
            line = line.strip('\n')
            self.seqances.append(line)
            seqArray = bytes(line,encoding = 'utf-8')
            length = len(seqArray)
            for index in range(0,length-1):
                x = seqArray[index]-65
                y = seqArray[index+1] - 65
                self.dataMa[i,x,y]+=self.step
            for index in range(0,length-3):
                x = seqArray[index]-65
                y = seqArray[index+1] - 65
                z = seqArray[index+2] - 65
                self.dataMa3[i,x,y,z]+=self.step 
            self.sumData[i] = sum(self.dataMa[i])
            i+=1

    def test_ofature(self,seq): #传入字符数组，输出一个一行二列数组,分别记录最大概率和类别
        leng = len(seq)
        output = []
        maxP = 0
        sumPro = Decimal(0)
        lab = 0
        score = []
        for i in range(0,self.numLab): #计算一条特征序列概率最大的类
            sumProb = Decimal(0)
            a = Decimal(leng)
            b = Decimal(len(self.seqances[i]))
            if a==0:
                a=1
            if a>b:
                score.append(b/a)
            else:
                score.append(a/b)
            
            prob = Decimal(1)
            tote = Decimal(self.sumData[i]+400)
            for j in range(0,leng-1):
                x = seq[j] - 65
                y = seq[j+1] - 65
                if j==0:
                    prob *= Decimal(self.dataMa[i,x,y]+1)/Decimal(tote)
                else:
                    z = seq[j-1] - 65
                    prob *= Decimal(self.dataMa3[i,z,x,y]+1)/Decimal(self.dataMa[i,x,y]+400)
            prob=prob*Decimal(self.labelMa[i])
            sumPro += prob
            if prob>=maxP:
                maxP = prob
                lab = i
        if sumPro ==0:
            print('zero')
        maxp = maxP*score[lab]/sumPro
        output.append(maxp)
        output.append(lab)
        return output

    def test_oSeq(self,seq):#传入类数行字符串，输出类别。
        output = []
        output.append(0)
        output.append(0)

        for each in seq:
            each = each.strip('\n')
            seqArr = bytes(each,encoding='utf-8')
            re = self.test_ofature(seqArr)
            self.P.append(re[0])
            if re[0]>=output[0]:
                output[0] = re[0]
                output[1] = re[1]

        return output
        

