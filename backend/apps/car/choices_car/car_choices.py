from django.db import models


class CarDrivetrainTypeChoices(models.TextChoices):
    FRONT_WHEEL = "FWD", "Front-Wheel Drive"
    REAR_WHEEL = "RWD", "Rear-Wheel Drive"
    ALL_WHEEL = "AWD", "All-Wheel Drive"
    FOUR_WHEEL = "4WD", "Four-Wheel Drive"


class CarBodyTypeChoices(models.TextChoices):
    HATCHBACK = "Hatchback", "Hatchback"
    SEDAN = "Sedan", "Sedan"
    COUPE = "Coupe", "Coupe"
    WAGON = "Wagon", "Wagon"
    SUV = "SUV", "SUV"
    CONVERTIBLE = "Convertible", "Convertible"
    PICKUP = "Pickup", "Pickup"
    VAN = "Van", "Van"
    MINIVAN = "Minivan", "Minivan"
    CROSSOVER = "Crossover", "Crossover"
    SPORT_CAR = "Sport car", "Sport car"
    LIMOUSINE = "Limousine", "Limousine"
    OTHER = "Other", "Other"


class CarGearTypeChoices(models.TextChoices):
    MANUAL = "Manual", "Manual"
    AUTOMATIC = "Automatic", "Automatic"
    SEMI_AUTOMATIC = "Semi-Automatic", "Semi-Automatic"
    CVT = "CVT", "Continuously Variable Transmission"
    DCT = "DCT", "Dual-Clutch Transmission"
    TIPTRONIC = "Tiptronic", "Tiptronic"
    SPORT_SHIFT = "Sport shift", "Sport shift"
    OTHER = "Other", "Other"


class CarFuelTypeChoices(models.TextChoices):
    PETROL = "Petrol", "Petrol"
    DIESEL = "Diesel", "Diesel"
    ELECTRIC = "Electric", "Electric"
    HYBRID = "Hybrid", "Hybrid"
    PLUG_IN_HYBRID = "Plug-in Hybrid", "Plug-in Hybrid"
    NATURAL_GAS = "Natural Gas", "Natural Gas"
    LIQUEFIED_PETROLEUM_GAS = "LPG", "Liquefied Petroleum Gas"
    BIODIESEL = "Biodiesel", "Biodiesel"
    ETHANOL = "Ethanol", "Ethanol"
    OTHER = "Other", "Other"


class CarBrandChoices(models.TextChoices):
    ACURA = "Acura", "Acura"
    ALFA_ROMEO = "Alfa Romeo", "Alfa Romeo"
    ASTON_MARTIN = "Aston Martin", "Aston Martin"
    AUDI = "Audi", "Audi"
    BENTLEY = "Bentley", "Bentley"
    BMW = "BMW", "BMW"
    BUGATTI = "Bugatti", "Bugatti"
    BUICK = "Buick", "Buick"
    CADILLAC = "Cadillac", "Cadillac"
    CHEVROLET = "Chevrolet", "Chevrolet"
    CHRYSLER = "Chrysler", "Chrysler"
    CITROEN = "Citroën", "Citroën"
    DODGE = "Dodge", "Dodge"
    FERRARI = "Ferrari", "Ferrari"
    FIAT = "Fiat", "Fiat"
    FORD = "Ford", "Ford"
    GENESIS = "Genesis", "Genesis"
    GMC = "GMC", "GMC"
    HONDA = "Honda", "Honda"
    HYUNDAI = "Hyundai", "Hyundai"
    INFINITY = "Infinity", "Infinity"
    JAGUAR = "Jaguar", "Jaguar"
    JEEP = "Jeep", "Jeep"
    KIA = "Kia", "Kia"
    LAMBORGHINI = "Lamborghini", "Lamborghini"
    LAND_ROVER = "Land Rover", "Land Rover"
    LEXUS = "Lexus", "Lexus"
    MASERATI = "Maserati", "Maserati"
    MAZDA = "Mazda", "Mazda"
    MCLAREN = "McLaren", "McLaren"
    MERCEDES_BENZ = "Mercedes-Benz", "Mercedes-Benz"
    MINI = "Mini", "Mini"
    MITSUBISHI = "Mitsubishi", "Mitsubishi"
    NISSAN = "Nissan", "Nissan"
    PAGANI = "Pagani", "Pagani"
    PEUGEOT = "Peugeot", "Peugeot"
    PORSCHE = "Porsche", "Porsche"
    RAM = "RAM", "RAM"
    RENAULT = "Renault", "Renault"
    ROLLS_ROYCE = "Rolls-Royce", "Rolls-Royce"
    SUBARU = "Subaru", "Subaru"
    SUZUKI = "Suzuki", "Suzuki"
    TESLA = "Tesla", "Tesla"
    TOYOTA = "Toyota", "Toyota"
    VOLKSWAGEN = "Volkswagen", "Volkswagen"
    VOLVO = "Volvo", "Volvo"
    SKODA = "Škoda", "Škoda"
    SEAT = "Seat", "Seat"
    SMART = "Smart", "Smart"
    SSANGYONG = "SsangYong", "SsangYong"
