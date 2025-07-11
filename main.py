import json
import sqlite3
from sqlite3 import Error
from typing import Optional
from fastapi import FastAPI, Body, HTTPException

app = FastAPI()


class DataModel:
    def __init__(self, ):
        self.id = None
        self.name = None
        self.brand = None
        self.category = None
        self.price = None
        self.discount = None
        self.finalPrice = None
        self.currency = None
        self.stock = None
        self.rating = None
        self.specs = None
        self.colors = None
        self.warranty = None
        self.isAvailable = None

    def fromjson(self, map: dict):
        self.id = map['id']
        self.name = map['name']
        self.brand = map['brand']
        self.category = map['category']
        self.price = map['price']
        self.discount = map['discount']
        self.finalPrice = map['finalPrice']
        self.currency = map['currency']
        self.stock = map['stock']
        self.rating = map['rating']
        self.colors = map['colors']
        self.warranty = map['warranty']
        self.isAvailable = map['isAvailable']

allData = {
    "products": [
        {
            "id": 1,
            "name": "گوشی هوشمند شیائومی ردمی نوت 12 پرو",
            "brand": "Xiaomi",
            "category": "موبایل",
            "price": 15_500_000,
            "discount": 12,
            "finalPrice": 13_640_000,
            "currency": "تومان",
            "stock": 23,
            "rating": 4.5,
            "colors": ["آبی", "مشکی", "طلایی"],
            "warranty": "18 ماهه",
            "isAvailable": True
        },
        {
            "id": 2,
            "name": "لپ تاپ ایسوس ویوو بوک 15",
            "brand": "Asus",
            "category": "لپ تاپ",
            "price": 32_000_000,
            "discount": 8,
            "finalPrice": 29_440_000,
            "currency": "تومان",
            "stock": 7,
            "rating": 4.3,
            "colors": ["نقره‌ای"],
            "warranty": "24 ماهه",
            "isAvailable": True
        },
        {
            "id": 3,
            "name": "هدفون بی‌سیم اپل ایرپادز پرو 2",
            "brand": "Apple",
            "category": "هدفون",
            "price": 11_200_000,
            "discount": 5,
            "finalPrice": 10_640_000,
            "currency": "تومان",
            "stock": 34,
            "rating": 4.8,
            "colors": ["سفید"],
            "warranty": "12 ماهه",
            "isAvailable": True
        },
        {
            "id": 4,
            "name": "تلویزیون هوشمند سامسونگ QLED 55 اینچ",
            "brand": "Samsung",
            "category": "تلویزیون",
            "price": 38_000_000,
            "discount": 15,
            "finalPrice": 32_300_000,
            "currency": "تومان",
            "stock": 4,
            "rating": 4.6,
            "colors": ["مشکی"],
            "warranty": "24 ماهه",
            "isAvailable": True
        },
        {
            "id": 5,
            "name": "اسمارت واچ هواوی جی تی 3 پرو",
            "brand": "Huawei",
            "category": "ساعت هوشمند",
            "price": 8_500_000,
            "discount": 10,
            "finalPrice": 7_650_000,
            "currency": "تومان",
            "stock": 18,
            "rating": 4.4,
            "colors": ["مشکی", "نقره‌ای"],
            "warranty": "12 ماهه",
            "isAvailable": True
        },
        {
            "id": 6,
            "name": "تبلت سامسونگ گلکسی تب S8",
            "brand": "Samsung",
            "category": "تبلت",
            "price": 28_000_000,
            "discount": 7,
            "finalPrice": 26_040_000,
            "currency": "تومان",
            "stock": 9,
            "rating": 4.7,
            "colors": ["نقره‌ای", "صورتی"],
            "warranty": "18 ماهه",
            "isAvailable": True
        },
        {
            "id": 7,
            "name": "کیبورد مکانیکی رزر بلک ویدو",
            "brand": "Razer",
            "category": "لوازم جانبی",
            "price": 6_200_000,
            "discount": 0,
            "finalPrice": 6_200_000,
            "currency": "تومان",
            "stock": 42,
            "rating": 4.9,
            "colors": ["مشکی"],
            "warranty": "24 ماهه",
            "isAvailable": True
        },
        {
            "id": 8,
            "name": "دوربین کانن EOS R6",
            "brand": "Canon",
            "category": "دوربین",
            "price": 85_000_000,
            "discount": 12,
            "finalPrice": 74_800_000,
            "currency": "تومان",
            "stock": 3,
            "rating": 4.8,
            "colors": ["مشکی"],
            "warranty": "18 ماهه",
            "isAvailable": True
        },
        {
            "id": 9,
            "name": "اسپیکر بلوتوثی جی بی ال پلیت 5",
            "brand": "JBL",
            "category": "اسپیکر",
            "price": 4_800_000,
            "discount": 20,
            "finalPrice": 3_840_000,
            "currency": "تومان",
            "stock": 27,
            "rating": 4.6,
            "colors": ["مشکی", "آبی"],
            "warranty": "12 ماهه",
            "isAvailable": True
        },
        {
            "id": 10,
            "name": "ماشین اصلاح فیلیپس سری 7000",
            "brand": "Philips",
            "category": "لوازم شخصی",
            "price": 3_500_000,
            "discount": 15,
            "finalPrice": 2_975_000,
            "currency": "تومان",
            "stock": 56,
            "rating": 4.5,
            "colors": ["نقره‌ای"],
            "warranty": "24 ماهه",
            "isAvailable": True
        }
    ],
    "totalProducts": 10,
    "lastUpdate": "2024-03-20",
    "description": "لیست کامل محصولات الکترونیکی با جزئیات فنی و قیمت‌گذاری"
}


