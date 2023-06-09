#Check how many multiple of 3  and 5 in the 1000
sum_ = 0
index = 999

while index > 0:
    num1 = index % 3
    numb2 = index % 5

    if num1 == 0 or numb2 == 0:
       print(index)
       sum_ = sum_ + index
    index = index - 1

print(sum_)


