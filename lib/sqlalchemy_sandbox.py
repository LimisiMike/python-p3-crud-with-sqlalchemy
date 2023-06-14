#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    __table_args__ = (
        PrimaryKeyConstraint( 
            'id',
            name='id_pk'),
        UniqueConstraint(
            'email',
            name='unique-email'),
        CheckConstraint(
            'grade BETWEEN 1 AND 12',
            name='grade_between_1_and_12'
        )
        )
    #CONTRAINTS
# Along with keys, constraints help ensure that our data meets certain criteria before being stored in the database. Constraints are stored in the optional __table_args__ class attribute. There are three main classes of constraint:
# PrimaryKeyConstraint: assigns primary key status to a Column. This can also be accomplished through the optional primary_key argument to the Column class constructor.
# UniqueConstraint: checks new records to ensure that they do not match existing records at unique Columns.
# CheckConstraint: uses SQL statements to check if new values meet specific criteria.
# Our new constraints for the Student model ensure that id is a primary key, email is unique, and grade is between 1 and 12.

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())
    
    Index('index_name', 'name') #Indexes are used to speed up lookups on certain column values. 
    
    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
                + f"Grade{self.grade}"

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    
    # Use our engine to configure a Session class
    Session = sessionmaker(bind=engine)
    # Use 'Session' class to create 'session' object
    session = Session()
    
    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )
    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    # session.bulk_save_objects([albert_einstein, alan_turing]) -returns None for the IDs
    # session.commit()
    session.add(albert_einstein)
    session.commit()
    session.add(alan_turing)
    session.commit()
    
    print(f"New student ID is {albert_einstein.id}.")
    print(f"New student ID is {alan_turing.id}.")
    
    # After creating a Student object, session.add() generates a statement to include in the session's transaction, then session.commit() executes all statements in the transaction and saves any changes to the database. session.commit() will also update your Student object with a id.
    
    # READ RECORDS
    
    # After the session.commit,
    
    students = session.query(Student)
    
    print([student for student in students])
    # OR
    # students = session.query(Student).all()
    # print(students)
    
    # => [Student 1: Albert Einstein, Grade 6, Student 2: Alan Turing, Grade 11]
    
    # Selecting Only certain columns using the query() selector
    
    names = [name for name in session.query(Student.name)]
    
    print(names)

# Order By() - for ordering results from a db
    students_by_name = [student for student in session.query(Student.name).order_by(Student.name)]
    
    # SOrting
    students_by_name = [student for student in session.query(Student.name, Student.grade).order_by(desc(Student.grade))]
    # => [('Alan Turing', 11), ('Albert Einstein', 6)]

    
    # To limit your result set to the first x records, you can use the limit() method:
    oldest_student = [student for student in session.query(
            Student.name, Student.birthday).order_by(
            desc(Student.grade)).limit(1)] #Or replace limit with first()

    print(oldest_student)

# => [('Alan Turing', datetime.datetime(1912, 6, 23, 0, 0))]

# Importing func from sqlalchemy gives us access to common SQL operations through functions like sum() and count().
    student_count = session.query(func.count(Student.id)).first()

    print(student_count)

# => (2,)

# Filtering
# Retrieving specific records requires use of the filter() method. 
    query = session.query(Student).filter(Student.name.like('%Alan%'), Student.grade == 11)
    
    # => Alan Turing
    
    # Update method
    session.query(Student).update({Student.grade: Student.grade + 1})
    
    print([(student.name, student.grade) for student in session.query(Student)])
    
    # => [('Albert Einstein', 7), ('Alan Turing', 12)]
    
    # DELETING DATA
    query = session.query(Student).filter(Student.name == "Albert Einstein")
    
    #retrieve first matching record as Object
    albert_einstein = query.first()
    
    # Delete record
    session.delete(albert_einstein)
    session.commit()
    
    # Try to retrieve deleted record
    albert_einstein = query.first()
    
    print(albert_einstein)
    
    #  => None