@app.get('/list_all_products')
async def add_all_products():
    db = DatabaseProducts()
    _database= await db.set_BigData_add_database(allData)
    if _database:
        raise HTTPException(status_code=200,detail='عملیات اضافه کردن کامل لیست محصولات به صورت فیک با موفقیت انجام شد')
    else:
        raise HTTPException(status_code=500, detail='خطای سرور')
    
    

@app.get('/list_store_user{brand}')
async def show_list_store(brand: str):
    data = list(filter(lambda x: x['brand'] == brand, allData['products']))
    print(data)
    if len(data) >= 1:
        return data
    else:
        raise HTTPException(status_code=400, detail='brand not in data')


@app.get('/list_show_all_skip')
async def list_show_all_skip(skip: int = 0, limit: int = 3):
    filtered = allData['products'].copy()
    datafilter= filtered[skip:skip+limit]
    return {
        'skip': skip,
        'limit': limit,
        'alldata': len(allData),
        'data': datafilter
    }


@app.post('/add_to_list')
async def add_list_and_database(add_data=Body(example={
            "id": 122,
            "name": "دوربین کانن EOS R6",
            "brand": "Canon",
            "category": "دوربین",
            "price": 85_000_000,
            "discount": 12,
            "finalPrice": 74_800_000,
            "currency": "تومان",
            "stock": 3,
            "rating": 4.8,
            "colors": ["مشکی"],
            "warranty": "18 ماهه",
            "isAvailable": True
        })):

    try:
        if add_data is not None:
            if not isinstance(add_data['id'],int) or add_data['id']<=0:
                raise HTTPException(status_code=400,detail='{id} به درستی وارد نشده است')

        db= DatabaseProducts()
        _database= await db.insert_data(data=add_data)
        db.close()
        if _database:
            return HTTPException(status_code=200,detail='عملیات با موفقیت انجام شد')
        else:
            raise HTTPException(status_code=400, detail="Failed to add product")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail=f'خطای مورد نظر این است {e} ')




@app.get('/get_all_products')
async def get_all_products():
    try:
        
        db = DatabaseProducts()
        _database = await db.get_query()
        db.close()
        if _database is not None:
            return _database
        else:
            raise HTTPException(status_code=400, detail="Failed to get products")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail=f'Error: {e}')

class DatabaseProducts:


    def __init__(self):
        self.con = sqlite3.connect('databaseProducts.db')
        self.database = self.con.cursor()
        self._create_database()
        
    def _create_database(self, ):
        self.database.execute('''
            CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY,
                name TEXT,
                brand TEXT,
                category TEXT,
                price REAL,
                discount INTEGER,
                finalPrice REAL,
                currency TEXT,
                stock INTEGER,
                rating REAL,
                colors TEXT,
                warranty TEXT,
                isAvailable INTEGER
            )
            ''')

        self.con.commit()
        
    async def insert_data(self,data: dict):
        dataProduct: DataModel = DataModel()
        dataProduct.fromjson(data)
        try:
            colors= json.dumps(dataProduct.colors)
            isAvailable= 1 if dataProduct.isAvailable else 0
            
            self.database.execute('''
                       INSERT INTO products(id, name, brand, category, price, discount, finalPrice, currency, 
                        stock, rating, colors, warranty, isAvailable) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                       ''', (
            dataProduct.id, dataProduct.name, dataProduct.brand, dataProduct.category, dataProduct.price,
            dataProduct.discount, dataProduct.finalPrice, dataProduct.currency, dataProduct.stock,
            dataProduct.rating, colors, dataProduct.warranty,
            isAvailable
            ))
            self.con.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False


    async def get_query(self):
        try:
            
            self.database.execute('SELECT * FROM products WHERE isAvailable = 1 ORDER BY id ASC')
            return self.database.fetchmany()
        except sqlite3.Error as e:
            print(e)
            return []


    async def set_BigData_add_database(self,data):
        try:
            self.database.execute('DELETE FROM products')
            self.con.commit()
            for i in data['products']:
               await self.insert_data(i)
            return True
        except Exception as e:
            print(e)
            return False

    def close(self):
        self.con.close()
        
        
