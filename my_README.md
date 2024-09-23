Docker---
        Build_image = docker build -t task .
        Run Container = docker run -p 5000:5000 -v $(pwd)/store.sqlite3:/app/store.sqlite3 task                                                  


App---
    Run = flask run


Important Note on Test Case Validation----
   There is an issue with assignment drafts: Assignments can only be submitted if they are in draft status. However, if a new assignment is created and its ID is passed in the test cases, the draft status is automatically changed to submitted. This leads to test failures in subsequent checks since those assignments are not correctly recognized as drafts. New assignment IDs must be passed in the test cases to avoid these failures.
