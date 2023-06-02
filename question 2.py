numb1=0
numb2=1
temp=1
sum=0

while sum<4000000:
    temp=numb1+numb2

    numb1=numb2
    numb2=temp

    
    if temp % 2 ==0:
     sum = sum + temp
   
 print(sum)
    	
