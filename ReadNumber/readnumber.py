# Python code

units = ["", "thousand", "million", "billion", "", "trillion"]

one_tens = ["", "one", "two", "three", "four", "five", "six", "seven", "eight",
               "night", "ten", "elevent", "twelve", "thirdteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eightteen", "nineteen", "twenty"]

tys = ["","", "twenty", "thirdty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

def append_head(head, tail):
    if(tail == ""):
        return head
    if(head == ""):
        return tail
    return head + " " + tail

def read_out_loud(number):
    answer = ""

    if(number == 0):
        return "zero"
    
    while number > 0:
        
        number_tri = number % 10**12
        number = number // 10**12

        temp = read_every_trillion(number_tri) 
        
        if(number > 0):
            temp = append_head(units[len(units) - 1], temp)

        answer = append_head(temp, answer)
        
    return answer

def read_every_trillion(number):
    unit_index = 0
    answer = ""
    while number > 0:        
        number_3 = number % 1000
        number = number // 1000
        answer = append_head(read_3_digits(number_3, unit_index), answer)
        unit_index += 1
        
    return answer

def read_3_digits(number_3, unit_index):
    if(number_3 == 0):
        return ""
    
    answer = ""    
    n_2 = number_3 % 100

    if n_2 <= 20:
        answer = one_tens[n_2]
    else:
        answer = tys[n_2//10]
        if(n_2 % 10 != 0):
            answer += "-" + one_tens[n_2 % 10]

    if number_3 // 100 != 0:
        answer = one_tens[number_3 // 100] + " hundred" +  answer

    answer = append_head(answer, units[unit_index])
    return answer
        
    
    
if __name__ == '__main__':
    number = 1000000000000000000010100
    answer = read_out_loud(number)
    print(answer)
