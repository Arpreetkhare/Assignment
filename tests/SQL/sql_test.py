import random
from sqlalchemy import text

from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum


def create_n_graded_assignments_for_teacher(number: int = 0, teacher_id: int = 1) -> int:
    """
    Creates 'n' graded assignments for a specified teacher and returns the count of assignments with grade 'A'.

    Parameters:
    - number (int): The number of assignments to be created.
    - teacher_id (int): The ID of the teacher for whom the assignments are created.

    Returns:
    - int: Count of assignments with grade 'A'.
    """
    # Count the existing assignments with grade 'A' for the specified teacher
    grade_a_counter: int = Assignment.filter(
        Assignment.teacher_id == teacher_id,
        Assignment.grade == GradeEnum.A
    ).count()

    # Create 'n' graded assignments
    for _ in range(number):
        # Randomly select a grade from GradeEnum
        grade = random.choice(list(GradeEnum))

        # Create a new Assignment instance
        assignment = Assignment(
            teacher_id=teacher_id,
            student_id=1,
            grade=grade,
            content='test content',
            state=AssignmentStateEnum.GRADED
        )

        # Add the assignment to the database session
        db.session.add(assignment)

        # Update the grade_a_counter if the grade is 'A'
        if grade == GradeEnum.A:
            grade_a_counter = grade_a_counter + 1

    # Commit changes to the database
    db.session.commit()

    # Return the count of assignments with grade 'A'
    return grade_a_counter


def test_get_assignments_in_graded_state_for_each_student():
    """Test to get graded assignments for each student"""

    # Find all the assignments for student 1 and change its state to 'GRADED'
    submitted_assignments: Assignment = Assignment.filter(Assignment.student_id == 1)

    # Iterate over each assignment and update its state
    for assignment in submitted_assignments:
        assignment.state = AssignmentStateEnum.GRADED  # Or any other desired state

    # Flush the changes to the database session
    db.session.flush()
    # Commit the changes to the database
    db.session.commit()

    # Define the expected result before any changes
    expected_result = [(1, 3)]

    # Execute the SQL query and compare the result with the expected result
    with open('tests/SQL/number_of_graded_assignments_for_each_student.sql', encoding='utf8') as fo:
        sql = fo.read()

    # Execute the SQL query compare the result with the expected result
    sql_result = db.session.execute(text(sql)).fetchall()
    for itr, result in enumerate(expected_result):
        assert result[0] == sql_result[itr][0]


def test_get_grade_A_assignments_for_teacher_with_max_grading():
    """Test to get count of grade A assignments for teacher which has graded maximum assignments"""

    # Read the SQL queries from a file
    with open('tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql', encoding='utf8') as fo:
        sql = fo.read().strip().split(';')  # Split by semicolon

    # Create and grade 5 assignments for the default teacher (teacher_id=1)
    grade_a_count_1 = create_n_graded_assignments_for_teacher(5)

    # Execute the first query to get count of grade A assignments for each teacher
    sql_result_1 = db.session.execute(text(sql[0])).fetchall()

    # Extract the count for teacher_id=1
    count_for_teacher_1 = next((count for tid, grade, count in sql_result_1 if tid == 1), 0)

    # Assert the result for teacher_id=1
    expected_count_for_teacher_1 = grade_a_count_1  # This should match the number you graded
    assert count_for_teacher_1 == expected_count_for_teacher_1, f"Expected {expected_count_for_teacher_1}, but got {count_for_teacher_1}"

    # Execute the second query to get count of grade A assignments for the top teacher
    sql_result_2 = db.session.execute(text(sql[1])).fetchall()

    # Calculate the expected count for the top teacher
    if sql_result_1:  # Ensure there are results
        top_teacher_id = max(sql_result_1, key=lambda x: x[2])[0]  # Get the teacher with the max graded assignments
        expected_grade_a_count = sum(count for tid, grade, count in sql_result_1 if tid == top_teacher_id and grade == 'A')
    else:
        expected_grade_a_count = 0  # Fallback in case there are no results

    # Assert the result for the top teacher's grade A count
    assert sql_result_2[0][0] == expected_grade_a_count, f"Expected {expected_grade_a_count}, but got {sql_result_2[0][0]}"
