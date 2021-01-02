-- Table Creation

create table ctf(
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name varchar(500) NOT NULL,
    createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) AUTO_INCREMENT = 1;


create table users(
    user_name varchar(100) NOT NULL PRIMARY KEY,
    pass_word varchar(200) NOT NULL
);

-- Queries

INSERT INTO ctf (name) values ('paargav');
INSERT INTO ctf (name) values ('bruno');

INSERT INTO users (user_name,pass_word) values ('user123','sha256$kwSJfqDP$439ea7adbfa75360d6aedb36b8daf71d7ee4e3d11baccec8af95c161b0bd1b3f');
INSERT INTO users (user_name,pass_word) values ('user456','sha256$ilP3KGkZ$12802bab86a82e243b0ac4a30391691c4d80868586cd1a0866debc632dd44c82');
INSERT INTO users (user_name,pass_word) values ('user789','sha256$aLFQ7uWr$5de2228064126536e8dafb7110deaa4bf8dc8addbac88365b2a9256bff37c476');