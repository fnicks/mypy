# импорт зависимостей
import random
import asyncio
from names import russian_names
import openai

# API ключ OPENAI
openai.api_key = "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"

# Создание класса человек
class Person:
    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
    # Фунция генерации информации на основе входных данных, используя Chat GPT    
    async def generate_info(self, personInfo, infoPrompt):
        prompt = f"{personInfo} - Пожалуйста сгенерируй предложение от моего лица {infoPrompt} (очень коротко)."
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7
        )
        info = response.choices[0].text.strip()
        return info
    # Функция поздороваться и записать био в файл
    async def say_hello(self):
        # "года" (в родительном падеже множественного числа) используется для чисел, оканчивающихся на 2, 3, 4, кроме 12, 13, 14.
        if self.age % 10 in [2, 3, 4] and self.age % 100 not in [12, 13, 14]:
            showAge = "года"
        else:
            showAge = "лет"
        personInfo = f"Привет, меня зовут {self.name}, мне {self.age} {showAge}. Я вешу {self.weight} кг., а мой рост составляет {self.height} см."
        born = await self.generate_info(personInfo, "о том где родился (район, город)")
        like = await self.generate_info(personInfo, "о моих интересах на примере")
        skill = await self.generate_info(personInfo, "о моем навыке на примере")
        habit = await self.generate_info(personInfo, "о моей вредной или полезной привычке")
        pet = await self.generate_info(personInfo, "о домашнем животном (или нету животных вовсе)")
        number = generate_mobile_number()
        with open("output.txt", "a", encoding="utf-8") as file:
            print(personInfo, file=file)
            print(f"{born}", file=file)
            print(f"{like}", file=file)
            print(f"{skill}", file=file)
            print(f"{habit}", file=file)
            print(f"{pet}", file=file)
            print(f"Номер моего мобильного: {number}", file=file)
            print("", file=file)
            
# Количество людей для генерации. (Случайно)        
quantity = random.randint(100, 1000)

# Генерация мобильного номера
def generate_mobile_number():
    first_digit = random.choice(["9", "8"])
    remaining_digits = "".join(random.choices("0123456789", k=10))
    mobile_number = first_digit + remaining_digits
    return mobile_number

# Процесс генерации людей.
people = []
for _ in range(quantity):
    name = random.choice(russian_names)  
    age = random.randint(18, 70)
    weight = round(random.uniform(50, 120), 2)
    height = random.randint(140, 210)
    person = Person(name, age, weight, height)
    people.append(person)

# Функция поздороваться (асинхронно)
async def say_hello_for_person(person):
    await person.say_hello()

# Каждому сгенерированному человеку нужно будет поздороваться
async def main():
    tasks = [say_hello_for_person(person) for person in people]
    await asyncio.gather(*tasks)

# Запуск
loop = asyncio.get_event_loop()
loop.run_until_complete(main())