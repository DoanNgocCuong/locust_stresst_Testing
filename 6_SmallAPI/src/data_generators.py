"""
Module sinh dữ liệu test cho Qwen3-0.6B API Locust test.
Tuân thủ nguyên tắc Single Responsibility:
- Chỉ chịu trách nhiệm tạo test data cho API chat/completions.
"""

import random
from typing import Dict, Any, Sequence, Optional
from dataclasses import dataclass

from config import Config
from excel_data_loader import ExcelDataLoader


# Sample Questions cho test
SAMPLE_QUESTIONS = [
    "Tớ Chào Bể Hả! Hôm nay cậu muốn chơi một trò chơi nhỏ với tớ không? Let's play a game!",
    "What is your favorite color?",
    "Can you help me learn English?",
    "How do you say 'apple' in English?",
    "Let's practice speaking English together!",
    "I want to learn new words today.",
    "Can you teach me about animals?",
    "What is the weather like today?",
    "I feel happy today!",
    "Let's play a fun game together!",
    "I'm excited to learn something new!",
    "Can you explain this to me?",
    "I'm curious about English grammar.",
    "That's correct! You're doing great!",
    "I'm proud of my progress!",
    "Don't worry, everything will be fine.",
    "I'm afraid of making mistakes.",
    "I can't hear you properly, can you repeat?",
    "Let me think about this...",
    "I'm sad because I made a mistake.",
]

# Sample Answers cho test
SAMPLE_ANSWERS = [
    "i think a yummy",
    "My favorite color is blue.",
    "Yes, I'd love to help!",
    "Apple means 'quả táo' in Vietnamese.",
    "Sure! Let's practice together.",
    "Great! Let's start learning.",
    "Of course! Animals are fun to learn about.",
    "It's sunny and warm today.",
    "That's wonderful!",
    "Sounds fun! Let's do it!",
    "Me too! Learning is exciting!",
    "I'll explain it step by step.",
    "Great question! Let me explain.",
    "Thank you! I'm trying my best.",
    "You should be proud!",
    "Thank you for comforting me.",
    "It's okay, everyone makes mistakes.",
    "I'll speak louder for you.",
    "Take your time to think.",
    "It's okay, we learn from mistakes.",
]

# Sample Responses cho test (cần detect emotion và learn_score)
SAMPLE_RESPONSES = [
    "Nghe vui quá! Bể Hả, cậu có muốn chơi trò kể tên các loại trái cây bằng tiếng Anh không? Name fruits in English!",
    "That's great! Blue is a beautiful color.",
    "I'm happy to help you learn English! Let's start with basic words.",
    "Excellent! 'Apple' is a fruit. Can you name more fruits?",
    "Wonderful! Let's practice English conversation together!",
    "That's the spirit! Learning new words is exciting!",
    "Sure! Let's learn about animals. What animals do you like?",
    "Nice observation! The weather affects our mood.",
    "I'm so happy to hear that! Happiness is contagious!",
    "Great idea! Playing games makes learning fun!",
    "That's wonderful! Being excited helps us learn better!",
    "Of course! I'll explain it clearly for you.",
    "Good question! Curiosity leads to learning!",
    "You're absolutely right! Keep up the great work!",
    "You should be proud! Progress takes time and effort!",
    "Don't worry, everything will be okay. I'm here to help.",
    "It's normal to feel afraid. But remember, mistakes help us learn!",
    "I'll speak more clearly. Can you hear me now?",
    "Take your time. Thinking carefully is important.",
    "It's okay to feel sad. But remember, mistakes are part of learning!",
]


class MessageFactory:
    """Sinh user message ngẫu nhiên từ danh sách cho sẵn."""

    def __init__(
        self,
        questions: Optional[Sequence[str]] = None,
        answers: Optional[Sequence[str]] = None,
        responses: Optional[Sequence[str]] = None,
    ):
        """
        Khởi tạo MessageFactory với các danh sách mẫu.

        Args:
            questions: Danh sách câu hỏi mẫu
            answers: Danh sách câu trả lời mẫu
            responses: Danh sách response mẫu
        """
        self._questions = list(questions or SAMPLE_QUESTIONS)
        self._answers = list(answers or SAMPLE_ANSWERS)
        self._responses = list(responses or SAMPLE_RESPONSES)

        if not self._questions or not self._answers or not self._responses:
            raise ValueError(
                "MessageFactory requires at least one question, answer, and response."
            )

    def random_question(self) -> str:
        """Trả về một câu hỏi ngẫu nhiên."""
        return random.choice(self._questions)

    def random_answer(self) -> str:
        """Trả về một câu trả lời ngẫu nhiên."""
        return random.choice(self._answers)

    def random_response(self) -> str:
        """Trả về một response ngẫu nhiên."""
        return random.choice(self._responses)

    def random_triplet(self) -> tuple[str, str, str]:
        """
        Trả về bộ ba (question, answer, response) ngẫu nhiên.

        Returns:
            Tuple (question, answer, response)
        """
        return (
            self.random_question(),
            self.random_answer(),
            self.random_response(),
        )


