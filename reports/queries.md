Query 1: Monthly data usage and active subscribers

SELECT
    month,
    COUNT(DISTINCT customer_id) AS active_subs,
    ROUND(SUM(total_mb) / 1024.0 / 1024, 1) AS total_tb
FROM v_usage_month
GROUP BY month
ORDER BY month;

__________________________________________________________________________________________________________________________________________________

Query 2: Data usage per day by experiment group

SELECT
    strftime('%Y-%m', u.usage_date) AS month,
    c.ab_group,
    COUNT(*) AS usage_days,
    ROUND(AVG(u.data_mb), 2) AS avg_mb_per_day
FROM usage_daily u
JOIN customer_features c
    ON u.customer_id = c.customer_id
GROUP BY month, c.ab_group
ORDER BY month, c.ab_group;

__________________________________________________________________________________________________________________________________________________

Query 3: Data allowance usage by plan

SELECT
    plan_name,
    monthly_gb AS allowance_gb,
    ROUND(AVG(total_data_mb / 1024.0 / 6), 2)
        AS used_gb,
    ROUND(
        100.0 * AVG(
            (total_data_mb / 1024.0 / 6) / monthly_gb
        ), 1
    ) AS allowance_used_pct,
    COUNT(*) AS subscribers
FROM customer_features
WHERE usage_days > 0
GROUP BY plan_name, monthly_gb
ORDER BY monthly_gb;

__________________________________________________________________________________________________________________________________________________

Query 4: Three selected-month metric cards

SELECT
    COUNT(DISTINCT customer_id) AS active_subs,
    ROUND(SUM(total_mb) / 1024.0 / 1024, 2) AS total_tb,
    ROUND(
        SUM(total_mb) / NULLIF(SUM(usage_days), 0),
        2
    ) AS mb_per_usage_day
FROM v_usage_month
WHERE month = :selected_month;

__________________________________________________________________________________________________________________________________________________

Query 5: Daily network data carried

SELECT
    usage_date,
    COUNT(*) AS usage_day_count,
    ROUND(SUM(data_mb) / 1024.0 / 1024, 3) AS daily_tb
FROM usage_daily
WHERE strftime('%Y-%m', usage_date) = :selected_month
GROUP BY usage_date
ORDER BY usage_date;

__________________________________________________________________________________________________________________________________________________

Query 6: Group A versus Group B

SELECT
    c.ab_group,
    COUNT(*) AS usage_days,
    COUNT(DISTINCT u.customer_id) AS subscribers,
    ROUND(AVG(u.data_mb), 2) AS avg_mb_per_day
FROM usage_daily u
JOIN customer_features c
    ON u.customer_id = c.customer_id
WHERE strftime('%Y-%m', u.usage_date) = :selected_month
GROUP BY c.ab_group
ORDER BY c.ab_group;

__________________________________________________________________________________________________________________________________________________

Query 7: Device-type data usage

SELECT
    c.device_type,
    COUNT(*) AS usage_days,
    COUNT(DISTINCT u.customer_id) AS subscribers,
    ROUND(AVG(u.data_mb), 2) AS avg_mb_per_day
FROM usage_daily u
JOIN customer_features c
    ON u.customer_id = c.customer_id
WHERE strftime('%Y-%m', u.usage_date) = :selected_month
GROUP BY c.device_type
ORDER BY avg_mb_per_day DESC;

__________________________________________________________________________________________________________________________________________________

Query 8: Daily usage-day counts

SELECT
    usage_date,
    COUNT(*) AS usage_days,
    ROUND(SUM(data_mb) / 1024.0 / 1024, 3) AS daily_tb
FROM usage_daily
WHERE strftime('%Y-%m', usage_date) = :selected_month
GROUP BY usage_date
ORDER BY usage_date;
