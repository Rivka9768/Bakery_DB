CREATE TABLE Shifts (
  shiftId SERIAL PRIMARY KEY,
  branchId NUMERIC NOT NULL,
  shiftDate DATE NOT NULL,
  shiftTime VARCHAR NOT NULL CHECK (shiftTime IN ('morning', ‘evening’)),
  FOREIGN KEY (branchId) REFERENCES Branches(branchId)
);



CREATE TABLE EmployeeShifts (
  employeeId NUMERIC NOT NULL,
  shiftId NUMERIC NOT NULL,
  PRIMARY KEY (employeeId, shiftId),
  FOREIGN KEY (employeeId) REFERENCES Employee(employeeId),
  FOREIGN KEY (shiftId) REFERENCES Shifts(shiftId)
);
