// This script is writen using Kuzu Graph Database Cypher syntax and features.

// Node table representing a person with their attributes.
CREATE NODE TABLE PERSON(person_id INT64 PRIMARY KEY, name STRING, birthDate DATE, description STRING);
// Node table representing a location.
CREATE NODE TABLE LOCATION(location_id INT64 PRIMARY KEY, name STRING);
// Node table representing a school.
CREATE NODE TABLE SCHOOL(school_id INT64 PRIMARY KEY, name STRING);
// Node table representing a hobby.
CREATE NODE TABLE HOBBY(hobby_id INT64 PRIMARY KEY, name STRING);
// Node table representing a job.
CREATE NODE TABLE JOB(job_id INT64 PRIMARY KEY, job_title STRING);
// Relationship table representing that a person lives in a location.
CREATE REL TABLE LIVES_IN( FROM PERSON TO LOCATION);
// Relationship table representing that a person is married to another person.
CREATE REL TABLE MARRIED_TO( FROM PERSON TO PERSON);
// Relationship table representing that a person studies at a school.
CREATE REL TABLE STUDIES_AT( FROM PERSON TO SCHOOL);
// Relationship table representing that a person is a parent of another person.
CREATE REL TABLE PARENT_OF( FROM PERSON TO PERSON);
// Relationship table representing that a person has a hobby.
CREATE REL TABLE HAS_HOBBY( FROM PERSON TO HOBBY);
// Relationship table representing that a person works as a certain job.
CREATE REL TABLE WORKS_AS( FROM PERSON TO JOB);
// Relationship table representing that a person is a child of another person.
CREATE REL TABLE CHILD_OF( FROM PERSON TO PERSON);
// Relationship table representing that a person is a sibling of another person.
CREATE REL TABLE SIBLING_OF( FROM PERSON TO PERSON);
