```python
import pydantic

print(pydantic.VERSION)
```

````markdown
## Using Pydantic for Regular Classes

**Yes** — Pydantic models can be used like regular Python classes by inheriting from `pydantic.BaseModel`.  
When the class is instantiated, Pydantic automatically performs **type coercion** and **validation**.

---

### Example

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class User(BaseModel):
    name: str
    age: int = Field(..., gt=0)  # must be greater than 0
    signup_date: Optional[date] = None

# ✅ Valid data — passes validation
u1 = User(name="Alice", age=25)
print(u1)

# ❌ Invalid data — raises pydantic.ValidationError
u2 = User(name="Bob", age=-5)
````

---

### How It Works

1. **Inheritance**

   * Inherit from `BaseModel` to turn your class into a Pydantic model.

2. **Automatic Validation**

   * When you instantiate the class, Pydantic:

     * Parses and coerces types (e.g., `"25"` → `25`, `"2025-08-13"` → `datetime.date`)
     * Validates against constraints (`gt=0`, regex, etc.)

3. **Normal Class Behavior**

   * After validation, the object behaves like a regular Python instance:

     ```python
     print(u1.name)   # "Alice"
     print(u1.age)    # 25
     ```

4. **No `__init__` Method Required**

   * You **don’t** need to define an `__init__` — Pydantic generates one automatically.
   * It accepts your declared fields as parameters, performs parsing, and sets attributes.
   * Example:

     ```python
     from pydantic import BaseModel

     class Item(BaseModel):
         name: str
         price: float

     # Instantiation without custom __init__
     item = Item(name="Laptop", price="999.99")  # string → float
     print(item.price)  # 999.99
     ```

---

✅ **Key takeaway**:
Pydantic models are regular Python classes with **built-in type checking and validation** that run automatically when you create an instance — no manual `__init__` required.


## Pydantic Field Definition Cheat Sheet (with `Annotated`)

| Case | Syntax | Example | Behavior |
|------|--------|---------|----------|
| **Required field** | `Annotated[type, Field(...)]` | `from typing import Annotated; from pydantic import BaseModel, Field; class User(BaseModel): name: Annotated[str, Field(min_length=1)]` | Must be provided and meet validation rules. |
| **Optional field (no validation)** | `Optional[type] = None` | `from typing import Optional; from pydantic import BaseModel; class User(BaseModel): nickname: Optional[str] = None` | Can be omitted or None; no extra validation. |
| **Optional field (with validation)** | `Annotated[Optional[type], Field(...)] = None` | `from typing import Optional, Annotated; from pydantic import BaseModel, Field; class User(BaseModel): age: Annotated[Optional[int], Field(gt=0)] = None` | Can be omitted or None; if provided, must meet validation rules. |
| **Python 3.10+ Optional shorthand** | `Annotated[type \| None, Field(...)] = None` | `from typing import Annotated; from pydantic import BaseModel, Field; class User(BaseModel): age: Annotated[int \| None, Field(gt=0)] = None` | Same as above, using union (`\|`) syntax. |


---

### Key Notes
1. **`Optional[X]`** (or `X | None` in Python 3.10+) means the field can be `None`.
2. If a field is `Optional` but **you don’t set a default**, it will still be required — it just allows `None` as a value.
3. To make a field truly *optional* (can be omitted), **set the default to `None`**.
4. Validation rules in `Field(...)` only apply when the value is not `None`.



```python
from typing import Annotated, List, Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    id: Annotated[
        int, Field(..., description="The unique identifier for the user", gt=0)
    ]
    name: Annotated[
        str,
        Field(..., description="The name of the user", min_length=1, max_length=100),
    ]
    email: Annotated[
        Optional[str],
        Field(
            None,
            description="The email address of the user",
            pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$",
        ),
    ] = None
    age: Annotated[
        Optional[int], Field(None, description="The age of the user", ge=0, le=120)
    ] = None
    tags: Annotated[
        List[str],
        Field(
            default_factory=list, description="A list of tags associated with the user"
        ),
    ]


user1 = User(
    id=123, name="John Doe", email="some@example.com", age=10, tags=["admin", "user"]
)

try:
    user2 = User(
        id=123,
        name="Jane Doe",
        email="some@example@com",
        age=1000,
        tags=["admin", "user"],
    )
except pydantic.ValidationError as e:
    error = e.errors()
    print("Validation error:", error)
    print("Error details:", e.json(indent=2))
    for err in error:
        print(f"Error in field '{err['loc'][0]}': {err['msg']} (type: {err['type']})")

```

````markdown
## Pydantic v2 — Field Validators: Before vs After

