queries = {

# ==================================================
# 🏺 artifact_metadata Table
# ==================================================

"1.List all artifacts from the 11th century belonging to Byzantine culture.":
"""
SELECT *
FROM artifact_metadata
WHERE culture = 'Byzantine'
  AND dated LIKE '%11%';
""",

"2.What are the unique cultures represented in the artifacts?":
"""
SELECT DISTINCT culture
FROM artifact_metadata
WHERE culture IS NOT NULL;
""",

"3.List all artifacts from the Archaic Period.":
"""
SELECT *
FROM artifact_metadata
WHERE period = 'Archaic Period';
""",

"4.List artifact titles ordered by accession year in descending order.":
"""
SELECT title
FROM artifact_metadata
ORDER BY title DESC;
""",

"5.How many artifacts are there per department?":
"""
SELECT department, COUNT(*) AS total_artifacts
FROM artifact_metadata
GROUP BY department;
""",

# ==================================================
# 🖼️ artifact_media Table
# ==================================================

"6.Which artifacts have more than 1 image?":
"""
SELECT objectid, imagecount
FROM artifact_media
WHERE imagecount > 1;
""",

"7.What is the average rank of all artifacts?":
"""
SELECT AVG(rank) AS average_rank
FROM artifact_media;
""",

"8.Which artifacts have a higher colorcount than mediacount?":
"""
SELECT objectid, colorcount, mediacount
FROM artifact_media
WHERE colorcount > mediacount;
""",

"9.List all artifacts created between 1500 and 1600.":
"""
SELECT objectid, datebegin, dateend
FROM artifact_media
WHERE datebegin >= 1500
  AND dateend <= 1600;
""",

"10.How many artifacts have no media files?":
"""
SELECT objectid
FROM artifact_media
WHERE mediacount = 0;
""",

# ==================================================
# 🎨 artifact_colors Table
# ==================================================

"11.What are all the distinct hues used in the dataset?":
"""
SELECT DISTINCT hue
FROM artifact_colors
WHERE hue IS NOT NULL;
""",

"12.What are the top 5 most used colors by frequency?":
"""
SELECT color, COUNT(*) AS frequency
FROM artifact_colors
GROUP BY color
ORDER BY frequency DESC
LIMIT 5;
""",

"13.What is the average coverage percentage for each hue?":
"""
SELECT hue, AVG(percent) AS avg_coverage
FROM artifact_colors
GROUP BY hue;
""",

"14.List all colors used for a given artifact ID.":
"""
SELECT *
FROM artifact_colors
WHERE objectid = 1;
""",

"15.What is the total number of color entries in the dataset?":
"""
SELECT COUNT(*) AS total_colors
FROM artifact_colors;
""",

# ==================================================
# 🔗 Join-Based Queries
# ==================================================

"16.List artifact titles and hues for all artifacts belonging to the Byzantine culture.":
"""
SELECT m.title, c.hue
FROM artifact_metadata m
JOIN artifact_colors c
ON m.id = c.objectid
WHERE m.culture = 'Byzantine';
""",

"17.List each artifact title with its associated hues.":
"""
SELECT m.title, c.hue
FROM artifact_metadata m
JOIN artifact_colors c
ON m.id = c.objectid;
""",

"18.Get artifact titles, cultures, and media ranks where the period is not null.":
"""
SELECT m.title, m.culture, md.media_rank
FROM artifact_metadata m
JOIN artifact_media md
ON m.id = md.objectid
WHERE m.period IS NOT NULL;
""",

"19.Find artifact titles ranked in the top 10 that include the color hue 'Grey'.":
"""
SELECT DISTINCT m.title, md.media_rank
FROM artifact_metadata m
JOIN artifact_media md ON m.id = md.objectid
JOIN artifact_colors c ON m.id = c.objectid
WHERE c.hue = 'Grey'
ORDER BY md.media_rank DESC
LIMIT 10;
""",

"20.How many artifacts exist per classification, and what is the average media count for each?":
"""
SELECT m.department AS classification,
       COUNT(*) AS total_artifacts,
       AVG(md.mediacount) AS avg_media
FROM artifact_metadata m
JOIN artifact_media md
ON m.id = md.objectid
GROUP BY m.department;
""",

# ==================================================
# ⭐ EXTRA QUERIES (Learner Framed)
# ==================================================

"21.What is the oldest artifact in the collection?":
"""
SELECT m.title, md.datebegin
FROM artifact_media md
JOIN artifact_metadata m
ON md.objectid = m.id
ORDER BY md.datebegin ASC
LIMIT 1;
""",

"22.Which artifact has the highest media rank?":
"""
SELECT m.title, md.media_rank
FROM artifact_media md
JOIN artifact_metadata m
ON md.objectid = m.id
ORDER BY md.media_rank DESC
LIMIT 1;
""",

"23.Which artifacts do not have culture information?":
"""
SELECT *
FROM artifact_metadata
WHERE culture IS NULL;
""",

"24.What is the average number of images per department?":
"""
SELECT m.department, AVG(md.imagecount) AS avg_images
FROM artifact_metadata m
JOIN artifact_media md
ON m.id = md.objectid
GROUP BY m.department;
""",

"25.Which is the most colorful artifact based on total color coverage?":
"""
SELECT objectid, SUM(percent) AS total_color_coverage
FROM artifact_colors
GROUP BY objectid
ORDER BY total_color_coverage DESC
LIMIT 1;
"""
}
