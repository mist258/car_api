from django.db import models


class AdvRegionChoices(models.TextChoices):
    VINNYTSIA = 'vinnytsia'
    DNIPRO = 'dnipro'
    DONETSK = 'donetsk'
    ZHYTOMYR = 'zhytomyr'
    ZAPORIZHZHIA = 'zaporizhzhia'
    IVANO_FRANKIVSK = 'ivano-frankivsk'
    KYIV = 'kyiv'
    KROPYVNYTSKYI = 'kropyvnytskyi'
    LUHANSK = 'luhansk'
    LUTSK = 'lutsk'
    LVIV = 'lviv'
    MYKOLAIV = 'mykolaiv'
    ODESA = 'odesa'
    POLTAVA = 'poltava'
    RIVNE = 'rivne'
    SUMY = 'sumy'
    TERNOPIL = 'ternopil'
    UZHHOROD = 'uzhhorod'
    KHARKIV = 'kharkiv'
    KHERSON = 'kherson'
    KHMELNYTSKYI = 'khmelnytskyi'
    CHERKASY = 'cherkasy'
    CHERNIVTSI = 'chernivtsi'
    CHERNIHIV = 'chernihiv'

class AdvCurrencyChoices(models.TextChoices):
    USD = 'USD'
    UAH = 'UAH'
    EUR = 'EUR'

