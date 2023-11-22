CREATE TABLE TelemetryData

(

    TelemetryDataID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,

    Temperature DECIMAL(18,2),

    Humidity DECIMAL(18,2),

    LogDate DATETIME DEFAULT GETDATE()

)