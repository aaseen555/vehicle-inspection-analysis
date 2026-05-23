import pandas as pd
import numpy as np

np.random.seed(42)
n = 10000

brands = {
    'Maruti': 0.30, 'Hyundai': 0.18, 'Honda': 0.12,
    'Tata': 0.10, 'Mahindra': 0.09, 'Toyota': 0.07,
    'Ford': 0.05, 'Volkswagen': 0.04, 'Renault': 0.03, 'Kia': 0.02
}
brand_base_price = {
    'Maruti': 350000, 'Hyundai': 480000, 'Honda': 560000,
    'Tata': 420000, 'Mahindra': 510000, 'Toyota': 650000,
    'Ford': 430000, 'Volkswagen': 520000, 'Renault': 390000, 'Kia': 580000
}
fuel_types = ['Petrol', 'Diesel', 'CNG', 'Electric']
fuel_weights = [0.52, 0.33, 0.12, 0.03]
transmission = ['Manual', 'Automatic']
trans_weights = [0.68, 0.32]
inspection_grades = ['A', 'B', 'C', 'D']
grade_weights = [0.25, 0.40, 0.25, 0.10]
owners = ['1st', '2nd', '3rd']
owner_weights = [0.55, 0.35, 0.10]
cities = ['Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata', 'Ahmedabad']

brand_list = np.random.choice(list(brands.keys()), n, p=list(brands.values()))
year = np.random.randint(2010, 2024, n)
age = 2025 - year
fuel = np.random.choice(fuel_types, n, p=fuel_weights)
trans = np.random.choice(transmission, n, p=trans_weights)
grade = np.random.choice(inspection_grades, n, p=grade_weights)
owner = np.random.choice(owners, n, p=owner_weights)
city = np.random.choice(cities, n)
km_driven = (age * np.random.randint(8000, 18000, n)).clip(5000, 250000)

def calc_price(brand, age, km, fuel, trans, grade, owner):
    base = brand_base_price[brand]
    age_factor = max(0.3, 1 - (age * 0.07))
    km_factor = max(0.5, 1 - (km / 500000))
    fuel_factor = 1.22 if fuel == 'Diesel' else (1.05 if fuel == 'Electric' else 1.0)
    trans_factor = 1.32 if trans == 'Automatic' else 1.0
    grade_factor = {'A': 1.15, 'B': 1.0, 'C': 0.85, 'D': 0.70}[grade]
    owner_factor = {'1st': 1.0, '2nd': 0.88, '3rd': 0.78}[owner]
    noise = np.random.uniform(0.92, 1.08)
    return int(base * age_factor * km_factor * fuel_factor * trans_factor * grade_factor * owner_factor * noise)

prices = [calc_price(brand_list[i], age[i], km_driven[i], fuel[i], trans[i], grade[i], owner[i]) for i in range(n)]

df = pd.DataFrame({
    'brand': brand_list,
    'year': year,
    'age': age,
    'km_driven': km_driven,
    'fuel_type': fuel,
    'transmission': trans,
    'inspection_grade': grade,
    'owner_type': owner,
    'city': city,
    'selling_price': prices,
    'km_per_year': (km_driven / age).astype(int)
})

df.to_csv('car_inspection_data.csv', index=False)
print(f"Dataset generated: {len(df)} records")
print(df.head())
