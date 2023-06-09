def sum_even_fabonancci(limit):

    num1 = 0
    numb2 = 1
    next_value = 0
    sum = 0

    while next_value < limit:
        next_value = num1 + numb2
        num1 = numb2
        numb2 = next_value
        if next_value % 2 == 0:
            sum += next_value
    return sum
print(sum_even_fabonancci(4000000))


