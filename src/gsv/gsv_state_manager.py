from gsv.Synthesizers.base import Base_TTS_Synthesizer

class GPTSoVITSStateManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.tts_synthesizer = None
        return cls._instance

    def set_state(self, tts_synthesizers: Base_TTS_Synthesizer):
        self.tts_synthesizer = tts_synthesizers

    def get_tts_synthesizer(self) -> Base_TTS_Synthesizer | None:
        return self.tts_synthesizer

# 全局存活
gsv_tts_state_manager = GPTSoVITSStateManager()