CREATE DATABASE PhantomPhontenotPhitness;

USE PhantomPhontenotPhitness;

CREATE USER IF NOT EXISTS 'phontenot'@'%' IDENTIFIED BY 'phitness';
GRANT ALL PRIVILEGES ON PhantomPhontenotPhitness.* TO 'phontenot'@'%';

CREATE TABLE user (
 id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
 weight INTEGER,
 height INTEGER,
 date_of_birth DATE,
 joined DATETIME,
 last_name VARCHAR(40),
 first_name VARCHAR(40),
 goal_weight INTEGER
);

CREATE TABLE coach (
 id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
 began_coaching DATE,
 joined DATETIME,
 last_name VARCHAR(40),
 first_name VARCHAR(40)
);

CREATE TABLE athlete (
 id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
 weight INTEGER,
 height INTEGER,
 date_of_birth DATE,
 joined DATETIME,
 last_name VARCHAR(40),
 first_name VARCHAR(40),
 goal_weight INTEGER,
 coach_id INTEGER,
 FOREIGN KEY (coach_id) REFERENCES coach(id) ON DELETE SET NULL
);

CREATE TABLE friends (
   athlete_id_1 INTEGER NOT NULL,
   athlete_id_2 INTEGER NOT NULL,
   PRIMARY KEY(athlete_id_1, athlete_id_2),
   FOREIGN KEY (athlete_id_1) REFERENCES athlete(id) ON DELETE CASCADE,
   FOREIGN KEY (athlete_id_2) REFERENCES athlete(id) ON DELETE CASCADE
);


CREATE TABLE admin (
  first varchar(40),
  last varchar(40),
  email varchar(50) NOT NULL,
  admin_perms tinyint(1),
  id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL
);


CREATE TABLE manages_athlete (
   athlete_id INTEGER NOT NULL,
   admin_id INTEGER NOT NULL,
   PRIMARY KEY(athlete_id, admin_id),
   FOREIGN KEY (athlete_id) REFERENCES athlete(id) ON DELETE CASCADE,
   FOREIGN KEY (admin_id) REFERENCES admin(id) ON DELETE CASCADE
);


CREATE TABLE manages_user (
   user_id INTEGER NOT NULL,
   admin_id INTEGER NOT NULL,
   PRIMARY KEY(user_id, admin_id),
   FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
   FOREIGN KEY (admin_id) REFERENCES admin(id) ON DELETE CASCADE
);


CREATE TABLE manages_coach (
   coach_id INTEGER NOT NULL,
   admin_id INTEGER NOT NULL,
   PRIMARY KEY(coach_id, admin_id),
   FOREIGN KEY (coach_id) REFERENCES coach(id) ON DELETE CASCADE,
   FOREIGN KEY (admin_id) REFERENCES admin(id) ON DELETE CASCADE
);


CREATE TABLE feedback (
   comment_text TEXT,
   time_submitted DATETIME NOT NULL,
   id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
   submitter_name VARCHAR(40),
   email VARCHAR(100),
   admin_id INTEGER NOT NULL,
   FOREIGN KEY (admin_id) REFERENCES admin(id) ON DELETE CASCADE
);

