// Node Tables
CREATE NODE TABLE Disease(name STRING, description STRING, type STRING, PRIMARY KEY (name));
CREATE NODE TABLE Symptom(name STRING, PRIMARY KEY (name));
CREATE NODE TABLE Diagnostic(name STRING, type STRING, PRIMARY KEY (name));
CREATE NODE TABLE Treatment(name STRING, type STRING, PRIMARY KEY (name));
CREATE NODE TABLE MedicalSpecialty(name STRING, PRIMARY KEY (name));

// Relationship Tables
CREATE REL TABLE HAS_SYMPTOM(FROM Disease TO Symptom, prevalence STRING);
CREATE REL TABLE DIAGNOSED_BY(FROM Disease TO Diagnostic);
CREATE REL TABLE TREATED_BY(FROM Disease TO Treatment);
CREATE REL TABLE MANAGED_BY(FROM Disease TO MedicalSpecialty);