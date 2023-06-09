def finalLargestPrime(number):
   index = 2
   while index*index < number:
     if number % index:
        index += 1

     else:
        number = number / index
   return number
print(int(finalLargestPrime(600851475143)))

         
         
   
 