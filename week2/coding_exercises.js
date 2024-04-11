// Q1
function findAndPrint(messages, currentStation){
    // your code here
    let stations1 = ['Songshan', 'Nanjing Sanmin', 'Taipei Arena', 'Nangjin Fuxing', 'Songjiang Nanjing',
                     'Zhongshan', 'Beimen', 'Ximen', 'Xiaonanmen', 'Chiang Kai-Shek Memorial Hall',
                     'Guting', 'Taipower Building', 'Gongguan', 'Wanlong', 'Jingmei', 'Dapinglin',
                     'Qizhang', 'Xiaobitan'];
    let stations2 = ['Songshan', 'Nanjing Sanmin', 'Taipei Arena', 'Nangjin Fuxing', 'Songjiang Nanjing',
                     'Zhongshan', 'Beimen', 'Ximen', 'Xiaonanmen', 'Chiang Kai-Shek Memorial Hall',
                     'Guting', 'Taipower Building', 'Gongguan', 'Wanlong', 'Jingmei', 'Dapinglin',
                     'Qizhang', 'Xindian City Hall', 'Xindian'];
    let stations3 = ['Xiaobitan', 'Qizhang', 'Xindian City Hall', 'Xindian'];

    // find the stations in messages values
    let judge_node = ['Songshan', 'Nanjing Sanmin', 'Taipei Arena', 'Nangjin Fuxing', 'Songjiang Nanjing',
                      'Zhongshan', 'Beimen', 'Ximen', 'Xiaonanmen', 'Chiang Kai-Shek Memorial Hall',
                      'Guting', 'Taipower Building', 'Gongguan', 'Wanlong', 'Jingmei', 'Dapinglin',
                      'Qizhang', 'Xindian City Hall', 'Xindian','Xiaobitan'];
    let new_messages = {};
    for (let k of Object.keys(messages)){
        for (let n of judge_node){
            if (messages[k].includes(n)){
                new_messages[k] = n;
            };
        };
    };

    // get distances between two stations
    const distance = function(n1, n2){
        if (n1 != 'Xiaobitan' && n2 != 'Xiaobitan'){
            return Math.abs(stations2.indexOf(n1) - stations2.indexOf(n2))
        }else if (stations1.includes(n1) && stations1.includes(n2)){
            return Math.abs(stations1.indexOf(n1) - stations1.indexOf(n2))
        }else if (stations3.includes(n1) && stations3.includes(n2)){
            return Math.abs(stations3.indexOf(n1) - stations3.indexOf(n2))
        };
    };
    

    let closestDistance = distance(currentStation, Object.values(new_messages)[0]);
    let closestCandidate = Object.keys(new_messages)[0];
    for (let j = 1; j < Object.values(new_messages).length; j++){
        if (closestDistance > distance(currentStation, Object.values(new_messages)[j])){
            closestDistance = distance(currentStation, Object.values(new_messages)[j]);
            closestCandidate = Object.keys(new_messages)[j];
        };
    };
    console.log(closestCandidate);
}
const messages={
"Bob":"I'm at Ximen MRT station.",
"Mary":"I have a drink near Jingmei MRT station.", 
"Copper":"I just saw a concert at Taipei Arena.", 
"Leslie":"I'm at home near Xiaobitan station.", 
"Vivian":"I'm at Xindian station waiting for you."
};
findAndPrint(messages, "Wanlong"); // print Mary 
findAndPrint(messages, "Songshan"); // print Copper 
findAndPrint(messages, "Qizhang"); // print Leslie 
findAndPrint(messages, "Ximen"); // print Bob 
findAndPrint(messages, "Xindian City Hall"); // print Vivian


////////////////////
// Q2
// your code here, maybe
let availability = {}; // store consultants schedule
let priority = {'price':[], 'rate':[]}; // store criteria priority

