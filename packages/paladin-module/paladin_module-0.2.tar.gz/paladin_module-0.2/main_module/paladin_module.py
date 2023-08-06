def square(x):
    #Возвращает квадрат числа x.
    return x ** 2
def cube(x):
    #Возвращает куб числа x.
    return x ** 3
def fibonacci(n):
    #Возвращает n-ое число Фибоначчи.
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
def is_prime(n):
    #Проверяет, является ли число простым.
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
def collatz(num):
    #Уравнение 3х+1
    while num != 1:
        print(num, end=' ')
    if num % 2 == 1:
        num = 3 * num + 1
    else:
        num = num // 2
    print(num)
    collatz(num)