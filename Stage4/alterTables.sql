--1

CREATE TABLE Shifts (
  shiftId SERIAL PRIMARY KEY,
  branchId NUMERIC NOT NULL,
  shiftDate DATE NOT NULL,
  shiftTime VARCHAR NOT NULL CHECK (shiftTime IN ('morning', ‘evening’)),
  FOREIGN KEY (branchId) REFERENCES Branches(branchId)
);

--2

CREATE TABLE EmployeeShifts (
  employeeId NUMERIC NOT NULL,
  shiftId NUMERIC NOT NULL,
  PRIMARY KEY (employeeId, shiftId),
  FOREIGN KEY (employeeId) REFERENCES Employee(employeeId),
  FOREIGN KEY (shiftId) REFERENCES Shifts(shiftId)
);

--3

CREATE TABLE LogChanges (
  logId SERIAL PRIMARY KEY,
  tableName VARCHAR NOT NULL,
  operation VARCHAR NOT NULL, -- INSERT, UPDATE, DELETE
  changedBy VARCHAR DEFAULT CURRENT_USER,
  changeTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  oldData JSONB,
  newData JSONB
);

