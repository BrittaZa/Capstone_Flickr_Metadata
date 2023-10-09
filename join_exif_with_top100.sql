/* Join exif data with top100 cameras table */

SELECT * INTO photo_exif_top100 FROM photo_exif AS e
LEFT JOIN (SELECT model AS model_top100, count AS count_top100, TYPE, semiprof FROM camera_top100) AS c
ON e.model = c.model_top100

/* Updating makes column (lowercase, combine names) */

UPDATE photo_exif_top100 SET make = lower(make);

SELECT make, count(*) AS count FROM photo_exif_top100 GROUP BY make ORDER BY count desc;

SELECT make, count(*) AS count FROM photo_exif_top100 WHERE make LIKE '%nikon%' GROUP BY make;
UPDATE photo_exif_top100 SET make = 'nikon' WHERE make LIKE '%nikon%';

SELECT make, count(*) FROM photo_exif_top100 WHERE make LIKE '%canon%' GROUP BY make;
UPDATE photo_exif_top100 SET make = 'canon' WHERE make LIKE '%canon%';

SELECT make, count(*) FROM photo_exif_top100 WHERE make LIKE '%sony%' GROUP BY make;
UPDATE photo_exif_top100 SET make = 'sony' WHERE make LIKE '%sony%';

SELECT make, count(*) FROM photo_exif_top100 WHERE make LIKE '%hasselblad%' GROUP BY make;
UPDATE photo_exif_top100 SET make = 'hasselblad' WHERE make LIKE '%hasselblad%';

SELECT make, count(*) FROM photo_exif_top100 WHERE make LIKE '%leica%' GROUP BY make;
UPDATE photo_exif_top100 SET make = 'leica' WHERE make LIKE '%leica%';

SELECT make, count(*) FROM photo_exif_top100 WHERE make LIKE '%olympus%' GROUP BY make;
UPDATE photo_exif_top100 SET make = 'olympus' WHERE make LIKE '%olympus%';

SELECT make, count(*) FROM photo_exif_top100 WHERE make LIKE '%fuji%' GROUP BY make;
UPDATE photo_exif_top100 SET make = 'fujifilm' WHERE make LIKE '%fuji%';

SELECT make, count(*) FROM photo_exif_top100 WHERE make LIKE '%ricoh%' GROUP BY make;
UPDATE photo_exif_top100 SET make = 'ricoh' WHERE make LIKE '%ricoh%';

SELECT make, count(*) FROM photo_exif_top100 WHERE make LIKE '%apple%' GROUP BY make;
UPDATE photo_exif_top100 SET make = 'apple' WHERE make LIKE '%apple%';

SELECT make, count(*) FROM photo_exif_top100 WHERE make LIKE '%samsung%' GROUP BY make;
UPDATE photo_exif_top100 SET make = 'samsung' WHERE make LIKE '%samsung%';

/* Investigate spikes IN Q4 2021 */
SELECT user_id, count(*) FROM photo_exif_top100 
WHERE date_and_time > '2021-10-01' AND date_and_time < '2022-01-01'
AND make = 'canon'
GROUP BY user_id ORDER BY count DESC;

SELECT user_id, count(*) FROM photo_exif_top100 
WHERE date_and_time > '2021-07-01' AND date_and_time < '2022-10-01'
AND make = 'nikon'
GROUP BY user_id ORDER BY count DESC;
