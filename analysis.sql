select * from homes
where city = 'Avon' and sale_amount < 1000000;

#Home Preferences
SELECT
    preference_type,
    value,
    COUNT(*) as value_count,
    SUM(COUNT(*)) OVER (PARTITION BY preference_type) as total_preference_count
FROM ClientPreferences
GROUP BY preference_type, value
order by total_preference_count DESC;

#Appoinments preferences
SELECT
    hf.feature_name,
    COUNT(a.appointment_id) AS total_appointments
FROM Homes h
LEFT JOIN HomeFeatureAssignments hfa ON h.home_id = hfa.home_id
LEFT JOIN HomeFeatures hf ON hfa.feature_id = hf.feature_id
LEFT JOIN Appointments a ON h.home_id = a.home_id
GROUP BY hf.feature_name
ORDER BY total_appointments DESC;

#Home sold
SELECT
    type,
    COUNT(*) AS total_homes,
    COUNT(CASE WHEN status = 'SOLD' THEN 1 END) AS sold_homes,
    ROUND((COUNT(CASE WHEN status = 'SOLD' THEN 1 END) * 100.0 / COUNT(*)), 2) AS sold_percentage
FROM Homes
GROUP BY type
ORDER BY sold_percentage DESC;

#Home leased
SELECT
    type,
    COUNT(*) AS total_homes,
    COUNT(CASE WHEN status = 'LEASED' THEN 1 END) AS leased_homes,
    ROUND((COUNT(CASE WHEN status = 'LEASED' THEN 1 END) * 100.0 / COUNT(*)), 2) AS leased_percentage
FROM Homes
GROUP BY type
ORDER BY leased_percentage DESC;

#School sold
WITH TotalHomes AS (
    SELECT
        school_id,
        COUNT(*) AS total_homes
    FROM Homes
    GROUP BY school_id
)
SELECT
    h.school_id,
    h.type,
    COUNT(*) AS homes_sold,
    ROUND((COUNT(*) * 100.0 / th.total_homes), 2) AS sold_percentage
FROM Homes h
JOIN TotalHomes th ON h.school_id = th.school_id
WHERE h.status = 'SOLD'
GROUP BY h.school_id, h.type, th.total_homes
ORDER BY homes_sold DESC, sold_percentage DESC, h.school_id, h.type;

#Homes with media room
SELECT
    h.home_id,
    h.address,
    h.city,
    h.state,
    h.date_recorded,
    h.assessed_value,
    h.sale_amount,
    h.sales_ratio,
    h.type,
    h.status
FROM Homes h
JOIN HomeFeatureAssignments hfa ON h.home_id = hfa.home_id
JOIN HomeFeatures hf ON hfa.feature_id = hf.feature_id
WHERE hf.feature_name = 'Media Room';

#sales ratio on different months
SELECT
    EXTRACT(MONTH FROM date_recorded) AS month,
    EXTRACT(YEAR FROM date_recorded) AS year,
    AVG(sales_ratio) AS average_sales_ratio
FROM Homes
WHERE
    type = 'Single Family' AND
    date_recorded BETWEEN '2021-03-01' AND '2021-03-31'
GROUP BY
    EXTRACT(MONTH FROM date_recorded),
    EXTRACT(YEAR FROM date_recorded)
UNION ALL
SELECT
    EXTRACT(MONTH FROM date_recorded) AS month,
    EXTRACT(YEAR FROM date_recorded) AS year,
    AVG(sales_ratio) AS average_sales_ratio
FROM Homes
WHERE
    type = 'Single Family' AND
    date_recorded BETWEEN '2021-06-01' AND '2021-06-30'
GROUP BY
    EXTRACT(MONTH FROM date_recorded),
    EXTRACT(YEAR FROM date_recorded)
ORDER BY year, month;