@dataclass
class ChatCompletionPayload:
    """Dataclass chứa payload cho API chat/completions."""

    model: str
    messages: list[Dict[str, str]]
    temperature: float
    repetition_penalty: float
    stream: bool
    enable_thinking: bool
    max_tokens: Optional[int] = None
    stop_tokens: Optional[list[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi payload thành dictionary."""
        payload = {
            "model": self.model,
            "messages": self.messages,
            "temperature": self.temperature,
            "repetition_penalty": self.repetition_penalty,
            "stream": self.stream,
        }
        
        # API yêu cầu enable_thinking nằm trong chat_template_kwargs
        payload["chat_template_kwargs"] = {
            "enable_thinking": self.enable_thinking
        }

        if self.max_tokens is not None:
            payload["max_tokens"] = self.max_tokens
        if self.stop_tokens:
            payload["stop"] = self.stop_tokens
        
        return payload


class ChatCompletionPayloadFactory:
    """Factory tạo payload cho API chat/completions."""

    def __init__(
        self,
        model: str = None,
        system_prompt: str = None,
        temperature: float = None,
        repetition_penalty: float = None,
        stream: bool = None,
        enable_thinking: bool = None,
        max_tokens: Optional[int] = None,
        stop_tokens: Optional[Sequence[str]] = None,
        questions: Optional[Sequence[str]] = None,
        answers: Optional[Sequence[str]] = None,
        responses: Optional[Sequence[str]] = None,
        excel_loader: Optional[ExcelDataLoader] = None,
        use_excel_data: bool = False,
    ):
        """
        Khởi tạo PayloadFactory.

        Args:
            model: Tên model (default từ Config)
            system_prompt: System prompt (default từ Config)
            temperature: Temperature parameter (default từ Config)
            repetition_penalty: Repetition penalty (default từ Config)
            stream: Stream mode (default từ Config)
            enable_thinking: Enable thinking mode (default từ Config)
            questions: Danh sách questions mẫu
            answers: Danh sách answers mẫu
            responses: Danh sách responses mẫu
            excel_loader: ExcelDataLoader instance để đọc dữ liệu từ Excel
            use_excel_data: Nếu True, sử dụng dữ liệu từ Excel thay vì random
        """
        self.model = model or Config.MODEL_NAME
        self.system_prompt = system_prompt or Config.SYSTEM_PROMPT
        self.temperature = temperature if temperature is not None else Config.TEMPERATURE
        self.repetition_penalty = (
            repetition_penalty
            if repetition_penalty is not None
            else Config.REPETITION_PENALTY
        )
        self.stream = stream if stream is not None else Config.STREAM
        self.enable_thinking = (
            enable_thinking if enable_thinking is not None else Config.ENABLE_THINKING
        )
        self.max_tokens = max_tokens if max_tokens is not None else Config.MAX_TOKENS
        self.stop_tokens = list(stop_tokens) if stop_tokens is not None else Config.STOP_TOKENS

        self.excel_loader = excel_loader
        self.use_excel_data = use_excel_data and excel_loader is not None
        
        self.message_factory = MessageFactory(questions, answers, responses)

    def build_payload(
        self,
        question: Optional[str] = None,
        answer: Optional[str] = None,
        response: Optional[str] = None,
        new_data_content: Optional[str] = None,
    ) -> ChatCompletionPayload:
        """
        Tạo payload cho API chat/completions.

        Args:
            question: Câu hỏi (nếu None sẽ random hoặc lấy từ Excel)
            answer: Câu trả lời (nếu None sẽ random hoặc lấy từ Excel)
            response: Response cần check (nếu None sẽ random hoặc lấy từ Excel)
            new_data_content: Nội dung từ cột new_data (nếu có, sẽ dùng trực tiếp)

        Returns:
            ChatCompletionPayload object
        """
        # Nếu sử dụng dữ liệu từ Excel và có new_data_content
        if self.use_excel_data and new_data_content is None:
            new_data_content = self.excel_loader.get_random_new_data()
        
        # Nếu có new_data_content, sử dụng trực tiếp làm user content
        if new_data_content:
            user_content = new_data_content
        else:
            # Fallback về cách cũ: sử dụng question/answer/response
            # Nếu không có question/answer/response, random từ factory
            if question is None or answer is None or response is None:
                q, a, r = self.message_factory.random_triplet()
                question = question or q
                answer = answer or a
                response = response or r

            # Tạo user message content theo format yêu cầu
            user_content = (
                f"Question: {question}\n"
                f"Answer: {answer}\n"
                f"Response: {response}"
            )

        # Tạo messages array với role user
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_content},
        ]

        return ChatCompletionPayload(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            repetition_penalty=self.repetition_penalty,
            stream=self.stream,
            enable_thinking=self.enable_thinking,
            max_tokens=self.max_tokens,
            stop_tokens=self.stop_tokens,
        )

