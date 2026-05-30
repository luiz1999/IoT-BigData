-- Distribuição de Leituras: Interno vs Externo

CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT 
 "room_id/id" AS device_id,
 ROUND(AVG(temp)::numeric, 2) AS avg_temp,
 COUNT(*) AS total_leituras
FROM temperature_readings
GROUP BY "room_id/id"
ORDER BY avg_temp DESC;

-- Leituras por Hora do Dia

CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT 
 EXTRACT(HOUR FROM TO_TIMESTAMP(noted_date, 'DD-MM-YYYY 
HH24:MI'))::int AS hora,
 COUNT(*) AS total_leituras
FROM temperature_readings
GROUP BY hora
ORDER BY hora;

-- Temperaturas Máximas e Mínimas por Dia

CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT 
 DATE(TO_TIMESTAMP(noted_date, 'DD-MM-YYYY HH24:MI')) AS 
data,
 ROUND(MAX(temp)::numeric, 2) AS temp_max,
 ROUND(MIN(temp)::numeric, 2) AS temp_min,
 ROUND(AVG(temp)::numeric, 2) AS temp_media
FROM temperature_readings
GROUP BY data
ORDER BY data;




