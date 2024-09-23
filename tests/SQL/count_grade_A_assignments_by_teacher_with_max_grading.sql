-- Query to count grade A assignments for each teacher
SELECT teacher_id, grade, COUNT(*) AS grade_a_count
FROM assignments
WHERE grade = 'A'
GROUP BY teacher_id;

-- Query to count grade A assignments for the teacher with the most graded assignments
WITH TeacherGrades AS (
    SELECT teacher_id, COUNT(*) AS total_graded
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
),
TopTeacher AS (
    SELECT teacher_id
    FROM TeacherGrades
    ORDER BY total_graded DESC
    LIMIT 1
)
SELECT COUNT(*) AS grade_a_count
FROM assignments
WHERE grade = 'A' AND teacher_id = (SELECT teacher_id FROM TopTeacher);
