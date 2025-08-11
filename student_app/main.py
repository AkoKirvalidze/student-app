import argparse
import json
from typing import List, Dict, Any, Union

from pydantic import BaseModel, Field, ValidationError, field_validator
from dicttoxml import dicttoxml


# --- Data Models ---
class Student(BaseModel):
    id: int
    name: str
    room: int

    @field_validator("id", "room")
    @classmethod
    def non_negative(cls, value):
        if value < 0:
            raise ValueError("ID and room must be non-negative")
        return value

    @field_validator("name")
    @classmethod
    def not_empty(cls, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        return value


class Room(BaseModel):
    id: int
    name: str


class RoomWithStudents(Room):
    students: List[Student] = Field(default_factory=list)


# --- Core Logic ---
class DataProcessor:
    def load_data(
        self, students_path: str, rooms_path: str
    ) -> tuple[List[Student], List[Room]]:
        """Load and validate JSON data for students and rooms."""
        try:
            with open(students_path, "r", encoding="utf-8") as f:
                students_data = json.load(f)
            with open(rooms_path, "r", encoding="utf-8") as f:
                rooms_data = json.load(f)

            students = [Student(**s) for s in students_data]
            rooms = [Room(**r) for r in rooms_data]
            return students, rooms

        except FileNotFoundError as e:
            raise RuntimeError(f"Missing file: {e}") from e
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON: {e}") from e
        except ValidationError as e:
            raise RuntimeError(f"Data validation failed: {e}") from e

    def combine_data(
            self, students: List[Student], rooms: List[Room]
    ) -> List[RoomWithStudents]:
        """Attach students to their corresponding rooms."""
        room_map = {room.id: RoomWithStudents(**room.model_dump()) for room in rooms}
        for student in students:
            if student.room in room_map:
                room_map[student.room].students.append(student)
        return list(room_map.values())

    def export_data(
        self, data: Union[List[RoomWithStudents], List[Dict[str, Any]]], fmt: str
    ):
        """Export data to JSON or XML."""
        if fmt == "json":
            print(json.dumps([r.model_dump() for r in data], indent=2))
        elif fmt == "xml":
            xml_bytes = dicttoxml(
                [r.model_dump() for r in data], custom_root="rooms", attr_type=False
            )
            print(xml_bytes.decode("utf-8"))
        else:
            raise ValueError(f"Unsupported format: {fmt}")


# --- CLI Entrypoint ---
def main():
    parser = argparse.ArgumentParser(
        description="Combine student and room data, export as JSON or XML."
    )
    parser.add_argument("--students", required=True, help="Path to students.json")
    parser.add_argument("--rooms", required=True, help="Path to rooms.json")
    parser.add_argument(
        "--format", choices=["json", "xml"], default="json", help="Output format"
    )

    args = parser.parse_args()
    processor = DataProcessor()

    try:
        students, rooms = processor.load_data(args.students, args.rooms)
        combined = processor.combine_data(students, rooms)
        processor.export_data(combined, args.format)
    except (RuntimeError, ValueError) as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
