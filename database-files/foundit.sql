DROP DATABASE IF EXISTS foundit;
CREATE DATABASE foundit;
USE foundit;

CREATE TABLE IF NOT EXISTS Admin (
    adminID INT PRIMARY KEY,
    email VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Settings (
    settingID INT PRIMARY KEY,
    value VARCHAR(255),
    adminID INT,
    FOREIGN KEY (adminID) REFERENCES Admin(adminID)
);

CREATE TABLE IF NOT EXISTS Analytics (
    analyticsID INT PRIMARY KEY,
    timestamp DATETIME,
    adminID INT,
    FOREIGN KEY (adminID) REFERENCES Admin(adminID)
);

CREATE TABLE IF NOT EXISTS Usage_Stats (
    usageID INT PRIMARY KEY,
    activeUsers INT,
    submissions INT,
    analyticsID INT,
    FOREIGN KEY (analyticsID) REFERENCES Analytics(analyticsID)
);

CREATE TABLE IF NOT EXISTS Item_Stats (
    statID INT PRIMARY KEY,
    numReports INT,
    matchRate DECIMAL(5,2),
    analyticsID INT,
    FOREIGN KEY (analyticsID) REFERENCES Analytics(analyticsID)
);

CREATE TABLE IF NOT EXISTS User_Log (
    logID INT PRIMARY KEY,
    timestamp DATETIME,
    activity VARCHAR(255),
    adminID INT,
    FOREIGN KEY (adminID) REFERENCES Admin(adminID)
);

CREATE TABLE IF NOT EXISTS Moderation (
    modID INT PRIMARY KEY,
    timestamp DATETIME,
    modType VARCHAR(100),
    adminID INT,
    FOREIGN KEY (adminID) REFERENCES Admin(adminID)
);

CREATE TABLE IF NOT EXISTS User (
    userID INT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    phoneNumber VARCHAR(20),
    accStatus VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Category (
    categoryID INT PRIMARY KEY,
    categoryName VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Location (
    locationID INT PRIMARY KEY,
    lastSeenAt VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Item (
    itemID INT PRIMARY KEY,
    description TEXT,
    status VARCHAR(50),
    dateFound DATETIME,
    daysInStorage INT,
    categoryID INT,
    FOREIGN KEY (categoryID) REFERENCES Category(categoryID)
);

CREATE TABLE IF NOT EXISTS Lost_Item_Report (
    lostReportID INT PRIMARY KEY,
    dateLost DATETIME,
    userID INT,
    locationID INT,
    FOREIGN KEY (userID) REFERENCES User(userID),
    FOREIGN KEY (locationID) REFERENCES Location(locationID)
);

CREATE TABLE IF NOT EXISTS Reward (
    rewardID INT PRIMARY KEY,
    rewardAmount DECIMAL(10,2),
    lostReportID INT,
    FOREIGN KEY (lostReportID) REFERENCES Lost_Item_Report(lostReportID)
);

CREATE TABLE IF NOT EXISTS Found_Item_Report (
    foundReportID INT PRIMARY KEY,
    dateFound DATETIME,
    `condition` VARCHAR(255),
    userID INT,
    locationID INT,
    itemID INT,
    FOREIGN KEY (userID) REFERENCES User(userID),
    FOREIGN KEY (locationID) REFERENCES Location(locationID),
    FOREIGN KEY (itemID) REFERENCES Item(itemID)
);

CREATE TABLE IF NOT EXISTS Notification (
    notificationID INT PRIMARY KEY,
    message TEXT,
    userID INT,
    FOREIGN KEY (userID) REFERENCES User(userID)
);

CREATE TABLE IF NOT EXISTS Desk_Manager (
    managerID INT PRIMARY KEY,
    name VARCHAR(255),
    phoneNumber VARCHAR(50),
    email VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Storage_Location (
    storageLocationID INT PRIMARY KEY,
    shelfNumber VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Found_Item_Inventory (
    inventoryID INT PRIMARY KEY,
    dateReceived DATETIME,
    managerID INT,
    itemID INT,
    storageLocationID INT,
    FOREIGN KEY (managerID) REFERENCES Desk_Manager(managerID),
    FOREIGN KEY (itemID) REFERENCES Item(itemID),
    FOREIGN KEY (storageLocationID) REFERENCES Storage_Location(storageLocationID)
);

CREATE TABLE IF NOT EXISTS ClaimRecord (
    claimID INT PRIMARY KEY,
    claimDate DATETIME,
    claimerEmail VARCHAR(255),
    itemID INT,
    managerID INT,
    FOREIGN KEY (itemID) REFERENCES Item(itemID),
    FOREIGN KEY (managerID) REFERENCES Desk_Manager(managerID)
);

CREATE TABLE IF NOT EXISTS Report (
    reportID INT PRIMARY KEY,
    content TEXT,
    modID INT,
    logID INT,
    userID INT,
    FOREIGN KEY (modID) REFERENCES Moderation(modID),
    FOREIGN KEY (logID) REFERENCES User_Log(logID),
    FOREIGN KEY (userID) REFERENCES User(userID)
);
