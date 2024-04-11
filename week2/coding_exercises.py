# Q1
def find_and_print(messages, current_station):
    # your code here
    stations1 = ['Songshan', 'Nanjing Sanmin', 'Taipei Arena', 'Nangjin Fuxing', 'Songjiang Nanjing',
                'Zhongshan', 'Beimen', 'Ximen', 'Xiaonanmen', 'Chiang Kai-Shek Memorial Hall',
                'Guting', 'Taipower Building', 'Gongguan', 'Wanlong', 'Jingmei', 'Dapinglin',
                'Qizhang', 'Xiaobitan']
    stations2 = ['Songshan', 'Nanjing Sanmin', 'Taipei Arena', 'Nangjin Fuxing', 'Songjiang Nanjing',
                'Zhongshan', 'Beimen', 'Ximen', 'Xiaonanmen', 'Chiang Kai-Shek Memorial Hall',
                'Guting', 'Taipower Building', 'Gongguan', 'Wanlong', 'Jingmei', 'Dapinglin',
                'Qizhang', 'Xindian City Hall', 'Xindian']
    stations3 = ['Xiaobitan', 'Qizhang', 'Xindian City Hall', 'Xindian']

    node_judge = line2 + ['Xiaobitan']
    new_messages = {}
    for k, v in messages.items():
        for n in node_judge:
            if n in v:
                new_messages[k] = n
    
    
    def distance(station1, station2):
        if station1 != 'Xiaobitan' and 'station2' != 'Xiaobitan':
            return abs(line2.index(station1) - line2.index(station2))
        else:
            try:
                return abs(line1.index(station1) - line1.index(station2))
            except:
                return abs(line3.index(station1) - line3.index(station2))
    
    candidate = ''
    d = 0
    for k, v in new_messages.items():
        if candidate == '':
            candidate = k
            d = distance(v, current_station)
            
        else:
            if distance(v, current_station) < d:
                candidate = k
                d = distance(v, current_station)
                
    print(candidate)

messages={
"Leslie":"I'm at home near Xiaobitan station.", 
"Bob":"I'm at Ximen MRT station.",
"Mary":"I have a drink near Jingmei MRT station.", 
"Copper":"I just saw a concert at Taipei Arena.", 
"Vivian":"I'm at Xindian station waiting for you."
}
find_and_print(messages, "Wanlong") # print Mary 
find_and_print(messages, "Songshan") # print Copper 
find_and_print(messages, "Qizhang") # print Leslie 
find_and_print(messages, "Ximen") # print Bob 
find_and_print(messages, "Xindian City Hall") # print Vivian


##############
# Q2
# your code here, maybe
availability = {}
priority = {}
    
def book(consultants, hour, duration, criteria):
    # your code here
    global availability
    global priority
    if availability == {}:
        priRate = {}
        priPrice = {}
        for c in consultants:
            availability[c['name']] = []
            priRate[c['rate']] = c['name']
            priPrice[c['price']] = c['name']

        priority = {'rate':[priRate[r] for r in sorted(priRate)[::-1]], 'price':[priPrice[p] for p in sorted(priPrice)]}
    
    this_priority = priority[criteria]
    for j in this_priority:
        temp = []
        for i in range(duration):
            if hour+i not in availability[j]:
                temp.append(hour+i)
            else:
                break
        
        if len(temp) == duration:
            availability[j] += temp
            print(j)
            return j
        
    print('No Service')
    return 'No Service'


consultants=[
{"name":"John", "rate":4.5, "price":1000}, 
{"name":"Bob", "rate":3, "price":1200}, 
{"name":"Jenny", "rate":3.8, "price":800}
]
book(consultants, 15, 1, "price") # Jenny 
book(consultants, 11, 2, "price") # Jenny 
book(consultants, 10, 2, "price") # John 
book(consultants, 20, 2, "rate") # John 
book(consultants, 11, 1, "rate") # Bob 
book(consultants, 11, 2, "rate") # No Service 
book(consultants, 14, 3, "price") # John


##############
# Q3
# -> 5 words aim at the 3rd word
def func(*data):
    # your code here
    unique_judge = {}
    for strd in [*data]:
        if len(strd) == 2 or len(strd) == 3:
            middle = strd[1]
        elif len(strd) == 4 or len(strd) == 5:
            middle = strd[2]
        
        if middle not in unique_judge.keys():
            unique_judge[middle] = [strd]
        else:
            unique_judge[middle].append(strd)
            
    for answer in unique_judge.values():
        if len(answer) == 1:
            print(answer[0])
            return answer[0]
        
    print('沒有')
    return '沒有'


func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花 
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有 
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安


##############
# Q4
# There is a number sequence: 0, 4, 8, 7, 11, 15, 14, 18, 22, 21, 25, ... 
# Find out the nth term in this sequence.
def get_number(index):
    # your code here 
    if index == 0:
        print(0)
    elif index > 0:
        if index%3 == 1:
            print(4+7*(index//3))
        elif index%3 == 2:
            print(8+7*(index//3))
        elif index%3 == 0:
            print(7*(index//3))

get_number(1) # print 4
get_number(5) # print 15 
get_number(10) # print 25 
get_number(30) # print 70


##############
# Q5
def find(spaces, stat, n):
    # your code here
    available_spaces = {}
    for ind, true in enumerate(stat):
        if true == 1 and spaces[ind]-n >= 0:
            available_spaces[spaces[ind]-n] = ind
    if available_spaces == {}:
        print(-1)
        
    else:
        print(available_spaces[min(available_spaces.keys())])

find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2) # print 5 
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4) # print -1 
find([4, 6, 5, 8], [0, 1, 1, 1], 4) # print 2