### Overview
Pydantic v2 lets you run **custom validation** on fields using `@field_validator`.  
You can control **when** the validator runs with the `mode` parameter:

- **`mode="before"`** → runs **before type parsing**  
- **`mode="after"`** → runs **after type parsing and built-in validation**

---

### Syntax Examples

#### 1. Before Validator
```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    age: int

    @field_validator("age", mode="before")
    def parse_age(cls, value):
        if isinstance(value, str):
            value = "".join(ch for ch in value if ch.isdigit())
        return int(value)

User(age="25 years").age  # 25
````

#### 2. After Validator

```python
class User(BaseModel):
    age: int

    @field_validator("age", mode="after")
    def validate_age(cls, value):
        if not (0 <= value <= 120):
            raise ValueError("Invalid age range")
        return value

User(age=30).age  # ✅ OK
```

#### 3. Combined Example

```python
class User(BaseModel):
    age: int

    @field_validator("age", mode="before")
    def strip_units(cls, v):
        if isinstance(v, str):
            v = v.replace("years", "").strip()
        return v

    @field_validator("age", mode="after")
    def check_range(cls, v):
        if not (0 <= v <= 120):
            raise ValueError("Invalid age range")
        return v

User(age="25 years").age  # 25
```

---

### Validation Flow

```text
Raw Input
    │
    ▼
before validator (mode="before")
    │
    ▼
Pydantic type parsing & built-in validation
    │
    ▼
after validator (mode="after")
    │
    ▼
Final Value
```

### Key Points

* **Before** → transform or normalize raw input
* **After** → enforce rules on parsed/validated values
* You can combine both to clean input **and** apply business rules

### Annotated field validators

https://docs.pydantic.dev/latest/concepts/validators/



```python
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ValidationError


def is_even(value: int) -> int:
    if value % 2 == 1:
        raise ValueError(f"{value} is not an even number")
    return value


class Model(BaseModel):
    number: Annotated[int, AfterValidator(is_even)]


try:
    Model(number=1)
except ValidationError as err:
    print(err)
```

In **Pydantic v2**, a **`@model_validator`** is used to run **validation logic that involves multiple fields at once** — essentially for **cross-field or whole-model validation**.

Unlike `@field_validator`, which validates a single field, `@model_validator` works on the **entire model instance** (or the input data) after or before field-level parsing, depending on the `mode`.

---

## **Key Points**

* Works at the **model level**, not individual fields.
* Can enforce rules like:

  * “Field B must be greater than Field A”
  * “Either field X or field Y must be provided”
* Supports `mode="before"` (runs before type parsing) or `mode="after"` (runs after parsing & field validation).

---

## **Example — Cross-Field Validation**

```python
from pydantic import BaseModel, model_validator, ValidationError

class Order(BaseModel):
    quantity: int
    price_per_item: float
    discount: float = 0.0

    # Ensure total price > discount
    @model_validator(mode="after")
    def check_discount(cls, values):
        total = values['quantity'] * values['price_per_item']
        if values['discount'] > total:
            raise ValueError("Discount cannot exceed total price")
        return values

# ✅ Valid
Order(quantity=5, price_per_item=10, discount=20)

# ❌ Invalid
# Order(quantity=2, price_per_item=10, discount=25)  # ValidationError
```

---

## **Before vs After**

| Mode     | When it runs                           | Use case                                |
| -------- | -------------------------------------- | --------------------------------------- |
| `before` | Before field parsing/type coercion     | Normalize raw input for multiple fields |
| `after`  | After field parsing & field validators | Enforce cross-field business rules      |

---

✅ **Key takeaway**:

* `@model_validator` is the tool for **whole-model or multi-field validation**.
* Combine with `@field_validator` to validate both **individual fields** and **relationships between fields**.

---




Here’s a **Jupyter Notebook–ready Markdown cheat sheet** comparing **instance-style vs class-style `@model_validator`** in Pydantic v2:

````markdown
## Pydantic v2 — Model Validator Styles

`@model_validator` lets you run validation logic that depends on multiple fields in your model.

---

### **1. Instance-style Validator (`self`)**
- First parameter: `self` (the model instance)
- Returns: `self` (possibly modified)
- Works **after parsing & field validation** (`mode="after"`)
- Clean and intuitive when working with the model directly

```python
from pydantic import BaseModel, model_validator
from typing import Self

class UserModel(BaseModel):
    username: str
    password: str
    password_repeat: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError("Passwords do not match")
        return self

# ✅ Example
user = UserModel(username="alice", password="1234", password_repeat="1234")
````

---

### **2. Class-style Validator (`cls`)**

* First parameter: `cls` (the class)
* Receives: `values` dictionary of field values
* Returns: dictionary of validated/modified values
* Useful for **pre-processing before instance creation** (`mode="before"`) or after field-level validation

