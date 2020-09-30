from Vending import vending

v = vending()
while v.CanWork:
    v.step()

print("Работа окончена,тяжелый денек сегодня выдался!")
