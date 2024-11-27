# INIT & RUN PROJECT

source init_project.sh

---

# UP PROJECT 

source init_project.sh -up

---

# UP VIRTUAL ENVIRONMENT

activate_venv

---

# DOWN VIRTUAL ENVIRONMENT

deactivate

---

# RUN TESTS

py ./d07/manage.py test ex.tests -v 2