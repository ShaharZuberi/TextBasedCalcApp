# TextBasedCalcApp
Welcome to the Text based calculator.

## Evaluation steps
1. First, we look to **replace assignment shortcuts** in the string such as +=, -=, *=, /=
2. Second, we look for **brackets** and try and solve them using **recursion**
3. Third, we interpret and replace the value of **unary operations** such as ++ and --
4. Fourth, we resolve **concatenated signs** such as 5---4 which is similar to 5-4
5. Fifth and last, we compute the expression based on **basic arithmetic computation** +-/*

##### Test execution
```bash
$ python Tests.py
``` 

## Valid expressions for example:
1. a=5+5+5*2/10-3
2. a=1
3. b=++a
4. c=a++
5. d=b+++1
6. e=++d+1

#### Complex problems:
Multiple signs:
1. a=-3+-+-+-2
2. b=10----9 

Multipliction of negativs
3. c=-4-6*-6*-4-2