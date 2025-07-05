# 在开头加入路径
import os
from fastapi import Request, HTTPException, APIRouter
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse# 将当前文件所在的目录添加到 sys.path
from gsv.Synthesizers.base import Base_TTS_Task
from gsv.gsv_state_manager import gsv_tts_state_manager
# 创建合成器实例

router = APIRouter()

# def set_tts_synthesizer(synthesizer:Base_TTS_Synthesizer):
#     global tts_synthesizer
#     tts_synthesizer = synthesizer

@router.post("/tts/gptsovits/character_list")
async def character_list(request: Request):
    tts_synthesizer = gsv_tts_state_manager.get_tts_synthesizer()
    if tts_synthesizer is None:
        return HTTPException(status_code=500, detail="TTS synthesizer not initialized")
    res = JSONResponse(tts_synthesizer.get_characters())
    return res

@router.post("/tts/gptsovits")
async def tts(request: Request):
    
    from time import time as tt
    t1 = tt()
    # 存储临时文件的字典
    temp_files = {}
    print(f"Request Time: {t1}")
    
    # 尝试从JSON中获取数据，如果不是JSON，则从查询参数中获取
    if request.method == "GET":
        data = request.query_params
    else:
        data = await request.json()
    tts_synthesizer = gsv_tts_state_manager.get_tts_synthesizer()
    if tts_synthesizer is None:
        return HTTPException(status_code=500, detail="TTS synthesizer not initialized")
    task:Base_TTS_Task = tts_synthesizer.params_parser(data) # type: ignore

    if task.task_type == "text" and task.text.strip() == "": # type: ignore
        return HTTPException(status_code=400, detail="Text is empty")
    elif task.task_type == "ssml" and task.ssml.strip() == "": # type: ignore
        return HTTPException(status_code=400, detail="SSML is empty")
    md5_value = task.md5
    if task.stream == False:
        # TODO: use SQL instead of dict
        if task.save_temp and md5_value in temp_files:
            return FileResponse(path=temp_files[md5_value], media_type=f'audio/{task.format}')
        else:
            # 假设 gen 是你的音频生成器
            try:
                save_path = tts_synthesizer.generate(task, return_type="filepath")
            except Exception as e:
                return HTTPException(status_code=500, detail=str(e))
            if task.save_temp:
                temp_files[md5_value] = save_path

            t2 = tt()
            print(f"total time: {t2-t1}")
            # 返回文件响应，FileResponse 会负责将文件发送给客户端
            return FileResponse(save_path, media_type=f"audio/{task.format}", filename=os.path.basename(save_path))
    else:
        gen = tts_synthesizer.generate(task, return_type="numpy")
        return StreamingResponse(gen,  media_type='audio/wav')
