-- ============================================================================
-- OLAP WORKLOAD - IMDb Movie Database
-- ============================================================================
-- Description: Analytical queries for performance testing and workload analysis
-- Database: IMDb (Internet Movie Database)
-- Query Count: 9
-- Focus: Movies from 2000-2020 production years
-- Workload Type: Read-heavy analytical operations
-- ============================================================================

-- Query 1: Movies with Large Cast
-- Description: Find movies produced between 2000-2020 with more than 10 cast members
-- Complexity: Medium | Operations: JOIN, GROUP BY, HAVING, ORDER BY, COUNT
SELECT t.title, COUNT(c.movie_id) AS num_cast_members 
FROM title AS t 
JOIN cast_info AS c ON t.id = c.movie_id 
WHERE t.production_year BETWEEN 2000 AND 2020 
GROUP BY t.title 
HAVING COUNT(c.movie_id) > 10 
ORDER BY num_cast_members DESC;

-- Query 2: Popular Keywords
-- Description: Find keywords that appear in more than 100 movies
-- Complexity: Medium | Operations: JOIN, GROUP BY, HAVING, ORDER BY, COUNT
SELECT k.keyword, COUNT(mk.movie_id) AS num_movies 
FROM keyword AS k 
JOIN movie_keyword AS mk ON k.id = mk.keyword_id 
GROUP BY k.keyword 
HAVING COUNT(mk.movie_id) > 100 
ORDER BY num_movies DESC;

-- Query 3: Prolific Actors
-- Description: Find actors/actresses with more than 50 roles
-- Complexity: Medium | Operations: JOIN, GROUP BY, HAVING, ORDER BY, COUNT, WHERE IN
SELECT n.name, COUNT(ci.person_id) AS num_roles 
FROM name AS n 
JOIN cast_info AS ci ON n.id = ci.person_id 
WHERE ci.role_id IN (1, 2) 
GROUP BY n.name 
HAVING COUNT(ci.person_id) > 50 
ORDER BY num_roles DESC;

-- Query 4: High Rated Movies
-- Description: Find movies from 2000-2020 with average rating above 7
-- Complexity: High | Operations: JOIN, GROUP BY, HAVING, ORDER BY, AVG, CAST
SELECT t.title, AVG(mi.info::integer) AS average_rating 
FROM title AS t 
JOIN movie_info AS mi ON t.id = mi.movie_id 
WHERE mi.info_type_id = 101 
  AND t.production_year BETWEEN 2000 AND 2020 
GROUP BY t.title 
HAVING AVG(mi.info::integer) > 7 
ORDER BY average_rating DESC;

-- Query 5: Movie Relationships
-- Description: Find movie-to-movie relationships (sequels, remakes, etc.) for movies from 2000-2020
-- Complexity: High | Operations: MULTIPLE JOIN, WHERE IN, BETWEEN
SELECT t1.title AS movie1, t2.title AS movie2, lt.link 
FROM movie_link AS ml 
JOIN title AS t1 ON ml.movie_id = t1.id 
JOIN title AS t2 ON ml.linked_movie_id = t2.id 
JOIN link_type AS lt ON ml.link_type_id = lt.id 
WHERE ml.link_type_id IN (9, 10, 12) 
  AND t1.production_year BETWEEN 2000 AND 2020;

-- Query 6: Movies with Multiple Production Companies
-- Description: Find movies from 2000-2020 associated with more than 5 companies
-- Complexity: Medium | Operations: JOIN, GROUP BY, HAVING, ORDER BY, COUNT
SELECT t.title, COUNT(mc.company_id) AS num_companies 
FROM title AS t 
JOIN movie_companies AS mc ON t.id = mc.movie_id 
WHERE t.production_year BETWEEN 2000 AND 2020 
GROUP BY t.title 
HAVING COUNT(mc.company_id) > 5 
ORDER BY num_companies DESC;

-- Query 7: Keyword Rich Movies
-- Description: Find movies from 2000-2020 with more than 20 associated keywords
-- Complexity: Medium | Operations: JOIN, GROUP BY, HAVING, ORDER BY, COUNT
SELECT t.title, COUNT(mk.keyword_id) AS num_keywords 
FROM title AS t 
JOIN movie_keyword AS mk ON t.id = mk.movie_id 
WHERE t.production_year BETWEEN 2000 AND 2020 
GROUP BY t.title 
HAVING COUNT(mk.keyword_id) > 20 
ORDER BY num_keywords DESC;

-- Query 8: People with Rich Biographical Data
-- Description: Find people with more than 10 personal information facts
-- Complexity: Medium | Operations: JOIN, GROUP BY, HAVING, ORDER BY, COUNT, WHERE IN
SELECT n.name, COUNT(pi.person_id) AS num_facts 
FROM name AS n 
JOIN person_info AS pi ON n.id = pi.person_id 
WHERE pi.info_type_id IN (2, 3, 4) 
GROUP BY n.name 
HAVING COUNT(pi.person_id) > 10 
ORDER BY num_facts DESC;

-- Query 9: Information Rich Movies
-- Description: Find movies from 2000-2020 with more than 15 different information entries
-- Complexity: Medium | Operations: JOIN, GROUP BY, HAVING, ORDER BY, COUNT
SELECT t.title, COUNT(mi.movie_id) AS num_movie_info 
FROM title AS t 
JOIN movie_info AS mi ON t.id = mi.movie_id 
WHERE t.production_year BETWEEN 2000 AND 2020 
GROUP BY t.title 
HAVING COUNT(mi.movie_id) > 15 
ORDER BY num_movie_info DESC;

-- ============================================================================
-- END OF OLAP WORKLOAD
-- ============================================================================
-- Statistics:
--   - Total Queries: 9
--   - Complexity: 7 Medium, 2 High
--   - Common Operations: JOIN (9), GROUP BY (8), HAVING (8), ORDER BY (8)
--   - Tables Used: title, cast_info, keyword, movie_keyword, name, 
--                  movie_info, movie_link, link_type, movie_companies, 
--                  person_info
-- ============================================================================