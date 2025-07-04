from contextlib import asynccontextmanager
from gsv.common_config_manager import __version__, api_config
from gsv.gsv_state_manager import gsv_tts_state_manager
from gsv.api.routes import router as gsv_router
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时执行
    # 动态导入合成器模块, 此处可写成 from gsv.Synthesizers.xxx import TTS_Synthesizer, TTS_Task
    from importlib import import_module
    synthesizer_name = api_config.synthesizer
    synthesizer_module = import_module(f"gsv.Synthesizers.{synthesizer_name}")
    TTS_Synthesizer = synthesizer_module.TTS_Synthesizer
    # TTS_Task = synthesizer_module.TTS_Task
    # 初始化合成器的类
    tts_synthesizer = TTS_Synthesizer(debug_mode=True)
    gsv_tts_state_manager.set_state(tts_synthesizer)
    # 生成一句话充当测试，减少第一次请求的等待时间
    gen = tts_synthesizer.generate(tts_synthesizer.params_parser({"text":"筆者はすでにエッセイの序論"}) )
    next(gen)
    print(f"Backend Version: {__version__}")
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(gsv_router)