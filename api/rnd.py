from faker import Faker
import random

faker = Faker()

def random_bear():
    bear_type_dict = {"POLAR", "BROWN", "BLACK", "GUMMY"}
    bear_type = random.choice(list(bear_type_dict))
    bear_name = faker.first_name()
    bear_age = round(random.uniform(0,99.9),1)  # I suggest the age of bear will be between 0 on 99.9 
    data = {"bear_type":bear_type, "bear_name": bear_name,"bear_age": bear_age} 
    return data
