from dataclasses import dataclass, field


@dataclass
class Chat:
    message: str = field()