function book(consultants, hour, duration, criteria){
    // your code here
    if (Object.keys(availability).length === 0){
        let rate_seq = {};
        let rate_compare = [];
        let price_seq = {};
        let price_compare = [];
        for (let ind = 0; ind < consultants.length; ind++){
            availability[consultants[ind]['name']] = [];
            rate_seq[consultants[ind]['rate']] = consultants[ind]['name'];
            rate_compare.push(consultants[ind]['rate']);
            price_seq[consultants[ind]['price']] = consultants[ind]['name'];
            price_compare.push(consultants[ind]['price']);
        };

        // sort() -> for string compare; 
        // sort(function(a, b){return a - b}) -> for numerical compare;
        let rate_compare_sort = rate_compare.sort(function(a, b){return a - b}).reverse();
        let price_compare_sort = price_compare.sort(function(a, b){return a - b});
        
        for (let inds = 0; inds < consultants.length; inds++){
            priority['rate'].push(rate_seq[rate_compare_sort[inds]]);
            priority['price'].push(price_seq[price_compare_sort[inds]]);
        };
        
    };
    
    // check which consultant is available for the booking duration with criteria order
    for (let c of priority[criteria]){
        // criteria operation
        let temp = [];
        for (let i = hour; i <= hour+duration-1; i++){
            if (!availability[c].includes(i)){
                temp.push(i);
            }else{
                break
            };
        };
        
        if (temp.length == duration){
            console.log(c);
            availability[c] = availability[c].concat(temp);
            return c
        };
        
    };
    console.log('No Service');
    return 'No Service'

}
const consultants=[
{"name":"John", "rate":4.5, "price":1000}, 
{"name":"Bob", "rate":3, "price":1200}, 
{"name":"Jenny", "rate":3.8, "price":800}
];
book(consultants, 15, 1, "price"); // Jenny 
book(consultants, 11, 2, "price"); // Jenny 
book(consultants, 10, 2, "price"); // John 
book(consultants, 20, 2, "rate"); // John 
book(consultants, 11, 1, "rate"); // Bob 
book(consultants, 11, 2, "rate"); // No Service 
book(consultants, 14, 3, "price"); // John


//////////////
// Q3
function func(...data){
    // your code here
    let judge_unique = {};
    for (let name of [...data]) {
        if (name.length == 2 | name.length == 3){
            if (!Object.keys(judge_unique).includes(name[1])){
                judge_unique[name[1]] = [name];
            }else {
                judge_unique[name[1]].push(name);
            };
        }else if (name.length == 4 | name.length == 5){
            if (!Object.keys(judge_unique).includes(name[2])){
                judge_unique[name[2]] = [name];
            }else {
                judge_unique[name[2]].push(name);
            };
        };
    };
    
    // last check for uniqueness
    for (let answer of Object.values(judge_unique)){
        if (answer.length == 1){
            console.log(answer[0]);
            return answer[0];
        };
    };

    console.log('沒有');
    return '沒有'

}
func("彭大牆", "陳王明雅", "吳明"); // print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花"); // print 林花花 
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花"); // print 沒有 
func("郭宣雅", "夏曼藍波安", "郭宣恆"); // print 夏曼藍波安


//////////////
// Q4
// There is a number sequence: 0, 4, 8, 7, 11, 15, 14, 18, 22, 21, 25, ... 
// Find out the nth term in this sequence.

function getNumber(index){
    // your code here
    if (index == 0){
        console.log(0);
    }else{
        if (index%3 == 1){
            console.log(4+7*(Math.floor(index/3)));
        }else if (index%3 == 2){
            console.log(8+7*(Math.floor(index/3)));
        }else{
            console.log(7*(Math.floor(index/3)));
        };
    };

}
getNumber(1); // print 4 
getNumber(5); // print 15 
getNumber(10); // print 25 
getNumber(30); // print 70


/////////////
// Q5
function find(spaces, stat, n){
    // your code here
    let current_perfect = -1;
    let answer = -1; 
    for (let i in spaces){
        if (stat[i] == 1 && spaces[i]-n >= 0){
            if (current_perfect == -1){
                current_perfect = spaces[i]-n;
                answer = i;
            }else if (spaces[i]-n < current_perfect){ 
                current_perfect = spaces[i]-n;
                answer = i;
            };
        };
    };

    console.log(answer);

}
find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2); // print 5 
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4); // print -1 
find([4, 6, 5, 8], [0, 1, 1, 1], 4); // print 2
