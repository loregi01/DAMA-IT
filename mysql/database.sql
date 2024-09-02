use db;

DROP TABLE IF EXISTS statistic, user, umessage, play, friend;

CREATE TABLE statistic (
    StatisticID int not null AUTO_INCREMENT,
    TotGames varchar(100) NOT NULL,
    TotWins varchar(100) NOT NULL,
    TotDraw varchar(100) NOT NULL,
    Elo varchar(100) NOT NULL,
    SLevel varchar(100) NOT NULL,
    PRIMARY KEY (StatisticID)
);

CREATE TABLE user (
    UserID int not null AUTO_INCREMENT,
    FirstName varchar(100) NOT NULL,
    Surname varchar(100) NOT NULL,
    Email varchar(100) NOT NULL,
    UPassword varchar(100) NOT NULL,
    Username varchar(100) NOT NULL,
    Birthdate varchar(100) NOT NULL,
    Statistic int NOT NULL,
    PRIMARY KEY (UserID),
    FOREIGN KEY (Statistic) REFERENCES statistic (StatisticID)
);

CREATE TABLE umessage (
    MessageID int not null AUTO_INCREMENT,
    Content varchar(100) NOT NULL,
    MDateTime varchar(100) NOT NULL,
    Sender varchar(100) NOT NULL,
    PRIMARY KEY (MessageID)
);

CREATE TABLE friend (
    FriendID int not null AUTO_INCREMENT,
    User1 int NOT NULL,
    User2 int NOT NULL,
    Fmessage int NOT NULL,
    PRIMARY KEY (FriendID),
    FOREIGN KEY (User1) REFERENCES user (UserID),
    FOREIGN KEY (User2) REFERENCES user (UserID),
    FOREIGN KEY (Fmessage) REFERENCES umessage (MessageID)
);

CREATE TABLE play (
    PlayID int not null AUTO_INCREMENT,
    Player1 int NOT NULL,
    Player2 int NOT NULL,
    PDateTime varchar(100) NOT NULL,
    WhitePlayer int NOT NULL,
    Winner varchar(100) NOT NULL,
    Elo1 varchar(100) NOT NULL,
    Elo2 varchar(100) NOT NULL,
    PRIMARY KEY (PlayID),
    FOREIGN KEY (Player1) REFERENCES user (UserID),
    FOREIGN KEY (Player2) REFERENCES user (UserID)
);
