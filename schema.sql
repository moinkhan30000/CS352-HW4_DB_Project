DROP DATABASE IF EXISTS cs353hw4db;
CREATE DATABASE cs353hw4db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE cs353hw4db;

CREATE TABLE student (
    sid CHAR(6) PRIMARY KEY,
    sname VARCHAR(50),
    bdate DATE,
    dept CHAR(2),
    year INT,
    gpa FLOAT
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE company (
    cid CHAR(5) PRIMARY KEY,
    cname VARCHAR(20),
    quota INT,
    gpa_threshold FLOAT,
    city VARCHAR(20)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE apply (
    app_no INT PRIMARY KEY,
    sid CHAR(6),
    cid CHAR(5),
    FOREIGN KEY (sid) REFERENCES student(sid) ON DELETE CASCADE,
    FOREIGN KEY (cid) REFERENCES company(cid) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Hocam I coud not make turkish characters work for some reason. I tried its encoding everywhere, it was not working so I just used english characters.
INSERT INTO student (sid, sname, bdate, dept, year, gpa) VALUES
('S101', 'Ali', '2005-03-11', 'CS', 2, 2.92),
('S102', 'Veli', '2002-01-07', 'EE', 3, 3.96),
('S103', 'Ayse', '2004-02-12', 'IE', 1, 3.30),
('S104', 'Mehmet', '2003-05-23', 'CS', 3, 3.07),
('S105', 'Zeynep', '2002-11-19', 'ME', 3, 2.55);


INSERT INTO company (cid, cname, quota, gpa_threshold, city) VALUES
('C101', 'tubitak', 10, 2.5, 'Ankara'),
('C102', 'bist', 2, 2.8, 'Istanbul'),
('C103', 'aselsan', 3, 3.0, 'Ankara'),
('C104', 'thy', 5, 2.4, 'Istanbul'),
('C105', 'milsoft', 6, 2.5, 'Ankara'),
('C106', 'amazon', 1, 3.8, 'Palo Alto'),
('C107', 'tai', 4, 3.0, 'Ankara'),
('C108', 'arcelik', 5, 2.75, 'Istanbul'),
('C109', 'siemens', 2, 2.5, 'Istanbul');

-- Hocam I only inserted 3 per student as that was the limit, instead of 4 and 5 from dummy data.
INSERT INTO apply (app_no, sid, cid) VALUES
(1, 'S101', 'C101'),
(2, 'S101', 'C102'),
(3, 'S101', 'C104'),

(4, 'S102', 'C103'),
(5, 'S102', 'C106'),
(6, 'S102', 'C107'),

(7, 'S103', 'C104'),
(8, 'S103', 'C107'),
(9, 'S103', 'C109'),

(10, 'S104', 'C102'),
(11, 'S104', 'C103'),
(12, 'S104', 'C107'),

(13, 'S105', 'C101'),
(14, 'S105', 'C104'),
(15, 'S105', 'C105');

