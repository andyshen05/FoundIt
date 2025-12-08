DROP DATABASE IF EXISTS foundit;
CREATE DATABASE foundit;
USE foundit;

CREATE TABLE IF NOT EXISTS admin (
    adminID INT PRIMARY KEY,
    email VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS settings (
    settingID INT PRIMARY KEY,
    value VARCHAR(255),
    adminID INT,
    FOREIGN KEY (adminID) REFERENCES admin(adminID)
);

CREATE TABLE IF NOT EXISTS analytics (
    analyticsID INT PRIMARY KEY,
    timestamp DATETIME,
    adminID INT,
    FOREIGN KEY (adminID) REFERENCES admin(adminID)
);

CREATE TABLE IF NOT EXISTS usage_stats (
    usageID INT PRIMARY KEY,
    activeUsers INT,
    submissions INT,
    analyticsID INT,
    FOREIGN KEY (analyticsID) REFERENCES analytics(analyticsID)
);

CREATE TABLE IF NOT EXISTS item_stats (
    statID INT PRIMARY KEY,
    numReports INT,
    matchRate DECIMAL(5,2),
    analyticsID INT,
    FOREIGN KEY (analyticsID) REFERENCES analytics(analyticsID)
);

CREATE TABLE IF NOT EXISTS user_log (
    logID INT PRIMARY KEY,
    timestamp DATETIME,
    activity VARCHAR(255),
    adminID INT,
    FOREIGN KEY (adminID) REFERENCES admin(adminID)
);

CREATE TABLE IF NOT EXISTS moderation (
    modID INT PRIMARY KEY,
    timestamp DATETIME,
    modType VARCHAR(100),
    adminID INT,
    FOREIGN KEY (adminID) REFERENCES admin(adminID)
);

CREATE TABLE IF NOT EXISTS user (
    userID INT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    phoneNumber VARCHAR(20),
    accStatus VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS category (
    categoryID INT PRIMARY KEY,
    categoryName VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS location (
    locationID INT PRIMARY KEY,
    lastSeenAt VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS items (
    itemID INT PRIMARY KEY,
    description TEXT,
    status VARCHAR(50),
    dateFound DATETIME,
    daysInStorage INT,
    categoryID INT,
    FOREIGN KEY (categoryID) REFERENCES category(categoryID)
);

CREATE TABLE IF NOT EXISTS lost_item_report (
    lostReportID INT PRIMARY KEY,
    dateLost DATETIME,
    userID INT,
    locationID INT,
    FOREIGN KEY (userID) REFERENCES user(userID),
    FOREIGN KEY (locationID) REFERENCES location(locationID)
);

CREATE TABLE IF NOT EXISTS reward (
    rewardID INT PRIMARY KEY,
    rewardAmount DECIMAL(10,2),
    lostReportID INT,
    FOREIGN KEY (lostReportID) REFERENCES lost_item_report(lostReportID)
);

CREATE TABLE IF NOT EXISTS found_item_report (
    foundReportID INT PRIMARY KEY,
    dateFound DATETIME,
    `condition` VARCHAR(255),
    userID INT,
    locationID INT,
    itemID INT,
    FOREIGN KEY (userID) REFERENCES user(userID),
    FOREIGN KEY (locationID) REFERENCES location(locationID),
    FOREIGN KEY (itemID) REFERENCES items(itemID)
);

CREATE TABLE IF NOT EXISTS notification (
    notificationID INT PRIMARY KEY,
    message TEXT,
    userID INT,
    FOREIGN KEY (userID) REFERENCES user(userID)
);

CREATE TABLE IF NOT EXISTS desk_manager (
    managerID INT PRIMARY KEY,
    name VARCHAR(255),
    phoneNumber VARCHAR(50),
    email VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS storage_location (
    storageLocationID INT PRIMARY KEY,
    shelfNumber VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS found_item_inventory (
    inventoryID INT PRIMARY KEY,
    dateReceived DATETIME,
    managerID INT,
    itemID INT,
    storageLocationID INT,
    FOREIGN KEY (managerID) REFERENCES desk_manager(managerID),
    FOREIGN KEY (itemID) REFERENCES items(itemID),
    FOREIGN KEY (storageLocationID) REFERENCES storage_location(storageLocationID)
);

CREATE TABLE IF NOT EXISTS claim_record (
    claimID INT PRIMARY KEY,
    claimDate DATETIME,
    claimerEmail VARCHAR(255),
    itemID INT,
    managerID INT,
    FOREIGN KEY (itemID) REFERENCES items(itemID),
    FOREIGN KEY (managerID) REFERENCES desk_manager(managerID)
);

CREATE TABLE IF NOT EXISTS report (
    reportID INT PRIMARY KEY,
    content TEXT,
    modID INT,
    logID INT,
    userID INT,
    FOREIGN KEY (modID) REFERENCES moderation(modID),
    FOREIGN KEY (logID) REFERENCES user_log(logID),
    FOREIGN KEY (userID) REFERENCES user(userID)
);
