-- app_user
CREATE TABLE app_user (
  id SERIAL PRIMARY KEY,
  username VARCHAR(80) UNIQUE NOT NULL,
  password TEXT NOT NULL,
  email_address VARCHAR(255) UNIQUE NOT NULL,
  role VARCHAR(20) NOT NULL CHECK (role IN ('admin','standard')) DEFAULT 'standard',
  update_password BOOLEAN
);

-- PROJECT
CREATE TABLE project (
  id SERIAL PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  problem_id INTEGER,
  solution_id INTEGER,
  difficulty INTEGER CHECK (difficulty BETWEEN 1 AND 5)
);

-- PROBLEM
CREATE TABLE problem (
  id SERIAL PRIMARY KEY,
  git_link VARCHAR(255) NOT NULL,
  problem_description TEXT
);

-- SOLUTION
CREATE TABLE solution (
  id SERIAL PRIMARY KEY,
  git_link VARCHAR(255) NOT NULL,
  solution_description TEXT NOT NULL
);

-- VIDEO
CREATE TABLE video (
  id SERIAL PRIMARY KEY,
  project_id INTEGER NOT NULL REFERENCES project(id) ON DELETE CASCADE,
  yt_code VARCHAR(32) NOT NULL,
  type VARCHAR(16) CHECK (type IN ('intro','tutorial','solution')),
  ordinal INTEGER
);

-- SUBMISSION (composite PK)
CREATE TABLE submission (
  app_user_id INTEGER NOT NULL REFERENCES app_user(id) ON DELETE CASCADE,
  project_id INTEGER NOT NULL REFERENCES project(id) ON DELETE CASCADE,
  is_complete BOOLEAN NOT NULL DEFAULT FALSE,
  grade NUMERIC(5,2),
  PRIMARY KEY (app_user_id, project_id)
);

-- Add the FKs from project to problem/solution
ALTER TABLE project
  ADD CONSTRAINT fk_project_problem FOREIGN KEY (problem_id) REFERENCES problem(id) ON DELETE RESTRICT;
ALTER TABLE project
  ADD CONSTRAINT fk_project_solution FOREIGN KEY (solution_id) REFERENCES solution(id) ON DELETE RESTRICT;
