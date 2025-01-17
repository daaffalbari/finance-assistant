import sqlite3
from datetime import datetime, timedelta
import random
import pandas as pd

def initialize_db():
    conn = sqlite3.connect("data/finance.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budget_categories (
        id INTEGER PRIMARY KEY,
        category TEXT,
        rules TEXT,
        budget REAL
    )
    """)
    conn.commit()
    conn.close()

    

def insert_budget_categories():
    categories = [
        ("Bills", "cable tv, credit card, Electricity, Gas, Insurance, Internet, Landline, Maintencance Fee, Mobile & data, rent, Subcription, Water", 1000000),
        ("Education", "tuition, books, courses", 500000),
        ("Entertainment", "movies, concerts, subscriptions, vacation, streaming services, Hangout, Games, Hobby", 300000),
        ("Foods & Drinks", "restaurants, cafes, Take outs", 1500000),
        ("Healthcare", "Drugs/Medicine, Gym/Fitness, Medical fee, Personal care, Sports", 800000),
        ("Shopping", "Fasion, electronics, accessories, Groceries, Gadget", 700000),
        ("Social Events", "weddings, charity & donations, funeral, gifts", 400000),
        ("Topup", "Brizzi BRI, Dana, Flazz BCA, GoPay, LinkAja, Mandiri E-Money, OVO, ShopeePay, TapCash", 200000),
        ("Transportation", "Gasoline, public transport, tolls, Parking fee, Travel fares, Taxi/Ojol, Vehicle maintenance", 500000),
        ("Others", "miscellaneous, undefined expenses", 300000)
    ]

    conn = sqlite3.connect("data/finance.db")
    cursor = conn.cursor()
    cursor.executemany("""
    INSERT INTO budget_categories (category, rules, budget) VALUES (?, ?, ?)
    """, categories)
    conn.commit()
    conn.close()


def generate_bank_transactions(num_transactions=30):  
    # Definisikan kategori dan nominal  
    categories = [  
        ("Bills", "cable tv, credit card, Electricity, Gas, Insurance, Internet, Landline, Maintenance Fee, Mobile & data, rent, Subscription, Water", 1000000),  
        ("Education", "tuition, books, courses", 500000),  
        ("Entertainment", "movies, concerts, subscriptions, vacation, streaming services, Hangout, Games, Hobby", 300000),  
        ("Foods & Drinks", "restaurants, cafes, Take outs", 1500000),  
        ("Healthcare", "Drugs/Medicine, Gym/Fitness, Medical fee, Personal care, Sports", 800000),  
        ("Shopping", "Fashion, electronics, accessories, Groceries, Gadget", 700000),  
        ("Social Events", "weddings, charity & donations, funeral, gifts", 400000),  
        ("Topup", "Brizzi BRI, Dana, Flazz BCA, GoPay, LinkAja, Mandiri E-Money, OVO, ShopeePay, TapCash", 200000),  
        ("Transportation", "Gasoline, public transport, tolls, Parking fee, Travel fares, Taxi/Ojol, Vehicle maintenance", 500000),  
        ("Others", "miscellaneous, undefined expenses", 300000)  
    ]  
  
    # Buat list untuk menyimpan data transaksi  
    data = []  
  
    # Generate data transaksi  
    for i in range(num_transactions):  
        # Pilih kategori secara acak  
        category = random.choice(categories)  
        # Tentukan tanggal transaksi  
        date = datetime.now() - timedelta(days=random.randint(0, 30))  # 30 hari terakhir  
        # Tambahkan data transaksi ke list  
        data.append({  
            "Tanggal": date.strftime("%Y-%m-%d"),  
            "Nominal": category[2],  
            "Kategori": category[0],  
            "Keterangan": f"{category[1].split(',')[0]} - {i+1}"  # Keterangan berdasarkan kategori  
        })  
 
    df_transaksi = pd.DataFrame(data)  
      
    return df_transaksi  
  
df_transaksi = generate_bank_transactions(30)  



initialize_db()
insert_budget_categories()