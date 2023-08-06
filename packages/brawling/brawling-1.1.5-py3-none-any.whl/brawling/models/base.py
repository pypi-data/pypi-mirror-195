from dataclasses import dataclass

__all__ = [
    "BaseModel"
]

@dataclass
class BaseModel:
    @classmethod
    def from_json(cls, obj):
        raise NotImplementedError()

    @staticmethod
    def _from_props(cls, obj: dict, fieldstr):
        return cls(*[obj.get(f, None) for f in fieldstr.split(" ")])