```python
from pydantic import BaseModel, model_validator

class UserModel(BaseModel):
    username: str
    password: str
    password_repeat: str

    @model_validator(mode="after")
    def check_passwords_match(cls, values):
        if values['password'] != values['password_repeat']:
            raise ValueError("Passwords do not match")
        return values

# ✅ Example
user = UserModel(username="alice", password="1234", password_repeat="1234")
```

---

### **Comparison Table**

| Style        | First Parameter | Returns                 | Use Case                                                   |
| ------------ | --------------- | ----------------------- | ---------------------------------------------------------- |
| **Instance** | `self`          | Model instance (`self`) | Access fields directly after parsing                       |
| **Class**    | `cls`           | `dict` of values        | Pre- or post-processing values before instance is returned |

---

✅ **Key Takeaways**

* Use **instance-style** when you want simple access to the model fields after creation.
* Use **class-style** when you need to manipulate field values before or during instance creation.
* Both can enforce cross-field or whole-model validation rules.


```python
from pydantic import BaseModel, ValidationError, model_validator
from typing_extensions import Self


class UserModel(BaseModel):
    username: str
    password: str
    password_repeat: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError("Passwords do not match")
        return self


try:
    user = UserModel(
        username="john_doe", password="secret123", password_repeat="secret1234"
    )
except ValidationError as e:
    error = e.errors()
    print("Error details:", e.json(indent=2))
    for err in error:
        field_name = err["loc"][0] if err["loc"] else "__root__"
        print(f"Error in field '{field_name}': {err['msg']} (type: {err['type']})")
```

If you want **optional fields** so you don’t have to use `...` for required fields, you can use **`Annotated[Optional[type], Field(...)] = None`** or the Python 3.10+ syntax `type | None`.

````markdown
## Dynamic Pydantic Models with Optional Fields and Validators

`create_model` allows you to **generate Pydantic models at runtime**. Using `Annotated` with `Optional`, you can avoid `...` while still supporting validation. Field and model validators can be attached dynamically.

---

### **Create Dynamic Model**

```python
from typing import Annotated, Optional
from pydantic import create_model, Field, field_validator, model_validator, ValidationError

# Field-level validator
def validate_username(cls, value):
    if value is not None and len(value) < 3:
        raise ValueError("Username too short")
    return value

# Model-level validator
def check_passwords_match(self):
    if self.password is not None and self.password_repeat is not None:
        if self.password != self.password_repeat:
            raise ValueError("Passwords do not match")
    return self

# Create dynamic model with optional fields
DynamicUser = create_model(
    'DynamicUser',
    username=(Annotated[Optional[str], Field(min_length=1)], None),
    password=(Annotated[Optional[str], Field(min_length=6)], None),
    password_repeat=(Annotated[Optional[str], Field(min_length=6)], None),
    age=(Annotated[Optional[int], Field(gt=0)], 30),
    __validators__={
        'username_validator': field_validator('username', mode='after')(validate_username),
        'password_match_validator': model_validator(check_passwords_match, mode='after')
    }
)
````

---

### **Instantiate and Validate**

```python
from pydantic import ValidationError

try:
    user = DynamicUser(username='al', password='secret123', password_repeat='secret1234')
except ValidationError as e:
    print(e.json(indent=2))
```

---

### **Key Points**

* Using `Optional[type] = None` avoids `...` for required fields.
* Field validators check individual fields.
* Model validators check cross-field logic.
* `Annotated` allows attaching validation constraints like `min_length` or `gt`.
* Default values make fields optional while still enforcing validation if a value is provided.

```



```python
from typing import Annotated, Optional

from pydantic import BaseModel, Field, PrivateAttr, create_model, field_validator


def alphanum(cls, v):
    if not v.isalnum():
        raise ValueError("must be alphanumeric")
    return v


validators = {"foo_validator": field_validator("foo")(alphanum)}

DynamicModel = create_model(
    "DynamicModel",
    foo=(str, Field(alias="FOO")),
    bar=(Annotated[Optional[str], Field(description="Bar field")], None),
    _private=(int, PrivateAttr(default=1)),
    __validators=validators,
)

# This dynamic model can be used like a regular Pydantic model
try:
    instance = DynamicModel(foo="valid", bar="test")
    print(instance)
except ValidationError as e:
    print("Validation error:", e.errors())
    print("Error details:", e.json(indent=2))


# Is equivalent to:
class StaticModel(BaseModel):
    foo: str = Field(alias="FOO")
    bar: Annotated[str, Field(description="Bar field")]
    _private: int = PrivateAttr(default=1)
```
