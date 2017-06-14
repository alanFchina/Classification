from fractions import Fraction
from numpy import *
from NB import *
from decimal import *

getcontext().prec=50

prproR = open('prpro.txt','r')

lines = prproR.readlines()         #读取并处理先验概率数据
pro =[] #先验概率
for each in lines:
    each = float(Fraction(each))
    pro.append(each)
prproR.close()

trainData = []               #处理训练和预测数据
forcData = []
sub_forcData = []
dataR = open('train3.fasta')
i = 0
for line in dataR:
    if i<=55:
        trainData.append(line)
    elif 55<i<=111:          #每56条同一预测序列数据存入一个sub_forcData
        sub_forcData.append(line)
        if i==111:
            i=55
            forcData.append(sub_forcData)
            sub_forcData=[]
    i+=1
size = len(forcData)  #预测序列条数
dataR.close()

nb = NaiveBayesClassifier(56,pro,1)

nb.loadDataSet(trainData)

num = 0                                         #输出结果，并将错误数据录入errorData.txt中
fw = open('errorData.txt','w')
for i in range(0,size):
    re = nb.test_oSeq(forcData[i])
    if i<30:
        if re[1] != i:
            fw.write(str(i)+' to '+str(re[1])+'\n')
            fw.write('F: '+str(nb.P[re[1]])+'\n')
            fw.write('R: '+str(nb.P[i])+'\n')
            seqnum = 0
            for item in forcData[i]:
                if seqnum ==i:
                    fw.write('R-----------\n')
                    fw.write(str(trainData[i]))
                    fw.write(str(item))
                    fw.write('-----------\n')
                elif seqnum==re[1]:
                    fw.write('F-----------\n')
                    fw.write(str(trainData[re[1]]))
                    fw.write(str(item))
                    fw.write('-----------\n')
                else:
                    fw.write(str(item))
                seqnum +=1
                
            fw.write('----------------------------------------\n')
            print("**")
            num+=1
    else:
        j = (i-30)//3
        if re[1]-30!=j:
            fw.write(str(j+30)+' to '+str(re[1])+'\n')
            fw.write('F: '+str(nb.P[re[1]])+'\n')
            fw.write('R: '+str(nb.P[j+30])+'\n')
            seqnum = 0
            for item in forcData[i]:
                if seqnum ==j+30:
                    fw.write('R-----------\n')
                    fw.write(str(trainData[seqnum]))
                    fw.write(str(item))
                    fw.write('-----------\n')
                elif seqnum==re[1]:
                    fw.write('F-----------\n')
                    fw.write(str(trainData[re[1]]))
                    fw.write(str(item))
                    fw.write('-----------\n')
                else:
                    fw.write(str(item))
                seqnum +=1
                
            fw.write('----------------------------------------\n')
            print('**')
            num+=1
    print(re)
    nb.P=[]
print(num)
print((108-num)/108)
fw.close()

        
