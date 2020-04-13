import csv
import os
import locale
from datetime import datetime
from functools import cmp_to_key
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 


lines = []

class Record(object):

    def __init__(self, date, description, isDebetCard, amount):
        self.date = date
        self.description = description
        self.isDebetCard = isDebetCard
        self.amount = amount

    def __str__(self):
        return self.date + "/"+ self.description+ "/" + str(self.amount)+"/" + str(self.isDebetCard)

for x in os.listdir('.'):
    if os.path.splitext(x)[1] == '.csv':
        with open(x,'r',encoding='gb2312')as f:
            f_csv = csv.reader(f)
            isValidLine = False
            isDebetCard = True
            
            for row in f_csv:
                if isValidLine and len(row) > 1:
                    row.insert(0,isDebetCard)
                    lines.append(row)
                if not isValidLine:
                    if len(row) > 0 and row[0].strip() == '对账标志':
                        isValidLine = True
                        isDebetCard = False
                    if len(row) > 0 and row[0].strip() == '交易日期':
                        isValidLine = True

records = []


# [True, '\t20200304', '\t17:07:26', '', '2.00', '582.92', '\tN5CP', '\t支付宝 - 扬州市民卡有限责任公司']
# [True, '\t20200303', '\t14:00:50', '100.00', '', '584.92', '\t本行CRS存款', '\t本行 CRS 异地存款  00258178 00405']
# [True, '\t20200303', '\t13:47:35', '', '20.00', '484.92', '\t专业版移动证书手续费', '\t专业版移动证书工本费（经典版）']
# [True, '\t20200302', '\t20:20:08', '', '50.00', '504.92', '\tU1PY', '\t财付通 - 微信支付 - 微信转账']
# [False, '\t未确认', '\t2020-03-31', '\t2020-04-01', '\t财付通 - 满记甜品', '7473', '19.00', '\t', '\t']
# [False, '\t未确认', '\t2020-03-31', '\t2020-04-01', '\t财付通 - 颜路边摊火锅（吾悦广', '7473', '68.00', '\t', '\t']
# [False, '\t未确认', '\t2020-03-31', '\t2020-04-01', '\t美团点评 - 美团支付 - 美团支付', '7473', '88.89', '\t', '\t']
# [False, '\t未确认', '\t2020-04-02', '\t2020-04-03', '\t支付宝 - 赵启琴', '7473', '19.50', '\t', '\t']


# 2020-02-16 * "基金提现"
#   Assets:Current:招商银行借记卡                     500 CNY
#   Assets:Investment:基金股票

for row in lines:
    isDebetCard = row[0]
    if (isDebetCard):
        tmpDate = row[1].strip()
        tmpDate = tmpDate[0:4] + "-" + tmpDate[4:6] + "-" + tmpDate[6:8]
        amount = 0.0
        if(row[3] == ''):
            amount = 0 - float(row[4])
        elif(row[4] == ''):
            amount = float(row[3])
        records.append(Record(date=tmpDate,description= row[7].strip(),amount= amount, isDebetCard = isDebetCard))
    else:
        tmpAmount = 0-locale.atof((row[6]))
        tmpRecord = Record(date=row[2].strip(),description=row[4].strip(),amount=tmpAmount,isDebetCard=isDebetCard)
        records.append(tmpRecord)

        
        # records.append(Record(date=row[2]))

        # records.append(Record(date=))

def compareDate(x,y):
    difference = datetime.strptime(x.date,'%Y-%m-%d') - datetime.strptime(y.date,'%Y-%m-%d')
    return difference.days



records.sort(key=cmp_to_key(compareDate))

with open('result.bean', 'w') as f:
    for record in records:
        f.write(record.date + " * \"" + record.description + "\"\n")
        if(record.isDebetCard):
            f.write("  Assets:Current:招商银行借记卡\t" + str(record.amount) + " CNY\n")
        else:
            f.write("  Liabilities:Current:招商银行贷记卡\t" + str(record.amount) + " CNY\n")
        f.write("  Expenses:Undefined:待定\n\n")
        

