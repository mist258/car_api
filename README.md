
# Clone AutoRia API (DRF)

## ADVERTISEMENT

I. AdvertisementCreate: view allows the seller to create a new advert, validating their account type: premium or basic.

IІ. ShowAllUsersAdv: user can view a list of their own adverts 

ІІІ. UpdateUserAdv: user can update their own advert by ID

IV. ShowUserAdvById: any user can view a advert by ID from a seller

V. DestroyUserAdv: а user or staff can delete an advert by ID

VI. ShowAdvertisementList: any user or guest can view the entire list of active adverts

VII. AdvCarAddPhoto: seller can add photos to the listing in a limited quantity (up to 10 images)

VIIІ. AdvCarRemovePhoto: seller can delete photos from a current advert

IX. CurrencyConverter: any user has the ability to convert the current price of an advert in the current currency to another available currency

X. ShowNonActivateAdvertisement: allows staff to view the list of inactive adverts

XI. DeactivateAdvertisement: allows staff to deactivate an advert by ID

XII. ActivateAdvertisement: allows staff to activate an advert by ID


## AUTH 
I. ActivationUser: allows the activation of a user's account

II. RecoveryPasswordRequest: user can send a request to reset their login password

III. RecoveryPassword: resets the password using the token

IV. SocketToken: get socket token for users


## USERS
I. UserCreate: allows the creation of a user account

II. UserBlock: allows staff to block a user by ID

III. UserUnblock: allows staff to unblock a user by ID

IV. UserToManager: allows the superuser (owner) to create a manager

V. GetMe: аny authorized user can obtain information about themselves

VI. ShowAllUsers: staff can obtain a list of all users using filters

VII. MakePremiumAccount: manager can change basic accout to premium


## START PROJECT


```bash
git clone https://github.com/mist258/car_api.git 

poetry install

docker compose build 

docker compose up -d 

docker exec -it car_api-db-1 psql -U postgres -c "CREATE DATABASE car_api;

docker compose run --rm app sh
-./manage.py makemigrations
-./manage.py migrate
```
    











































