"""
Copyright (c) 2023, Alexander Blinov


Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice,
 this list of conditions and the following disclaimer.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Credits:

getDividers() function by Leonid Merkulov
maxDividerNotEqualsToNumber() function by Leonid Merkulov

decToBase() function by Alexey Bolshakov

ИНФОРМАЦИЯ:
  Библиотека предоставлена в ознакомительных целях. Это значит, что
вы можете воспользоваться реализацией предоставленных здесь функций на ЕГЭ, ВЫУЧИВ необходимые
НАИЗУСТЬ.

"""

import re
import turtle as t
import time


#Функция, проверяющая, является ли число палиндромом
#Автор: Александр Блинов
def isPalindrome(number):
    if str(number) == str(number)[::-1]:
        return True
    else:
        return False


#Получить делители числа
#Автор: Леонид Меркулов
def getDividers(number):
    mas = []

    if int(number ** 0.5) ** 2 == number:
        mas.append(int(number ** 0.5))

    for i in range(1, int(number ** 0.5) + 1):
        if number % i == 0:
            mas.append(i)
            mas.append(number // i)

    return sorted(list(set(mas)))


#Получить максимальный делитель, не равный самому числу
#Автор: Леонид Меркулов
def maxDividerNotEqualsToNumber(number):
    mas = []

    if int(number ** 0.5) ** 2 == number:
        mas.append(number ** 0.5)

    for i in range(2, int(number ** 0.5)):
        if number % i == 0:
            mas.append(i)
            return number // i


#Получить цифры числа на нечётных индексах
#Автор: Александр Блинов
def notEvenIndexDigits(number):
    ret = []

    for k in range(1, len(str(number)) + 1, 2):
        ret.append(k)

    return ret


#Получить нечётные цифры числа
#Автор: Александр Блинов
def notEvenDigits(number):
    ret = []

    for k in str(number):
        if int(k) % 2 != 0:
            ret.append(int(k))

    return ret


#Получить сумму цифр
#Автор: Александр Блинов
def sumOfDigits(number):
    ret = 0

    for g in str(number):
        ret += int(g)

    return ret

#Перевод числа из десятичной системы счисления в любую с помощью словаря
#Автор: Алексей Большаков
def decToBase(a, base):
    dict_ = '0123456789abcdefghijklmnop'
    s = ''
    while a != 0:
        s = str(dict_[a % base]) + s
        a //= base
    return s

#Проверка маски, которая встречается в 25 номере(на момент ЕГЭ 2023). Переводит маску в регулярное выражение и осуществляет поиск по нему
#Автор: Александр Блинов
def checkMask(number, mask):
    return bool(re.compile(mask.replace('?', '[0-9]').replace('*', '([0-9]+|)') + "$").match(str(number)))


#Функция, которая принимает текстовые команды черепахи из задания и переводит их в команды для черепахи из модуля turtle.
#Применяется в 6 задании. Эта функция сделана для проверки правильности работы вашего алгоритма, не стоит учить эту функцию на ЕГЭ.
#На вход функция принимает массив из строк алгоритма задания. Вы можете дополнительно указать параметры сетки.
#Примечание: Код должен передаваться в функцию в виде массива строк. Также вы можете загрузить код из файла, передав в аргумент
#команду open()
#Автор: Александр Блинов
def turtle_6(code, gridSizeX = 16, gridSizeY = 16, gridScale = 20, gridDotSize = 3):

    cmds = []

    for line in code:

        commands = re.findall("[a-zA-ZА-Яа-яËё]+ [А-Яа-я0-9]+", line)

        cont = False

        for command in commands:
            op = command.split()[0]
            value = command.split()[1]

            if op == "Повтори":
                for i in range(int(value)):
                    for j in range(1, len(commands)):
                        cmds.append(commands[j])

                cont = True
                break

            else:
                cmds.append(command)

        if cont:
            continue


    turtleFuncs = {"Вперёд": t.forward, "Направо": t.right, "Налево": t.left, "Назад": t.back, "Поднять": t.penup, "Опустить": t.pendown}

    for x in range(gridSizeX):
        for y in range(gridSizeY):
            t.setx(x * gridScale)
            t.sety(y * gridScale)
            t.pendown()
            t.dot(gridDotSize)
            t.penup()

    t.setx(0)
    t.sety((gridSizeY - 1) * gridScale)
    t.pendown()

    for cmd in cmds:
        if cmd != "Поднять хвост" and cmd != "Опустить хвост":
            op = cmd.split()[0]
            value = int(cmd.split()[1])

            if op != "Налево" and op != "Направо":
                value *= gridScale

            turtleFuncs[op](value)
        else:
            op = cmd.split()[0]
            turtleFuncs[op]()

    t.done()


#Функция, которая принимает код для исполнителя "Редактор" из задания 12 и возвращает перевод этого кода на Python для дальнейшего использования.
#Передав True во второй параметр, функция выведет код.
#Примечание: Код должен передаваться в функцию в виде массива строк. Также вы можете загрузить код из файла, передав в аргумент
#команду open(). Необходимо соблюдать все табуляции для корректной работы. Функция возвращает код также в виде массива.
#Автор: Александр Блинов
def toPythonCode_12(s, printCode = False):
    code = []
    code.append("string = 'ВАША СТРОКА'")
    for line in s:
        l = line.replace("НАЧАЛО", "").replace("заменить С КОНЦА СТРОКИ", "pass #Замена с конца строки ещё не реализована").replace("КОНЕЦ ЕСЛИ", "").replace("КОНЕЦ ПОКА", "").replace("ПОКА", "while").replace("КОНЕЦ", "").replace("ИНАЧЕ ЕСЛИ", "elif").replace("ЕСЛИ", "if").replace("НЕ", "not").replace("ИНАЧЕ", "else:").replace("ИЛИ", "or").replace("И", "and").replace("ТО ", "").replace("\n", "")

        for tokenFound in re.findall("нашлось \([A-Za-z0-9<>]+\)", line):
            repl = "'" + re.findall("\([A-Za-z0-9<>]+\)", tokenFound)[0][1:-1] + "' in string"

            l = l.replace(tokenFound, repl)


        for tokenReplace in re.findall("заменить \([A-Za-z0-9<>]+, [A-Za-z0-9<>]+\)", line):
            fnd = re.findall("[A-Za-z0-9<>]+, [A-Za-z0-9<>]+", tokenReplace)[0].replace(', ', ',')

            repl = "string.replace('" + fnd.split(',')[0] + "', '" + fnd.split(',')[1] + "')"

            l = l.replace(tokenReplace, repl)

        if "while" in l or "if" in l:
            l += ":"

        if len(l) != 0:
            code.append(l)

    if printCode:
        for pl in code:
            print(pl)

    return code

#Простой бенчмарк для получения прмерного времени работы какой-либо функции
def benchmark(function):
    def wrapper():
        t1 = time.time()
        function()
        t2 = time.time() - t1
        print(f"[EGETools Benchmark] Result: {t2}")

    return wrapper
