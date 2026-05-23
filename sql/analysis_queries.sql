-- ================================================================
-- Vehicle Inspection Quality & Pricing Analysis
-- Author: Mohd Aaseen
-- Tool: SQL (Compatible with MySQL / PostgreSQL / SQLite)
-- ================================================================

-- ── TABLE SETUP ─────────────────────────────────────────────────
CREATE TABLE car_listings (
    id              INTEGER PRIMARY KEY,
    brand           VARCHAR(50),
    year            INTEGER,
    age             INTEGER,
    km_driven       INTEGER,
    fuel_type       VARCHAR(20),
    transmission    VARCHAR(20),
    inspection_grade VARCHAR(5),
    owner_type      VARCHAR(10),
    city            VARCHAR(50),
    selling_price   INTEGER,
    km_per_year     INTEGER
);

-- ── 1. Average Resale Price by Brand ────────────────────────────
SELECT 
    brand,
    COUNT(*)                          AS total_listings,
    ROUND(AVG(selling_price), 0)      AS avg_price,
    ROUND(MIN(selling_price), 0)      AS min_price,
    ROUND(MAX(selling_price), 0)      AS max_price
FROM car_listings
GROUP BY brand
ORDER BY avg_price DESC;

-- ── 2. Inspection Grade Impact on Pricing ───────────────────────
SELECT 
    inspection_grade,
    COUNT(*)                          AS total_cars,
    ROUND(AVG(selling_price), 0)      AS avg_price,
    ROUND(AVG(km_driven), 0)          AS avg_km_driven,
    ROUND(AVG(age), 1)                AS avg_age
FROM car_listings
GROUP BY inspection_grade
ORDER BY inspection_grade;

-- ── 3. Price Premium: Diesel vs Petrol ──────────────────────────
SELECT 
    fuel_type,
    COUNT(*)                          AS listings,
    ROUND(AVG(selling_price), 0)      AS avg_price
FROM car_listings
GROUP BY fuel_type
ORDER BY avg_price DESC;

-- ── 4. Transmission Price Premium ───────────────────────────────
SELECT 
    transmission,
    COUNT(*)                          AS total_cars,
    ROUND(AVG(selling_price), 0)      AS avg_price
FROM car_listings
GROUP BY transmission
ORDER BY avg_price DESC;

-- ── 5. Price Depreciation by Age ────────────────────────────────
SELECT 
    age,
    COUNT(*)                          AS listings,
    ROUND(AVG(selling_price), 0)      AS avg_price
FROM car_listings
GROUP BY age
ORDER BY age ASC;

-- ── 6. Top Cities by Avg Resale Price ───────────────────────────
SELECT 
    city,
    COUNT(*)                          AS listings,
    ROUND(AVG(selling_price), 0)      AS avg_price
FROM car_listings
GROUP BY city
ORDER BY avg_price DESC;

-- ── 7. Brand × Inspection Grade Price Matrix ────────────────────
SELECT 
    brand,
    ROUND(AVG(CASE WHEN inspection_grade = 'A' THEN selling_price END), 0) AS grade_A,
    ROUND(AVG(CASE WHEN inspection_grade = 'B' THEN selling_price END), 0) AS grade_B,
    ROUND(AVG(CASE WHEN inspection_grade = 'C' THEN selling_price END), 0) AS grade_C,
    ROUND(AVG(CASE WHEN inspection_grade = 'D' THEN selling_price END), 0) AS grade_D
FROM car_listings
GROUP BY brand
ORDER BY grade_A DESC;

-- ── 8. KM Bucket Analysis ───────────────────────────────────────
SELECT 
    CASE 
        WHEN km_driven BETWEEN 0     AND 30000  THEN '0-30K km'
        WHEN km_driven BETWEEN 30001 AND 60000  THEN '30-60K km'
        WHEN km_driven BETWEEN 60001 AND 100000 THEN '60-100K km'
        WHEN km_driven BETWEEN 100001 AND 150000 THEN '100-150K km'
        ELSE '150K+ km'
    END                               AS km_range,
    COUNT(*)                          AS listings,
    ROUND(AVG(selling_price), 0)      AS avg_price
FROM car_listings
GROUP BY km_range
ORDER BY avg_price DESC;

-- ── 9. Owner Type Impact ────────────────────────────────────────
SELECT 
    owner_type,
    COUNT(*)                          AS listings,
    ROUND(AVG(selling_price), 0)      AS avg_price,
    ROUND(AVG(km_driven), 0)          AS avg_km
FROM car_listings
GROUP BY owner_type
ORDER BY avg_price DESC;

-- ── 10. High Value Listings ─────────────────────────────────────
SELECT 
    brand, year, km_driven, fuel_type, 
    transmission, inspection_grade, selling_price
FROM car_listings
WHERE inspection_grade = 'A'
  AND km_driven < 50000
  AND transmission = 'Automatic'
ORDER BY selling_price DESC
LIMIT 20;
