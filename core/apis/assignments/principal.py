from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse

from core.models import Teacher , Assignment,AssignmentStateEnum
from sqlalchemy import select

from .schema import AssignmentSchema , TeacherSchema , AssignmentGradeSchema



principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""

    assignments_q = select(Assignment).where(
        Assignment.state.in_([AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED])
    )
    
    assignments=db.session.execute(assignments_q).scalars().all()
    
    students_assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)


@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_Teachers(p):
    
        
    teachers = db.session.query(Teacher).all()

    teachers_dump= TeacherSchema().dump(teachers,many=True)
    return APIResponse.respond(data=teachers_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal

def grade_assignment(p, incoming_payload):
    """Re*Grade an assignment"""
    
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)

   