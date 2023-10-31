from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from datetime import date

app = FastAPI()


class Employee(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    date_joined: date
    age: int = Field(..., ge=18)
    city: str = Field(..., min_length=1, max_length=50)
    library_id: int
    is_active: bool
    salary: float = Field(..., gt=0)


employees = []


@app.post("/employees")
def create_employee(employee: Employee):
    employees.append(employee)
    return {"message": "Employee created successfully"}


@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: Employee):
    if employee_id < 0 or employee_id >= len(employees):
        raise HTTPException(status_code=404, detail="Employee not found")
    employees[employee_id] = employee
    return {"message": "Employee updated successfully"}


@app.get("/employees/{employee_id}")
def get_employee_profile(employee_id: int):
    if employee_id < 0 or employee_id >= len(employees):
        raise HTTPException(status_code=404, detail="Employee not found")
    return employees[employee_id]


@app.get("/employees")
def get_employee_list(
    min_age: int = Query(None, ge=18),
    max_age: int = Query(None, le=100),
    city: str = Query(None),
    is_active: bool = Query(None)
):
    filtered_employees = employees

    if min_age is not None:
        filtered_employees = [e for e in filtered_employees if e.age >= min_age]
    if max_age is not None:
        filtered_employees = [e for e in filtered_employees if e.age <= max_age]
    if city is not None:
        filtered_employees = [e for e in filtered_employees if e.city == city]
    if is_active is not None:
        filtered_employees = [e for e in filtered_employees if e.is_active == is_active]

    return filtered_employees
