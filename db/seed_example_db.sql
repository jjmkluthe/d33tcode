-- ChatGPT was used to help generate example data
-- I refactored this to match my own vision for the project

-- db/seed.sql
-- Seed data for the d33tcode project
-- Run after tables exist:  psql -d d33tcode -f db/seed.sql

BEGIN;

-- Clear existing data and reset sequences
TRUNCATE TABLE
    submission,
    video,
    project,
    solution,
    problem,
    app_user
RESTART IDENTITY CASCADE;

------------------------------------------------------------
-- Users (10 rows)
------------------------------------------------------------
INSERT INTO app_user (id, username, password, email_address, role, update_password) VALUES
  (1, 'admin',  'placeholder', 'admin@example.com',  'admin', false),
  (2, 'alice',  'placeholder', 'alice@example.com',  'standard', false),
  (3, 'bob',    'placeholder', 'bob@example.com',    'standard', false),
  (4, 'carol',  'placeholder', 'carol@example.com',  'standard', false),
  (5, 'dave',   'placeholder', 'dave@example.com',   'standard', false),
  (6, 'erin',   'placeholder', 'erin@example.com',   'standard', false),
  (7, 'frank',  'placeholder', 'frank@example.com',  'standard', false),
  (8, 'grace',  'placeholder', 'grace@example.com',  'standard', false),
  (9, 'heidi',  'placeholder', 'heidi@example.com',  'standard', false),
  (10,'ivan',   'placeholder', 'ivan@example.com',   'standard', false);

------------------------------------------------------------
-- Problems (10 rows)
------------------------------------------------------------
INSERT INTO problem (id, git_link, problem_description) VALUES
  (1,  'https://github.com/d33tcode/problem-1',  'Fix off-by-one error in pagination.'),
  (2,  'https://github.com/d33tcode/problem-2',  'Resolve N+1 query in user listing.'),
  (3,  'https://github.com/d33tcode/problem-3',  'Handle null values in CSV import.'),
  (4,  'https://github.com/d33tcode/problem-4',  'Race condition in background job.'),
  (5,  'https://github.com/d33tcode/problem-5',  'Incorrect join on submissions.'),
  (6,  'https://github.com/d33tcode/problem-6',  'Caching bug on project detail view.'),
  (7,  'https://github.com/d33tcode/problem-7',  'Edge-case bug in grade rounding.'),
  (8,  'https://github.com/d33tcode/problem-8',  'Video embed breakage in old browsers.'),
  (9,  'https://github.com/d33tcode/problem-9',  'API returns inconsistent status codes.'),
  (10, 'https://github.com/d33tcode/problem-10', 'Deployment config mismatch.');

------------------------------------------------------------
-- Solutions (10 rows)
------------------------------------------------------------
INSERT INTO solution (id, git_link, solution_description) VALUES
  (1,  'https://github.com/d33tcode/problem-1-solution',  'Normalize page indices and bounds.'),
  (2,  'https://github.com/d33tcode/problem-2-solution',  'Add eager loading with proper joins.'),
  (3,  'https://github.com/d33tcode/problem-3-solution',  'Validate and coerce nulls on import.'),
  (4,  'https://github.com/d33tcode/problem-4-solution',  'Use locking around shared resources.'),
  (5,  'https://github.com/d33tcode/problem-5-solution',  'Adjust join condition and foreign keys.'),
  (6,  'https://github.com/d33tcode/problem-6-solution',  'Bust cache on relevant updates.'),
  (7,  'https://github.com/d33tcode/problem-7-solution',  'Centralize grade calculation logic.'),
  (8,  'https://github.com/d33tcode/problem-8-solution',  'Polyfill embed API and add fallbacks.'),
  (9,  'https://github.com/d33tcode/problem-9-solution',  'Standardize API error handling module.'),
  (10, 'https://github.com/d33tcode/problem-10-solution', 'Align configs across environments.');

------------------------------------------------------------
-- Projects (10 rows)
------------------------------------------------------------
INSERT INTO project (id, title, description, problem_id, solution_id, difficulty) VALUES
  (1,  'Pagination Fix',          'Debug and fix pagination on the project list.',          1,  1,  2),
  (2,  'User Listing Performance','Optimize user list queries and indexes.',               2,  2,  3),
  (3,  'CSV Import Cleanup',      'Harden CSV import for bad data.',                        3,  3,  2),
  (4,  'Background Jobs',         'Stabilize and observe background workers.',              4,  4,  4),
  (5,  'Submission Joins',        'Fix joins between projects and submissions.',            5,  5,  3),
  (6,  'Cache Invalidation',      'Implement safe cache invalidation.',                     6,  6,  4),
  (7,  'Grading Logic',           'Unify grading logic across the app.',                    7,  7,  3),
  (8,  'Video Embeds',            'Improve video embedding across devices.',                8,  8,  2),
  (9,  'API Error Handling',      'Standardize API error responses.',                       9,  9,  4),
  (10, 'Deployment Review',       'Review and fix deployment configuration issues.',       10, 10,  5);

------------------------------------------------------------
-- Videos (>=10 rows)
-- 3 videos (intro/tutorial/solution) for first 4 projects, 1 intro each for 5 and 6.
------------------------------------------------------------
INSERT INTO video (id, project_id, yt_code, type, ordinal) VALUES
  (1,  1, 'VID-P1-INTRO',    'intro',    1),
  (2,  1, 'VID-P1-TUTORIAL', 'tutorial', 1),
  (3,  1, 'VID-P1-SOLUTION', 'solution', 1),

  (4,  2, 'VID-P2-INTRO',    'intro',    1),
  (5,  2, 'VID-P2-TUTORIAL', 'tutorial', 1),
  (6,  2, 'VID-P2-SOLUTION', 'solution', 1),

  (7,  3, 'VID-P3-INTRO',    'intro',    1),
  (8,  3, 'VID-P3-TUTORIAL', 'tutorial', 1),
  (9,  3, 'VID-P3-SOLUTION', 'solution', 1),

  (10, 4, 'VID-P4-INTRO',    'intro',    1),
  (11, 4, 'VID-P4-TUTORIAL', 'tutorial', 1),
  (12, 4, 'VID-P4-SOLUTION', 'solution', 1),

  (13, 5, 'VID-P5-INTRO',    'intro',    1),
  (14, 6, 'VID-P6-INTRO',    'intro',    1);

------------------------------------------------------------
-- Submissions (>=10 rows)
-- Each non-admin user submits for the first two projects.
------------------------------------------------------------
INSERT INTO submission (app_user_id, project_id, is_complete, grade) VALUES
  (2, 1, TRUE,  95.00),
  (2, 2, TRUE,  88.50),
  (3, 1, FALSE, NULL),
  (3, 2, TRUE,  91.00),
  (4, 1, TRUE,  84.25),
  (4, 2, FALSE, NULL),
  (5, 1, TRUE,  90.00),
  (5, 2, TRUE,  92.75),
  (6, 1, FALSE, NULL),
  (6, 2, TRUE,  87.00),
  (7, 1, TRUE,  80.00),
  (7, 2, TRUE,  89.25),
  (8, 1, TRUE,  93.50),
  (8, 2, FALSE, NULL),
  (9, 1, TRUE,  85.00),
  (9, 2, TRUE,  86.75),
  (10,1, FALSE, NULL),
  (10,2, TRUE,  90.50);

COMMIT;
