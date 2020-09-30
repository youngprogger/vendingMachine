class vending():

    def __init__(self):
        self.CanWork = True
        # Список из списков
        # Каждый элемент - название, количество и цена
        self.Goods = [
            ['Coca Cola', 15, 210],
            ['Mtn Dew', 15, 215],
            ['Hamburger', 15, 402],
            ['Choco Pie', 15, 179],
            ['Sandwich', 15, 364]

        ]
        # Какие монеты/купюры принимает автомат
        self.AcceptCoin = [50, 100, 200, 500]
        # Сколько есть монет для сдачи (номинал и количество)
        self.HaveCoin = [
            [1, 400],
            [2, 400],
            [5, 400],
            [10, 400]
        ]
        # История полученных банкнот (вообще)
        self.History = []
        # История полученных банкнот (за последнюю загрузку)
        self.LastHistory = []

    # Вывести список доступных для продажи товаров
    def printState(self):
        for g in self.Goods:
            if int(g[2]) <= self.Sum:
                print(g[0], " по цене ", g[2])

    # Проверить, допустима ли купюра
    def checkCoin(self, coin):
        for test in self.AcceptCoin:
            if test == coin: return True
        return False

    # Определить, остался ли хоть один товар
    def setCanWork(self):
        for product in self.Goods:
            if int(product[1]) != 0: return True
        return False

    # Выдать сдачу.
    # начиная с последней монеты в списке
    # если она есть в наличии и меньше номиналом, чем требуется сдача
    # добавить в список
    def MakeChange(self, money):
        result = []
        self.OK = True  # Сдача выдана успешно
        index = len(self.HaveCoin) - 1
        while money > 0:
            if (self.HaveCoin[index][1] > 0) and money >= self.HaveCoin[index][0]:
                self.HaveCoin[index][1] -= 1
                result += [self.HaveCoin[index][0]]
                money -= self.HaveCoin[index][0]
            else:
                index -= 1
                if index < 0:
                    print("Сдачи не будет")

                    # вернуть сдачу на место

                    for r in result:
                        # узнать, что за монетка
                        for index in range(len(self.HaveCoin)):
                            if self.HaveCoin[index][0] == r:
                                # вернуть обратно в кассу
                                self.HaveCoin[index][1] += 1
                                break

                    self.OK = False
                    return result
        return result

    # Принять купюру или список купюр (через пробел)
    # негодные возвращает
    # годные суммирует
    def getCoin(self):
        paylist = input("Внесите, пожалуйста, деньги (можно несколько значений через пробел) : ")
        hasgood = False
        for coin in paylist.split():
            try:
                intcoin = int(coin)
                if self.checkCoin(intcoin):
                    self.Sum += intcoin
                    hasgood = True
                    self.LastHistory += [intcoin]  # добавить в историю
                else:
                    print('Данный вид купюры не поддерживается автоматом ', coin)
            except:
                print('Данный вид купюры не поддерживается автоматом ', coin)
        return hasgood

    # Функция "Сервис". Вызывается при вводе некоего ключевого слова
    def Service(self):
        maxp = 15
        maxc = 400
        for index in range(len(self.Goods)):
            self.Goods[index][1] = maxp
        for index in range(len(self.HaveCoin)):
            self.HaveCoin[index][1] = maxc
        print("Купюры, находящиеся в автомате")
        print(self.History)
        self.History = []

    # Функция "Текущее состояние". Вызывается при вводе другого ключевого слова
    def Test(self):
        for index in range(len(self.Goods)):
            print(self.Goods[index])
        for index in range(len(self.HaveCoin)):
            print(self.HaveCoin[index])

    # Основной метод автомата
    def step(self):

        self.Sum = 0
        while True:

            # Получить деньги
            if not self.getCoin(): continue
            self.printState()
            print("Для просмотра состояния (ассортимента) ,или если вас интересуют другие товары, введите команду test")
            print("Для завершения работы автомата введите команду exit")
            print("Для возврата купюр введите команду return")

            product = input("Введите название товара (или Enter, если  недостаточно денег на покупку)   = ")
            # Если Enter, то продолжить ввод денег
            if product == "": continue

            # Если команда "сервисное обслуживание"
            if product == "srvop17":
                self.Service()
                print('Внесенный залог ', self.Sum, ",купюрами ", self.LastHistory, "выдан!")
                self.Sum = 0
                self.LastHistory = []
                continue

            # Если команда "проверка"
            if product == "test":
                self.Test()
                print('Внесенный залог ', self.Sum, ",купюрами ", self.LastHistory, "выдан!")
                self.Sum = 0
                self.LastHistory = []
                continue

            # Если команда "закончить"
            if product == "exit":
                print('Внесенный залог ', self.Sum, ",купюрами ", self.LastHistory, "выдан!")
                self.Sum = 0
                self.CanWork = False
                self.LastHistory = []
                return

            # Если команда "верни деньги!"
            if product == "return":
                print('Внесенный залог ', self.Sum, ",купюрами ", self.LastHistory, "выдан!")
                self.Sum = 0
                self.LastHistory = []
                return

            # Найти продукт по имени
            found = None
            foundindex = 0
            for goods in self.Goods:
                if goods[0] == product:
                    found = goods
                    break
                foundindex += 1
            # Не нашел
            if not found:
                print(product, " К сожалению, в автомате не имеется введенного продукта ")
                print('Вернул ваш залог', ",купюрами", self.LastHistory, "рублей!")
                self.Sum = 0
                self.LastHistory = []

                continue

            # Нашел, но кончился
            Exists = int(found[1]) > 0
            if not Exists:
                print('К сожалению, продукт закончился ', product)
                print('Внесенный залог ', self.Sum, ",купюрами ", self.LastHistory, "выдан!")
                self.Sum = 0
                self.LastHistory = []
                continue

            # Если есть, но дороже
            Need = int(found[2])
            if Need > self.Sum:
                print('Вы ввели недостаточную сумму')
                continue
            # Выдача сдачи (список выпавших монеток)
            temp = self.MakeChange(self.Sum - Need)
            if not self.OK:
                self.Sum = 0
                print('Внесенный залог ', self.Sum, ",купюрами ", self.LastHistory, "выдан!")
                self.LastHistory = []
                continue

            print('Возьмите,пожалуйста, вашу сдачу ', temp)
            self.History += self.LastHistory
            self.LastHistory = []
            # Продажа
            self.Goods[foundindex][1] -= 1
            print('**** ', product, ' выдан! *******')
            break
        # Определить возможность дальнейшей работы
        self.CanWork = self.setCanWork()
        return


