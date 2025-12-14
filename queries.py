queries = {

# ---------- artifact_metadata ----------
"1. Artifacts from 11th century & Byzantine culture":
"""
SELECT * FROM artifact_metadata
WHERE century = '11th century' AND culture = 'Byzantine';
""",

"2. Unique cultures":
"""
SELECT DISTINCT culture FROM artifact_metadata
WHERE culture IS NOT NULL;
""",

"3. Artifacts from Archaic Period":
"""
SELECT * FROM artifact_metadata
WHERE period = 'Archaic Period';
""",

"4. Titles ordered by accession year (desc)":
"""
SELECT title, accessionyear
FROM artifact_metadata
ORDER BY accessionyear DESC;
""",

"5. Artifact count per department":
"""
SELECT department, COUNT(*) AS total
FROM artifact_metadata
GROUP BY department;
""",

# ---------- artifact_media ----------
"6. Artifacts with more than 1 image":
"""
SELECT objectid, imagecount
FROM artifact_media
WHERE imagecount > 1;
""",

"7. Average media rank":
"""
SELECT AVG(media_rank) AS avg_rank
FROM artifact_media;
""",

"8. Higher colorcount than mediacount":
"""
SELECT objectid, colorcount, mediacount
FROM artifact_media
WHERE colorcount > mediacount;
""",

"9. Artifacts created between 1500 & 1600":
"""
SELECT objectid, datebegin, dateend
FROM artifact_media
WHERE datebegin >= 1500 AND dateend <= 1600;
""",

"10. Artifacts with no media files":
"""
SELECT objectid
FROM artifact_media
WHERE mediacount = 0;
""",

# ---------- artifact_colors ----------
"11. Distinct hues":
"""
SELECT DISTINCT hue FROM artifact_colors
WHERE hue IS NOT NULL;
""",

"12. Top 5 most used colors":
"""
SELECT color, COUNT(*) AS frequency
FROM artifact_colors
GROUP BY color
ORDER BY frequency DESC
LIMIT 5;
""",

"13. Avg coverage % per hue":
"""
SELECT hue, AVG(percent) AS avg_percent
FROM artifact_colors
GROUP BY hue;
""",

"14. Colors for a given artifact ID":
"""
SELECT * FROM artifact_colors
WHERE objectid = 1;
""",

"15. Total color entries":
"""
SELECT COUNT(*) AS total_colors
FROM artifact_colors;
""",

# ---------- JOIN QUERIES ----------
"16. Titles & hues (Byzantine culture)":
"""
SELECT m.title, c.hue
FROM artifact_metadata m
JOIN artifact_colors c ON m.id = c.objectid
WHERE m.culture = 'Byzantine';
""",

"17. Artifact titles with hues":
"""
SELECT m.title, c.hue
FROM artifact_metadata m
JOIN artifact_colors c ON m.id = c.objectid;
""",

"18. Titles, cultures & media rank (period not null)":
"""
SELECT m.title, m.culture, md.media_rank
FROM artifact_metadata m
JOIN artifact_media md ON m.id = md.objectid
WHERE m.period IS NOT NULL;
""",

"19. Top 10 ranked artifacts with Grey color":
"""
SELECT DISTINCT m.title, md.media_rank
FROM artifact_metadata m
JOIN artifact_media md ON m.id = md.objectid
JOIN artifact_colors c ON m.id = c.objectid
WHERE c.hue = 'Grey'
ORDER BY md.media_rank DESC
LIMIT 10;
""",

"20. Artifacts per classification & avg media count":
"""
SELECT m.classification, COUNT(*) AS total_artifacts,
AVG(md.mediacount) AS avg_media
FROM artifact_metadata m
JOIN artifact_media md ON m.id = md.objectid
GROUP BY m.classification;
""",

# ---------- EXTRA (FOR FULL MARKS) ----------
"21. Oldest artifact":
"""
SELECT title, datebegin
FROM artifact_media md
JOIN artifact_metadata m ON md.objectid = m.id
ORDER BY datebegin ASC
LIMIT 1;
""",

"22. Latest acquired artifact":
"""
SELECT title, accessionyear
FROM artifact_metadata
ORDER BY accessionyear DESC
LIMIT 1;
""",

"23. Artifacts without culture":
"""
SELECT * FROM artifact_metadata
WHERE culture IS NULL;
""",

"24. Avg images per classification":
"""
SELECT m.classification, AVG(md.imagecount)
FROM artifact_metadata m
JOIN artifact_media md ON m.id = md.objectid
GROUP BY m.classification;
""",

"25. Most colorful artifact":
"""
SELECT objectid, SUM(percent) AS total_color
FROM artifact_colors
GROUP BY objectid
ORDER BY total_color DESC
LIMIT 1;
"""
}
