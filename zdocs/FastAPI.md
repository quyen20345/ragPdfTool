# 📘 ragPdfTool

Note **FastAPI**.

---


## get va post trong fastapi

```bash
- get: lay du lieu tu server
- post: 

```
---

## [Type hints cheat sheet](https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html)
```python
# Variables
age: int = 22
salary: int 
...

# Useful built-in types
# collections
x: List[int] = [1]
x: Set[int] = {6,7}
x: Dict[str, float] = {"field": 3.0}
x: Tuple[int, str, float] = (3, "yes", 8.0)
x: Tuple[int, ...] = (1, 2, 3)

# Union vs Optional
Uinon[int, str] mean a variable maybe "int" or "str"
Optional[int] mean a variable maybe "int" or "None"
Optional[int] similar Union[int, None]

# Functions
def stringify(num: int) -> str:
   return str(num)

def show_name(name: str) -> None:
   print(f"my name is {name}")
```
---

## 🛠 Xử lý lỗi cổng (port)

```bash
sudo lsof -i :8000        # Kiểm tra tiến trình chiếm cổng
sudo kill -9 <PID>        # Dừng tiến trình chiếm cổng
```
```